import uuid
import string
import random
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, join
from sqlalchemy.orm import joinedload

from app.models.certificate import Certificate
from app.models.study_plan import StudyPlan


class CertificateRepository:
    """
    Repositório para operações de banco de dados relacionadas a certificados.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, certificate_data: Dict[str, Any]) -> Certificate:
        """
        Cria um novo certificado no banco de dados.

        Args:
            certificate_data: Dicionário contendo os dados do certificado.

        Returns:
            Instância do certificado criado.
        """
        # Gerar um código único para o certificado, se não foi fornecido
        if "certificate_code" not in certificate_data:
            certificate_data["certificate_code"] = self._generate_certificate_code()

        certificate = Certificate(**certificate_data)
        self.db.add(certificate)
        await self.db.commit()
        await self.db.refresh(certificate)
        return certificate

    def _generate_certificate_code(self, length=12) -> str:
        """
        Gera um código único para o certificado.

        Args:
            length: Tamanho do código a ser gerado (padrão: 12 caracteres)

        Returns:
            String contendo código alfanumérico único.
        """
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    async def get_by_id(self, certificate_id: uuid.UUID) -> Optional[Tuple[Certificate, StudyPlan]]:
        """
        Busca um certificado pelo ID e retorna junto com o plano de estudo associado.

        Args:
            certificate_id: ID do certificado a ser buscado.

        Returns:
            Tupla com certificado e plano de estudo ou None se não encontrado.
        """
        query = select(Certificate, StudyPlan).join(
            StudyPlan, Certificate.study_plan_id == StudyPlan.id
        ).where(Certificate.id == certificate_id)

        result = await self.db.execute(query)
        row = result.first()

        if row:
            return row
        return None

    async def get_by_code(self, certificate_code: str) -> Optional[Tuple[Certificate, StudyPlan]]:
        """
        Busca um certificado pelo código único e retorna junto com o plano de estudo associado.

        Args:
            certificate_code: Código único do certificado.

        Returns:
            Tupla com certificado e plano de estudo ou None se não encontrado.
        """
        query = select(Certificate, StudyPlan).join(
            StudyPlan, Certificate.study_plan_id == StudyPlan.id
        ).where(Certificate.certificate_code == certificate_code)

        result = await self.db.execute(query)
        row = result.first()

        if row:
            return row
        return None

    async def get_all_by_user_id(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Tuple[Certificate, StudyPlan]]:
        """
        Busca todos os certificados de um usuário com paginação.

        Args:
            user_id: ID do usuário.
            skip: Número de registros para pular (paginação).
            limit: Número máximo de registros para retornar.

        Returns:
            Lista de tuplas com certificados e planos de estudo.
        """
        query = select(Certificate, StudyPlan).join(
            StudyPlan, Certificate.study_plan_id == StudyPlan.id
        ).where(Certificate.user_id == user_id).offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.all())

    async def get_for_study_plan(
        self, user_id: uuid.UUID, study_plan_id: uuid.UUID
    ) -> Optional[Certificate]:
        """
        Verifica se já existe um certificado para um plano de estudo específico.

        Args:
            user_id: ID do usuário.
            study_plan_id: ID do plano de estudo.

        Returns:
            Certificado existente ou None.
        """
        query = select(Certificate).where(
            Certificate.user_id == user_id,
            Certificate.study_plan_id == study_plan_id
        )

        result = await self.db.execute(query)
        row = result.scalar_one_or_none()
        return row

    async def increment_download_count(self, certificate_id: uuid.UUID) -> Certificate:
        """
        Incrementa o contador de downloads do certificado.

        Args:
            certificate_id: ID do certificado.

        Returns:
            Certificado atualizado.
        """
        query = select(Certificate).where(Certificate.id == certificate_id)
        result = await self.db.execute(query)
        certificate = result.scalar_one_or_none()

        if certificate:
            certificate.download_count += 1
            await self.db.commit()
            await self.db.refresh(certificate)

        return certificate

    async def update(self, certificate: Certificate) -> Certificate:
        """
        Atualiza um certificado existente.

        Args:
            certificate: Instância do certificado com as alterações.

        Returns:
            Certificado atualizado.
        """
        self.db.add(certificate)
        await self.db.commit()
        await self.db.refresh(certificate)
        return certificate

    async def get_by_user_id(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Certificate]:
        """
        Obtém todos os certificados de um usuário.

        Args:
            user_id: ID do usuário
            skip: Quantidade de itens para pular (paginação)
            limit: Quantidade máxima de itens a retornar

        Returns:
            List[Certificate]: Lista de certificados do usuário
        """
        query = (
            select(Certificate)
            .options(joinedload(Certificate.study_plan))
            .where(Certificate.user_id == user_id)
            .order_by(Certificate.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_by_user_id(self, user_id: uuid.UUID) -> int:
        """
        Conta o número total de certificados de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            int: Quantidade de certificados
        """
        query = (
            select(func.count())
            .select_from(Certificate)
            .where(Certificate.user_id == user_id)
        )

        result = await self.db.execute(query)
        return result.scalar_one()

    async def update_image_url(self, certificate_id: uuid.UUID, image_url: str) -> Optional[Certificate]:
        """
        Atualiza a URL da imagem do certificado.

        Args:
            certificate_id: ID do certificado
            image_url: URL da imagem

        Returns:
            Optional[Certificate]: O certificado atualizado ou None
        """
        stmt = (
            update(Certificate)
            .where(Certificate.id == certificate_id)
            .values(image_url=image_url)
            .returning(Certificate)
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        return result.scalar_one_or_none()

    async def increment_shared_count(self, certificate_id: uuid.UUID) -> Optional[Certificate]:
        """
        Incrementa o contador de compartilhamentos do certificado.

        Args:
            certificate_id: ID do certificado

        Returns:
            Optional[Certificate]: O certificado atualizado ou None
        """
        stmt = (
            update(Certificate)
            .where(Certificate.id == certificate_id)
            .values(shared_count=Certificate.shared_count + 1)
            .returning(Certificate)
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        return result.scalar_one_or_none()

    async def check_if_exists(self, user_id: uuid.UUID, study_plan_id: uuid.UUID) -> bool:
        """
        Verifica se já existe um certificado para o usuário e plano de estudo.

        Args:
            user_id: ID do usuário
            study_plan_id: ID do plano de estudo

        Returns:
            bool: True se existir, False caso contrário
        """
        query = (
            select(Certificate)
            .where(Certificate.user_id == user_id)
            .where(Certificate.study_plan_id == study_plan_id)
        )

        result = await self.db.execute(query)
        return result.first() is not None
