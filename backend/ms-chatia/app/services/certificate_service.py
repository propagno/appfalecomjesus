import logging
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.study import Certificate
from app.schemas.study import CertificateCreate

logger = logging.getLogger(__name__)


class CertificateService:
    """
    Serviço para gerenciamento de certificados.

    Responsável por:
    - Gerar certificados de conclusão
    - Validar elegibilidade
    - Armazenar histórico
    - Permitir download e compartilhamento

    Attributes:
        db: Sessão do banco de dados
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de certificados.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    async def generate_certificate(
        self,
        user_id: UUID,
        plan_id: UUID,
        plan_title: str
    ) -> Dict:
        """
        Gera certificado de conclusão.

        Args:
            user_id: ID do usuário
            plan_id: ID do plano
            plan_title: Título do plano

        Returns:
            Dict com detalhes do certificado

        Raises:
            HTTPException: Se erro na geração
        """
        try:
            # Verifica se já existe
            existing = self.db.query(Certificate).filter(
                Certificate.user_id == user_id,
                Certificate.plan_id == plan_id
            ).first()

            if existing:
                return {
                    "id": existing.id,
                    "code": existing.certificate_code,
                    "plan_title": existing.plan_title,
                    "completion_date": existing.completion_date
                }

            # Gera código único
            certificate_code = str(uuid4())[:8].upper()

            # Cria certificado
            certificate = Certificate(
                user_id=user_id,
                plan_id=plan_id,
                plan_title=plan_title,
                certificate_code=certificate_code,
                completion_date=datetime.utcnow(),
                download_count=0
            )

            self.db.add(certificate)
            self.db.commit()
            self.db.refresh(certificate)

            return {
                "id": certificate.id,
                "code": certificate.certificate_code,
                "plan_title": certificate.plan_title,
                "completion_date": certificate.completion_date
            }

        except Exception as e:
            logger.error(f"Error generating certificate: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar certificado"
            )

    async def get_certificate(
        self,
        certificate_id: UUID
    ) -> Optional[Dict]:
        """
        Retorna detalhes do certificado.

        Args:
            certificate_id: ID do certificado

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            certificate = self.db.query(Certificate).filter(
                Certificate.id == certificate_id
            ).first()

            if not certificate:
                return None

            return {
                "id": certificate.id,
                "code": certificate.certificate_code,
                "plan_title": certificate.plan_title,
                "completion_date": certificate.completion_date,
                "download_count": certificate.download_count
            }

        except Exception as e:
            logger.error(f"Error getting certificate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar certificado"
            )

    async def list_certificates(
        self,
        user_id: UUID
    ) -> List[Dict]:
        """
        Lista certificados do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de certificados

        Raises:
            HTTPException: Se erro na listagem
        """
        try:
            certificates = self.db.query(Certificate).filter(
                Certificate.user_id == user_id
            ).order_by(Certificate.completion_date.desc()).all()

            return [{
                "id": c.id,
                "code": c.certificate_code,
                "plan_title": c.plan_title,
                "completion_date": c.completion_date,
                "download_count": c.download_count
            } for c in certificates]

        except Exception as e:
            logger.error(f"Error listing certificates: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar certificados"
            )

    async def validate_certificate(
        self,
        certificate_code: str
    ) -> Optional[Dict]:
        """
        Valida autenticidade do certificado.

        Args:
            certificate_code: Código do certificado

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na validação
        """
        try:
            certificate = self.db.query(Certificate).filter(
                Certificate.certificate_code == certificate_code
            ).first()

            if not certificate:
                return None

            return {
                "id": certificate.id,
                "code": certificate.certificate_code,
                "plan_title": certificate.plan_title,
                "completion_date": certificate.completion_date,
                "is_valid": True
            }

        except Exception as e:
            logger.error(f"Error validating certificate: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao validar certificado"
            )

    async def increment_download_count(
        self,
        certificate_id: UUID
    ) -> None:
        """
        Incrementa contador de downloads.

        Args:
            certificate_id: ID do certificado

        Raises:
            HTTPException: Se erro no incremento
        """
        try:
            certificate = self.db.query(Certificate).filter(
                Certificate.id == certificate_id
            ).first()

            if certificate:
                certificate.download_count += 1
                self.db.commit()

        except Exception as e:
            logger.error(f"Error incrementing downloads: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar downloads"
            )

    async def generate_certificate_text(
        self,
        certificate: Dict
    ) -> str:
        """
        Gera texto do certificado.

        Args:
            certificate: Dados do certificado

        Returns:
            Texto formatado

        Raises:
            HTTPException: Se erro na geração
        """
        try:
            completion_date = certificate["completion_date"].strftime(
                "%d/%m/%Y")

            return f"""
            CERTIFICADO DE CONCLUSÃO
            
            Certificamos que o aluno concluiu com êxito o plano de estudos
            "{certificate['plan_title']}" na plataforma FaleComJesus.
            
            Data de conclusão: {completion_date}
            Código de validação: {certificate['code']}
            
            Este certificado pode ser validado em:
            {settings.BASE_URL}/certificados/validar/{certificate['code']}
            """

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar texto do certificado"
            )
