from datetime import datetime
from typing import List, Dict, Optional, Tuple
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_, desc, asc

from app.models.user_point import UserPoint
from app.models.point_history import PointHistory
from app.schemas.gamification import (
    UserPointsResponse,
    UserPointsDetail,
    PointsHistoryResponse,
    PointHistoryItem
)


class PointsService:
    """Serviço para gerenciamento de pontos dos usuários"""

    def __init__(self, db: Session):
        self.db = db

        # Categorias válidas de pontos
        self._valid_categories = [
            "oracao",
            "estudo",
            "compartilhamento",
            "quiz",
            "presenca",
            "comentario",
            "reflexao",
            "interacao",
            "contribuicao",
            "geral"
        ]

        # Fontes de ação válidas para alterar pontos
        self._valid_action_sources = [
            "ms-auth",
            "ms-study",
            "ms-bible",
            "ms-chatia",
            "ms-admin",
            "ms-gamification",
            "ms-monetization"
        ]

    async def get_user_points(self, user_id: str) -> UserPointsResponse:
        """
        Obtém os pontos do usuário, incluindo detalhes por categoria.

        Args:
            user_id: ID do usuário

        Returns:
            Objeto com informações de pontos do usuário
        """
        # Obter os pontos por categoria
        points_by_category = self.db.query(UserPoint).filter(
            UserPoint.user_id == user_id
        ).all()

        # Se não encontrar, retornar zero em todas categorias
        if not points_by_category:
            # Criar pontuação inicial para o usuário
            points_by_category = []
            for category in self._valid_categories:
                point = UserPoint(
                    id=str(uuid4()),
                    user_id=user_id,
                    category=category,
                    amount=0,
                    updated_at=datetime.utcnow()
                )
                self.db.add(point)
                points_by_category.append(point)

            self.db.commit()

        # Calcular pontuação total
        total_points = sum(point.amount for point in points_by_category)

        # Montar detalhes por categoria
        points_details = [
            UserPointsDetail(
                category=point.category,
                amount=point.amount,
                updated_at=point.updated_at
            ) for point in points_by_category
        ]

        return UserPointsResponse(
            user_id=user_id,
            total_points=total_points,
            points_by_category=points_details
        )

    async def get_points_history(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None
    ) -> PointsHistoryResponse:
        """
        Obtém o histórico de transações de pontos do usuário.

        Args:
            user_id: ID do usuário
            skip: Quantos registros pular (para paginação)
            limit: Limite de registros a retornar
            category: Filtrar por categoria específica

        Returns:
            Histórico de pontos paginado
        """
        # Construir a query base
        query = self.db.query(PointHistory).filter(
            PointHistory.user_id == user_id
        )

        # Adicionar filtro de categoria se fornecido
        if category:
            query = query.filter(PointHistory.category == category)

        # Obter o total para paginação
        total = query.count()

        # Aplicar ordenação e paginação
        query = query.order_by(
            desc(PointHistory.created_at)).offset(skip).limit(limit)

        # Executar a consulta
        history_items = query.all()

        # Montar resposta
        history = [
            PointHistoryItem(
                id=item.id,
                amount=item.amount,
                category=item.category,
                description=item.description,
                created_at=item.created_at,
                action_source=item.action_source
            ) for item in history_items
        ]

        return PointsHistoryResponse(
            items=history,
            total=total,
            skip=skip,
            limit=limit
        )

    async def add_points(
        self,
        user_id: str,
        amount: int,
        category: str,
        description: str,
        action_source: str
    ) -> UserPointsDetail:
        """
        Adiciona pontos para um usuário.

        Args:
            user_id: ID do usuário
            amount: Quantidade de pontos (positivo)
            category: Categoria dos pontos
            description: Descrição da ação realizada
            action_source: Fonte da ação (microsserviço)

        Returns:
            Detalhes atualizados dos pontos na categoria

        Raises:
            ValueError: Se os parâmetros forem inválidos
        """
        # Validações
        if amount <= 0:
            raise ValueError("Quantidade de pontos deve ser positiva")

        if category not in self._valid_categories:
            raise ValueError(
                f"Categoria inválida. Categorias válidas: {', '.join(self._valid_categories)}")

        if action_source not in self._valid_action_sources:
            raise ValueError(
                f"Fonte de ação inválida. Fontes válidas: {', '.join(self._valid_action_sources)}")

        # Buscar o registro de pontos do usuário para a categoria
        user_point = self.db.query(UserPoint).filter(
            and_(
                UserPoint.user_id == user_id,
                UserPoint.category == category
            )
        ).first()

        # Se não existir, criar um novo
        if not user_point:
            user_point = UserPoint(
                id=str(uuid4()),
                user_id=user_id,
                category=category,
                amount=0,
                updated_at=datetime.utcnow()
            )
            self.db.add(user_point)

        # Atualizar pontos
        user_point.amount += amount
        user_point.updated_at = datetime.utcnow()

        # Registrar no histórico
        history_entry = PointHistory(
            id=str(uuid4()),
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            action_source=action_source,
            created_at=datetime.utcnow()
        )

        self.db.add(history_entry)
        self.db.commit()
        self.db.refresh(user_point)

        # Verificar conquistas
        await self._check_point_achievements(user_id, category, user_point.amount)

        return UserPointsDetail(
            category=user_point.category,
            amount=user_point.amount,
            updated_at=user_point.updated_at
        )

    async def subtract_points(
        self,
        user_id: str,
        amount: int,
        category: str,
        description: str,
        action_source: str
    ) -> UserPointsDetail:
        """
        Remove pontos de um usuário.

        Args:
            user_id: ID do usuário
            amount: Quantidade de pontos a remover (positivo)
            category: Categoria dos pontos
            description: Descrição da ação realizada
            action_source: Fonte da ação (microsserviço)

        Returns:
            Detalhes atualizados dos pontos na categoria

        Raises:
            ValueError: Se os parâmetros forem inválidos
        """
        # Validações
        if amount <= 0:
            raise ValueError("Quantidade de pontos deve ser positiva")

        if category not in self._valid_categories:
            raise ValueError(
                f"Categoria inválida. Categorias válidas: {', '.join(self._valid_categories)}")

        if action_source not in self._valid_action_sources:
            raise ValueError(
                f"Fonte de ação inválida. Fontes válidas: {', '.join(self._valid_action_sources)}")

        # Buscar o registro de pontos do usuário para a categoria
        user_point = self.db.query(UserPoint).filter(
            and_(
                UserPoint.user_id == user_id,
                UserPoint.category == category
            )
        ).first()

        # Se não existir ou não tiver pontos suficientes, erro
        if not user_point or user_point.amount < amount:
            raise ValueError("Pontos insuficientes para a operação")

        # Atualizar pontos
        user_point.amount -= amount
        user_point.updated_at = datetime.utcnow()

        # Registrar no histórico (valor negativo)
        history_entry = PointHistory(
            id=str(uuid4()),
            user_id=user_id,
            amount=-amount,  # Valor negativo para indicar subtração
            category=category,
            description=description,
            action_source=action_source,
            created_at=datetime.utcnow()
        )

        self.db.add(history_entry)
        self.db.commit()
        self.db.refresh(user_point)

        return UserPointsDetail(
            category=user_point.category,
            amount=user_point.amount,
            updated_at=user_point.updated_at
        )

    async def get_point_categories(self) -> List[str]:
        """
        Retorna a lista de categorias de pontos disponíveis.

        Returns:
            Lista de categorias válidas
        """
        return self._valid_categories

    async def _check_point_achievements(self, user_id: str, category: str, amount: int) -> None:
        """
        Verifica e atualiza conquistas relacionadas a pontos.

        Esta função é chamada internamente após ganho de pontos
        para verificar se o usuário alcançou alguma nova conquista.

        Args:
            user_id: ID do usuário
            category: Categoria dos pontos
            amount: Quantidade total atual
        """
        # Esta é uma implementação inicial simplificada
        # Em uma versão mais completa, verificaria conquistas no banco de dados
        # Para simplificar, estamos apenas logando a verificação por enquanto
        print(
            f"Verificando conquistas para user_id={user_id}, categoria={category}, total={amount}")

        # TODO: Implementar integração com o serviço de conquistas
        pass
