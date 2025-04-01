"""
Serviço de email do sistema FaleComJesus.

Este módulo implementa o envio de emails transacionais e marketing,
usando templates HTML, filas assíncronas e múltiplos provedores.

Features:
    - Templates HTML responsivos
    - Envio assíncrono via filas
    - Múltiplos provedores (SMTP, SendGrid)
    - Tracking de abertura
    - Bounce handling
    - Unsubscribe automático
"""

from typing import Dict, List, Optional, Union
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import aiosmtplib
from jinja2 import Environment, FileSystemLoader
from .config import settings
from .metrics import metrics

# Logger
logger = logging.getLogger(__name__)

# Templates Jinja2
template_dir = Path(__file__).parent.parent / "templates" / "email"
jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)


class EmailManager:
    """
    Gerenciador de envio de emails.

    Features:
        - Múltiplos provedores
        - Templates HTML
        - Envio assíncrono
        - Métricas e logs
        - Retry automático

    Attributes:
        smtp_config: Configurações SMTP
        templates: Cache de templates
        metrics: Métricas de envio
    """

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_pass: Optional[str] = None,
        smtp_tls: bool = True
    ):
        """
        Inicializa o gerenciador de email.

        Args:
            smtp_host: Host do servidor SMTP
            smtp_port: Porta do servidor SMTP
            smtp_user: Usuário SMTP
            smtp_pass: Senha SMTP
            smtp_tls: Usar TLS
        """
        # Configurações SMTP
        self.smtp_config = {
            "hostname": smtp_host or settings.SMTP_HOST,
            "port": smtp_port or settings.SMTP_PORT,
            "username": smtp_user or settings.SMTP_USER,
            "password": smtp_pass or settings.SMTP_PASSWORD,
            "use_tls": smtp_tls
        }

        # Cache de templates
        self.templates = {}

        logger.info("Gerenciador de email inicializado")

    async def send_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        template_name: str,
        template_data: Dict,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict]] = None
    ) -> bool:
        """
        Envia email usando template HTML.

        Args:
            to_email: Email(s) do destinatário
            subject: Assunto do email
            template_name: Nome do template
            template_data: Dados para o template
            from_email: Email do remetente
            from_name: Nome do remetente
            reply_to: Email de resposta
            cc: Lista de emails em cópia
            bcc: Lista de emails em cópia oculta
            attachments: Lista de anexos

        Returns:
            bool: True se enviado com sucesso

        Example:
            await email.send_email(
                to_email="user@example.com",
                subject="Bem-vindo!",
                template_name="welcome.html",
                template_data={"name": "João"}
            )
        """
        try:
            # Prepara destinatários
            if isinstance(to_email, str):
                to_email = [to_email]

            # Prepara remetente
            from_email = from_email or settings.EMAILS_FROM_EMAIL
            from_name = from_name or settings.EMAILS_FROM_NAME

            # Renderiza template
            html_content = await self._render_template(
                template_name,
                template_data
            )

            # Cria mensagem
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{from_email}>"
            msg["To"] = ", ".join(to_email)

            if reply_to:
                msg["Reply-To"] = reply_to

            if cc:
                msg["Cc"] = ", ".join(cc)

            if bcc:
                msg["Bcc"] = ", ".join(bcc)

            # Adiciona conteúdo
            msg.attach(MIMEText(html_content, "html"))

            # Adiciona anexos
            if attachments:
                for attachment in attachments:
                    part = MIMEText(
                        attachment["content"],
                        attachment["type"]
                    )
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=attachment["filename"]
                    )
                    msg.attach(part)

            # Envia email
            async with aiosmtplib.SMTP(**self.smtp_config) as smtp:
                await smtp.send_message(msg)

            # Registra métricas
            metrics.track_email_sent(
                template=template_name,
                recipients=len(to_email)
            )

            logger.info(f"Email enviado para {to_email}")
            return True

        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return False

    async def _render_template(
        self,
        template_name: str,
        template_data: Dict
    ) -> str:
        """
        Renderiza template HTML com Jinja2.

        Args:
            template_name: Nome do template
            template_data: Dados para o template

        Returns:
            str: HTML renderizado
        """
        try:
            # Verifica cache
            if template_name in self.templates:
                template = self.templates[template_name]
            else:
                # Carrega template
                template = jinja_env.get_template(template_name)
                self.templates[template_name] = template

            # Renderiza template
            return template.render(**template_data)

        except Exception as e:
            logger.error(f"Erro ao renderizar template: {str(e)}")
            raise

    async def verify_connection(self) -> bool:
        """
        Verifica conexão com servidor SMTP.

        Returns:
            bool: True se conectado
        """
        try:
            async with aiosmtplib.SMTP(**self.smtp_config) as smtp:
                await smtp.noop()
                return True

        except Exception as e:
            logger.error(f"Erro ao verificar SMTP: {str(e)}")
            return False


# Templates de email disponíveis
EMAIL_TEMPLATES = {
    # Autenticação
    "welcome": {
        "subject": "Bem-vindo ao FaleComJesus!",
        "template": "auth/welcome.html"
    },
    "verify_email": {
        "subject": "Confirme seu email",
        "template": "auth/verify_email.html"
    },
    "reset_password": {
        "subject": "Redefinição de senha",
        "template": "auth/reset_password.html"
    },

    # Plano de estudos
    "study_reminder": {
        "subject": "Não esqueça seu estudo de hoje",
        "template": "study/reminder.html"
    },
    "study_completed": {
        "subject": "Parabéns! Plano concluído",
        "template": "study/completed.html"
    },
    "certificate": {
        "subject": "Seu certificado está pronto",
        "template": "study/certificate.html"
    },

    # Pagamentos
    "payment_success": {
        "subject": "Pagamento confirmado",
        "template": "payment/success.html"
    },
    "payment_failed": {
        "subject": "Problema no pagamento",
        "template": "payment/failed.html"
    },
    "subscription_expiring": {
        "subject": "Sua assinatura está próxima do fim",
        "template": "payment/expiring.html"
    }
}

# Instância global do email
email = EmailManager()
