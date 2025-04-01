"""
Serviço de certificados do sistema FaleComJesus.

Este módulo implementa a geração e gerenciamento de certificados
digitais para usuários que completam planos de estudo.

Features:
    - Geração de PDF
    - Templates personalizáveis
    - QR Code de validação
    - Compartilhamento social
    - Histórico de certificados
    - Validação online
"""

from typing import Dict, List, Optional, Union
import logging
import qrcode
import pdfkit
import json
from datetime import datetime, timedelta
from pathlib import Path
from .config import settings
from .cache import cache
from .metrics import metrics
from .email import email

# Logger
logger = logging.getLogger(__name__)


class CertificateManager:
    """
    Gerenciador de certificados digitais.

    Features:
        - Geração de PDF
        - Templates HTML
        - QR Code
        - Compartilhamento
        - Validação

    Attributes:
        template_dir: Diretório de templates
        output_dir: Diretório de saída
        metrics: Métricas de certificados
    """

    def __init__(
        self,
        template_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        wkhtmltopdf_path: Optional[str] = None
    ):
        """
        Inicializa o gerenciador de certificados.

        Args:
            template_dir: Diretório de templates
            output_dir: Diretório de saída
            wkhtmltopdf_path: Caminho do wkhtmltopdf
        """
        # Diretórios
        self.template_dir = Path(template_dir or settings.CERT_TEMPLATE_DIR)
        self.output_dir = Path(output_dir or settings.CERT_OUTPUT_DIR)

        # Configuração PDF
        self.pdf_config = {
            "wkhtmltopdf": wkhtmltopdf_path or settings.WKHTMLTOPDF_PATH,
            "page-size": "A4",
            "margin-top": "0mm",
            "margin-right": "0mm",
            "margin-bottom": "0mm",
            "margin-left": "0mm"
        }

        logger.info("Gerenciador de certificados inicializado")

    async def generate_certificate(
        self,
        user_id: str,
        user_name: str,
        plan_name: str,
        completion_date: datetime,
        certificate_id: str,
        template_name: str = "default.html"
    ) -> Dict:
        """
        Gera certificado digital.

        Args:
            user_id: ID do usuário
            user_name: Nome do usuário
            plan_name: Nome do plano
            completion_date: Data de conclusão
            certificate_id: ID do certificado
            template_name: Nome do template

        Returns:
            Dict: Dados do certificado

        Example:
            cert = await certificates.generate_certificate(
                user_id="123",
                user_name="João Silva",
                plan_name="Paz Interior",
                completion_date=datetime.now(),
                certificate_id="CERT-123"
            )
        """
        try:
            # Gera QR Code
            qr_data = await self._generate_qr_code(certificate_id)

            # Renderiza template
            html = await self._render_template(
                template_name,
                {
                    "user_name": user_name,
                    "plan_name": plan_name,
                    "completion_date": completion_date.strftime("%d/%m/%Y"),
                    "certificate_id": certificate_id,
                    "qr_code": qr_data
                }
            )

            # Gera PDF
            pdf_path = await self._generate_pdf(
                html,
                certificate_id
            )

            # Salva no banco
            await self._save_to_db(
                user_id,
                certificate_id,
                plan_name,
                completion_date,
                pdf_path
            )

            # Registra métricas
            metrics.track_certificate(
                "certificate_generated",
                plan_name=plan_name
            )

            return {
                "id": certificate_id,
                "pdf_url": f"/certificates/{certificate_id}.pdf",
                "qr_code": qr_data
            }

        except Exception as e:
            logger.error(f"Erro ao gerar certificado: {str(e)}")
            raise

    async def validate_certificate(
        self,
        certificate_id: str
    ) -> Dict:
        """
        Valida certificado digital.

        Args:
            certificate_id: ID do certificado

        Returns:
            Dict: Dados de validação
        """
        try:
            # Busca no banco
            cert = await self._get_from_db(certificate_id)

            if not cert:
                return {
                    "valid": False,
                    "message": "Certificado não encontrado"
                }

            # Verifica data
            if cert["expires_at"] < datetime.now():
                return {
                    "valid": False,
                    "message": "Certificado expirado"
                }

            return {
                "valid": True,
                "user_name": cert["user_name"],
                "plan_name": cert["plan_name"],
                "completion_date": cert["completion_date"],
                "issued_at": cert["issued_at"]
            }

        except Exception as e:
            logger.error(f"Erro ao validar certificado: {str(e)}")
            return {
                "valid": False,
                "message": "Erro na validação"
            }

    async def share_certificate(
        self,
        certificate_id: str,
        platform: str,
        user_id: str
    ) -> bool:
        """
        Compartilha certificado em rede social.

        Args:
            certificate_id: ID do certificado
            platform: Plataforma (facebook, twitter, etc)
            user_id: ID do usuário

        Returns:
            bool: True se compartilhado
        """
        try:
            # Gera URL de compartilhamento
            share_url = await self._generate_share_url(
                certificate_id,
                platform
            )

            # Registra compartilhamento
            await self._save_share(
                certificate_id,
                platform,
                user_id
            )

            # Registra métricas
            metrics.track_certificate(
                "certificate_shared",
                platform=platform
            )

            return True

        except Exception as e:
            logger.error(f"Erro ao compartilhar certificado: {str(e)}")
            return False

    async def _generate_qr_code(
        self,
        certificate_id: str
    ) -> str:
        """
        Gera QR Code para validação.

        Args:
            certificate_id: ID do certificado

        Returns:
            str: Base64 do QR Code
        """
        try:
            # URL de validação
            validate_url = f"{settings.APP_URL}/certificates/validate/{certificate_id}"

            # Gera QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )

            qr.add_data(validate_url)
            qr.make(fit=True)

            # Converte para base64
            img = qr.make_image(fill_color="black", back_color="white")
            return img.get_image_base64()

        except Exception as e:
            logger.error(f"Erro ao gerar QR Code: {str(e)}")
            return ""

    async def _render_template(
        self,
        template_name: str,
        data: Dict
    ) -> str:
        """
        Renderiza template HTML.

        Args:
            template_name: Nome do template
            data: Dados para renderização

        Returns:
            str: HTML renderizado
        """
        try:
            # Carrega template
            template_path = self.template_dir / template_name
            with open(template_path) as f:
                template = f.read()

            # Substitui variáveis
            for key, value in data.items():
                template = template.replace(
                    f"{{{{ {key} }}}}",
                    str(value)
                )

            return template

        except Exception as e:
            logger.error(f"Erro ao renderizar template: {str(e)}")
            raise

    async def _generate_pdf(
        self,
        html: str,
        certificate_id: str
    ) -> str:
        """
        Gera PDF do certificado.

        Args:
            html: HTML renderizado
            certificate_id: ID do certificado

        Returns:
            str: Caminho do PDF
        """
        try:
            # Configura PDF
            options = {
                "page-size": self.pdf_config["page-size"],
                "margin-top": self.pdf_config["margin-top"],
                "margin-right": self.pdf_config["margin-right"],
                "margin-bottom": self.pdf_config["margin-bottom"],
                "margin-left": self.pdf_config["margin-left"]
            }

            # Gera PDF
            output_path = self.output_dir / f"{certificate_id}.pdf"
            pdfkit.from_string(
                html,
                str(output_path),
                options=options,
                configuration=pdfkit.configuration(
                    wkhtmltopdf=self.pdf_config["wkhtmltopdf"]
                )
            )

            return str(output_path)

        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {str(e)}")
            raise

    async def _generate_share_url(
        self,
        certificate_id: str,
        platform: str
    ) -> str:
        """
        Gera URL de compartilhamento.

        Args:
            certificate_id: ID do certificado
            platform: Plataforma

        Returns:
            str: URL de compartilhamento
        """
        try:
            # URL base
            base_url = f"{settings.APP_URL}/certificates/{certificate_id}"

            # Parâmetros por plataforma
            params = {
                "facebook": {
                    "u": base_url,
                    "t": "Conquistei meu certificado no FaleComJesus!"
                },
                "twitter": {
                    "url": base_url,
                    "text": "Conquistei meu certificado no FaleComJesus!"
                },
                "whatsapp": {
                    "text": f"Conquistei meu certificado no FaleComJesus! {base_url}"
                }
            }

            # Gera URL
            if platform in params:
                return f"{settings.SHARE_URLS[platform]}?{urlencode(params[platform])}"
            else:
                return base_url

        except Exception as e:
            logger.error(f"Erro ao gerar URL: {str(e)}")
            return ""


# Instância global de certificados
certificates = CertificateManager()
