from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_, desc, asc, case

from app.models.user_point import UserPoint
from app.models.point_history import PointHistory
from app.schemas.gamification import (
    LeaderboardResponse,
    LeaderboardEntryResponse,
    UserRankingResponse
)


class LeaderboardService:
    """Serviço para gerenciamento de rankings e leaderboards"""

    def __init__(self, db: Session):
        self.db = db

        # Períodos válidos para o leaderboard
        self._valid_periods = ["daily", "weekly", "monthly", "all_time"]

    async def get_leaderboard(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        time_period: str = "all_time"
    ) -> LeaderboardResponse:
        """
        Obtém o ranking de usuários com base em pontos.

        Args:
            skip: Quantos registros pular (para paginação)
            limit: Limite de registros a retornar
            category: Filtrar por categoria específica (se None, usa pontos totais)
            time_period: Período de tempo a considerar (daily, weekly, monthly, all_time)

        Returns:
            Ranking paginado de usuários
        """
        # Validar o período
        if time_period not in self._valid_periods:
            time_period = "all_time"

        # Determinar o momento inicial com base no período
        from_date = self._get_period_start_date(time_period)

        # Obter dados do ranking
        if time_period == "all_time" and category is None:
            # Caso mais simples: total de pontos global
            ranking_data = await self._get_all_time_total_ranking(skip, limit)
        elif time_period == "all_time" and category is not None:
            # Total de pontos de uma categoria específica
            ranking_data = await self._get_all_time_category_ranking(category, skip, limit)
        else:
            # Ranking por período específico
            ranking_data = await self._get_period_ranking(time_period, category, from_date, skip, limit)

        # Extrair dados e total
        entries, total = ranking_data

        # Montar a resposta
        return LeaderboardResponse(
            entries=entries,
            total=total,
            skip=skip,
            limit=limit,
            period=time_period,
            category=category
        )

    async def get_user_ranking(
        self,
        user_id: str,
        category: Optional[str] = None,
        time_period: str = "all_time"
    ) -> UserRankingResponse:
        """
        Obtém a posição do usuário no ranking.

        Args:
            user_id: ID do usuário
            category: Filtrar por categoria específica (se None, usa pontos totais)
            time_period: Período de tempo a considerar

        Returns:
            Detalhes da posição do usuário no ranking
        """
        # Validar o período
        if time_period not in self._valid_periods:
            time_period = "all_time"

        # Determinar o momento inicial com base no período
        from_date = self._get_period_start_date(time_period)

        # Obter pontos do usuário
        user_points = await self._get_user_points_for_period(user_id, category, from_date)

        # Contar usuários com mais pontos
        users_ahead = await self._count_users_ahead(user_id, category, from_date, user_points)

        # Calcular ranking (posição é baseada em zero, então +1)
        rank = users_ahead + 1

        # Obter usuário acima e abaixo no ranking
        user_above = await self._get_user_at_position(rank - 1, category, from_date) if rank > 1 else None
        user_below = await self._get_user_at_position(rank + 1, category, from_date)

        # Calcular pontos necessários para subir no ranking
        points_to_advance = user_above["points"] - \
            user_points if user_above else 0

        # Calcular pontos de vantagem para o usuário abaixo
        points_advantage = user_points - \
            user_below["points"] if user_below else 0

        # Montar a resposta
        return UserRankingResponse(
            user_id=user_id,
            rank=rank,
            points=user_points,
            category=category,
            period=time_period,
            total_participants=await self._count_total_users_in_ranking(category, from_date),
            points_to_advance=points_to_advance,
            points_advantage=points_advantage,
            next_user=user_above["user_id"] if user_above else None,
            previous_user=user_below["user_id"] if user_below else None
        )

    async def get_friends_leaderboard(
        self,
        user_id: str,
        category: Optional[str] = None,
        time_period: str = "all_time"
    ) -> LeaderboardResponse:
        """
        Obtém o ranking apenas entre amigos do usuário.

        Args:
            user_id: ID do usuário
            category: Filtrar por categoria específica (se None, usa pontos totais)
            time_period: Período de tempo a considerar

        Returns:
            Ranking com o usuário e seus amigos
        """
        # TODO: Implementar integração com serviço de amizades

        # Por enquanto, implementação simplificada que retorna os 10 usuários com pontuação próxima
        user_points = await self._get_user_points_for_period(
            user_id,
            category,
            self._get_period_start_date(time_period)
        )

        # Obter 5 usuários acima e 5 abaixo
        entries_above = await self._get_users_around_points(
            user_points,
            higher=True,
            limit=5,
            category=category,
            from_date=self._get_period_start_date(time_period),
            exclude_user_id=user_id
        )

        entries_below = await self._get_users_around_points(
            user_points,
            higher=False,
            limit=5,
            category=category,
            from_date=self._get_period_start_date(time_period),
            exclude_user_id=user_id
        )

        # Adicionar o próprio usuário
        user_entry = LeaderboardEntryResponse(
            rank=await self._count_users_ahead(user_id, category, self._get_period_start_date(time_period), user_points) + 1,
            user_id=user_id,
            points=user_points,
            is_current_user=True
        )

        # Combinar e ordenar por pontos (decrescente)
        all_entries = entries_above + [user_entry] + entries_below
        all_entries.sort(key=lambda x: x.points, reverse=True)

        # Reajustar ranking
        for i, entry in enumerate(all_entries, 1):
            entry.rank = i

        return LeaderboardResponse(
            entries=all_entries,
            total=len(all_entries),
            skip=0,
            limit=len(all_entries),
            period=time_period,
            category=category
        )

    async def get_leaderboard_categories(self) -> List[str]:
        """
        Retorna a lista de categorias disponíveis para o ranking.

        Returns:
            Lista de categorias
        """
        # Consultar categorias únicas no banco de dados
        query = self.db.query(UserPoint.category).distinct()
        categories = [row[0] for row in query.all()]

        return categories

    def _get_period_start_date(self, period: str) -> Optional[datetime]:
        """
        Determina a data de início para um período de tempo.

        Args:
            period: Período (daily, weekly, monthly, all_time)

        Returns:
            Data de início ou None para all_time
        """
        if period == "all_time":
            return None

        now = datetime.utcnow()

        if period == "daily":
            # Início do dia atual (00:00:00)
            return datetime(now.year, now.month, now.day, 0, 0, 0)

        elif period == "weekly":
            # Início da semana atual (segunda-feira)
            days_since_monday = now.weekday()
            return (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)

        elif period == "monthly":
            # Início do mês atual
            return datetime(now.year, now.month, 1, 0, 0, 0)

        # Fallback para all_time
        return None

    async def _get_all_time_total_ranking(
        self,
        skip: int,
        limit: int
    ) -> Tuple[List[LeaderboardEntryResponse], int]:
        """
        Obtém o ranking global de todos os tempos com base na soma total de pontos.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Tupla com lista de entradas do ranking e total de usuários
        """
        # Subconsulta para somar pontos por usuário
        subquery = self.db.query(
            UserPoint.user_id,
            func.sum(UserPoint.amount).label("total_points")
        ).group_by(
            UserPoint.user_id
        ).subquery()

        # Consulta principal para obter os usuários ordenados por pontos
        query = self.db.query(
            subquery.c.user_id,
            subquery.c.total_points
        ).order_by(
            desc(subquery.c.total_points)
        )

        # Contar total para paginação
        total = query.count()

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a consulta
        results = query.all()

        # Criar as entradas do ranking
        entries = []
        for i, (user_id, points) in enumerate(results, skip + 1):
            entries.append(LeaderboardEntryResponse(
                rank=i,
                user_id=user_id,
                points=points,
                is_current_user=False  # Será atualizado depois se necessário
            ))

        return entries, total

    async def _get_all_time_category_ranking(
        self,
        category: str,
        skip: int,
        limit: int
    ) -> Tuple[List[LeaderboardEntryResponse], int]:
        """
        Obtém o ranking global de todos os tempos para uma categoria específica.

        Args:
            category: Categoria de pontos
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Tupla com lista de entradas do ranking e total de usuários
        """
        # Consulta para obter os usuários ordenados por pontos na categoria
        query = self.db.query(
            UserPoint.user_id,
            UserPoint.amount
        ).filter(
            UserPoint.category == category
        ).order_by(
            desc(UserPoint.amount)
        )

        # Contar total para paginação
        total = query.count()

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a consulta
        results = query.all()

        # Criar as entradas do ranking
        entries = []
        for i, (user_id, points) in enumerate(results, skip + 1):
            entries.append(LeaderboardEntryResponse(
                rank=i,
                user_id=user_id,
                points=points,
                is_current_user=False  # Será atualizado depois se necessário
            ))

        return entries, total

    async def _get_period_ranking(
        self,
        period: str,
        category: Optional[str],
        from_date: datetime,
        skip: int,
        limit: int
    ) -> Tuple[List[LeaderboardEntryResponse], int]:
        """
        Obtém o ranking para um período específico.

        Args:
            period: Período (daily, weekly, monthly)
            category: Categoria de pontos ou None para total
            from_date: Data de início do período
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Tupla com lista de entradas do ranking e total de usuários
        """
        # Construir consulta base no histórico de pontos
        base_query = self.db.query(
            PointHistory.user_id,
            func.sum(PointHistory.amount).label("period_points")
        ).filter(
            PointHistory.created_at >= from_date
        )

        # Adicionar filtro de categoria se necessário
        if category:
            base_query = base_query.filter(PointHistory.category == category)

        # Agrupar por usuário e ordenar
        subquery = base_query.group_by(
            PointHistory.user_id
        ).subquery()

        # Consulta principal para ordenar por pontos
        query = self.db.query(
            subquery.c.user_id,
            subquery.c.period_points
        ).order_by(
            desc(subquery.c.period_points)
        )

        # Contar total para paginação
        total = query.count()

        # Aplicar paginação
        query = query.offset(skip).limit(limit)

        # Executar a consulta
        results = query.all()

        # Criar as entradas do ranking
        entries = []
        for i, (user_id, points) in enumerate(results, skip + 1):
            entries.append(LeaderboardEntryResponse(
                rank=i,
                user_id=user_id,
                points=points,
                is_current_user=False  # Será atualizado depois se necessário
            ))

        return entries, total

    async def _get_user_points_for_period(
        self,
        user_id: str,
        category: Optional[str],
        from_date: Optional[datetime]
    ) -> int:
        """
        Obtém os pontos de um usuário para um período e categoria específicos.

        Args:
            user_id: ID do usuário
            category: Categoria específica ou None para total
            from_date: Data de início ou None para todos os tempos

        Returns:
            Total de pontos
        """
        if from_date is None:
            # Todos os tempos
            if category:
                # Categoria específica
                point = self.db.query(UserPoint).filter(
                    and_(
                        UserPoint.user_id == user_id,
                        UserPoint.category == category
                    )
                ).first()

                return point.amount if point else 0
            else:
                # Total de todas as categorias
                points = self.db.query(
                    func.sum(UserPoint.amount)
                ).filter(
                    UserPoint.user_id == user_id
                ).scalar()

                return points or 0
        else:
            # Período específico
            query = self.db.query(
                func.sum(PointHistory.amount)
            ).filter(
                and_(
                    PointHistory.user_id == user_id,
                    PointHistory.created_at >= from_date
                )
            )

            # Adicionar filtro de categoria se necessário
            if category:
                query = query.filter(PointHistory.category == category)

            points = query.scalar()
            return points or 0

    async def _count_users_ahead(
        self,
        user_id: str,
        category: Optional[str],
        from_date: Optional[datetime],
        user_points: int
    ) -> int:
        """
        Conta quantos usuários estão à frente do usuário no ranking.

        Args:
            user_id: ID do usuário
            category: Categoria específica ou None para total
            from_date: Data de início ou None para todos os tempos
            user_points: Pontos atuais do usuário

        Returns:
            Número de usuários à frente
        """
        if from_date is None:
            # Todos os tempos
            if category:
                # Categoria específica
                return self.db.query(UserPoint).filter(
                    and_(
                        UserPoint.category == category,
                        UserPoint.amount > user_points
                    )
                ).count()
            else:
                # Total de todas as categorias
                subquery = self.db.query(
                    UserPoint.user_id,
                    func.sum(UserPoint.amount).label("total_points")
                ).group_by(
                    UserPoint.user_id
                ).subquery()

                return self.db.query(subquery).filter(
                    subquery.c.total_points > user_points
                ).count()
        else:
            # Período específico
            base_query = self.db.query(
                PointHistory.user_id,
                func.sum(PointHistory.amount).label("period_points")
            ).filter(
                PointHistory.created_at >= from_date
            )

            # Adicionar filtro de categoria se necessário
            if category:
                base_query = base_query.filter(
                    PointHistory.category == category)

            # Agrupar por usuário
            subquery = base_query.group_by(
                PointHistory.user_id
            ).subquery()

            # Contar usuários com mais pontos
            return self.db.query(subquery).filter(
                subquery.c.period_points > user_points
            ).count()

    async def _get_user_at_position(
        self,
        position: int,
        category: Optional[str],
        from_date: Optional[datetime]
    ) -> Optional[Dict[str, Any]]:
        """
        Obtém o usuário em uma posição específica do ranking.

        Args:
            position: Posição no ranking (baseada em 1)
            category: Categoria específica ou None para total
            from_date: Data de início ou None para todos os tempos

        Returns:
            Dicionário com user_id e points, ou None se a posição não existir
        """
        if position < 1:
            return None

        if from_date is None:
            # Todos os tempos
            if category:
                # Categoria específica
                query = self.db.query(
                    UserPoint.user_id,
                    UserPoint.amount
                ).filter(
                    UserPoint.category == category
                ).order_by(
                    desc(UserPoint.amount)
                )
            else:
                # Total de todas as categorias
                subquery = self.db.query(
                    UserPoint.user_id,
                    func.sum(UserPoint.amount).label("total_points")
                ).group_by(
                    UserPoint.user_id
                ).subquery()

                query = self.db.query(
                    subquery.c.user_id,
                    subquery.c.total_points
                ).order_by(
                    desc(subquery.c.total_points)
                )
        else:
            # Período específico
            base_query = self.db.query(
                PointHistory.user_id,
                func.sum(PointHistory.amount).label("period_points")
            ).filter(
                PointHistory.created_at >= from_date
            )

            # Adicionar filtro de categoria se necessário
            if category:
                base_query = base_query.filter(
                    PointHistory.category == category)

            # Agrupar por usuário
            subquery = base_query.group_by(
                PointHistory.user_id
            ).subquery()

            # Ordenar por pontos
            query = self.db.query(
                subquery.c.user_id,
                subquery.c.period_points
            ).order_by(
                desc(subquery.c.period_points)
            )

        # Aplicar offset para obter a posição específica
        query = query.offset(position - 1).limit(1)

        # Executar a consulta
        result = query.first()

        if not result:
            return None

        return {
            "user_id": result[0],
            "points": result[1]
        }

    async def _count_total_users_in_ranking(
        self,
        category: Optional[str],
        from_date: Optional[datetime]
    ) -> int:
        """
        Conta o número total de usuários no ranking.

        Args:
            category: Categoria específica ou None para total
            from_date: Data de início ou None para todos os tempos

        Returns:
            Número total de usuários
        """
        if from_date is None:
            # Todos os tempos
            if category:
                # Categoria específica
                return self.db.query(UserPoint).filter(
                    UserPoint.category == category
                ).distinct(UserPoint.user_id).count()
            else:
                # Total de todas as categorias
                return self.db.query(UserPoint.user_id).distinct().count()
        else:
            # Período específico
            query = self.db.query(PointHistory.user_id).filter(
                PointHistory.created_at >= from_date
            )

            # Adicionar filtro de categoria se necessário
            if category:
                query = query.filter(PointHistory.category == category)

            return query.distinct().count()

    async def _get_users_around_points(
        self,
        points: int,
        higher: bool,
        limit: int,
        category: Optional[str],
        from_date: Optional[datetime],
        exclude_user_id: Optional[str] = None
    ) -> List[LeaderboardEntryResponse]:
        """
        Obtém usuários com pontuação próxima a um valor específico.

        Args:
            points: Valor de pontos de referência
            higher: Se True, obtém usuários com mais pontos; se False, com menos
            limit: Número máximo de usuários a retornar
            category: Categoria específica ou None para total
            from_date: Data de início ou None para todos os tempos
            exclude_user_id: ID de usuário a excluir dos resultados

        Returns:
            Lista de entradas do ranking
        """
        if from_date is None:
            # Todos os tempos
            if category:
                # Categoria específica
                query = self.db.query(
                    UserPoint.user_id,
                    UserPoint.amount
                ).filter(
                    UserPoint.category == category
                )

                # Comparação baseada em higher
                if higher:
                    query = query.filter(UserPoint.amount > points)
                    query = query.order_by(asc(UserPoint.amount))
                else:
                    query = query.filter(UserPoint.amount < points)
                    query = query.order_by(desc(UserPoint.amount))
            else:
                # Total de todas as categorias
                subquery = self.db.query(
                    UserPoint.user_id,
                    func.sum(UserPoint.amount).label("total_points")
                ).group_by(
                    UserPoint.user_id
                ).subquery()

                query = self.db.query(
                    subquery.c.user_id,
                    subquery.c.total_points
                )

                # Comparação baseada em higher
                if higher:
                    query = query.filter(subquery.c.total_points > points)
                    query = query.order_by(asc(subquery.c.total_points))
                else:
                    query = query.filter(subquery.c.total_points < points)
                    query = query.order_by(desc(subquery.c.total_points))
        else:
            # Período específico
            base_query = self.db.query(
                PointHistory.user_id,
                func.sum(PointHistory.amount).label("period_points")
            ).filter(
                PointHistory.created_at >= from_date
            )

            # Adicionar filtro de categoria se necessário
            if category:
                base_query = base_query.filter(
                    PointHistory.category == category)

            # Agrupar por usuário
            subquery = base_query.group_by(
                PointHistory.user_id
            ).subquery()

            query = self.db.query(
                subquery.c.user_id,
                subquery.c.period_points
            )

            # Comparação baseada em higher
            if higher:
                query = query.filter(subquery.c.period_points > points)
                query = query.order_by(asc(subquery.c.period_points))
            else:
                query = query.filter(subquery.c.period_points < points)
                query = query.order_by(desc(subquery.c.period_points))

        # Excluir usuário específico se necessário
        if exclude_user_id:
            if category:
                query = query.filter(UserPoint.user_id != exclude_user_id)
            else:
                query = query.filter(subquery.c.user_id != exclude_user_id)

        # Aplicar limite
        query = query.limit(limit)

        # Executar a consulta
        results = query.all()

        # Criar entradas (rank será ajustado depois)
        entries = []
        for user_id, user_points in results:
            # Calcular ranking (temporário, será ajustado depois)
            if higher:
                rank = await self._count_users_ahead(exclude_user_id, category, from_date, points) + 1
            else:
                rank = await self._count_users_ahead(user_id, category, from_date, user_points) + 1

            entries.append(LeaderboardEntryResponse(
                rank=rank,
                user_id=user_id,
                points=user_points,
                is_current_user=False
            ))

        return entries
