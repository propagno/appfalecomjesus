import logging
from typing import Callable

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging
from app.core.metrics import update_system_metrics

logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable:
    """
    Cria handler de inicialização.

    Responsável por:
    - Inicializar banco
    - Configurar logging
    - Iniciar métricas
    - Validar conexões

    Args:
        app: Aplicação FastAPI

    Returns:
        Handler de inicialização
    """
    async def start_app() -> None:
        """
        Inicializa aplicação.

        Raises:
            Exception: Se erro na inicialização
        """
        try:
            # Configura logging
            setup_logging()
            logger.info("Iniciando aplicação...")

            # Inicializa banco
            init_db()
            logger.info("Banco de dados inicializado")

            # Inicia métricas
            update_system_metrics(
                cpu=0.0,
                memory=0,
                disk=0.0
            )
            logger.info("Métricas iniciadas")

            logger.info("Aplicação iniciada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao iniciar aplicação: {str(e)}")
            raise

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    Cria handler de finalização.

    Responsável por:
    - Fechar conexões
    - Salvar estado
    - Limpar recursos
    - Registrar logs

    Args:
        app: Aplicação FastAPI

    Returns:
        Handler de finalização
    """
    async def stop_app() -> None:
        """
        Finaliza aplicação.

        Raises:
            Exception: Se erro na finalização
        """
        try:
            logger.info("Finalizando aplicação...")

            # TODO: Implementar limpeza de recursos

            logger.info("Aplicação finalizada com sucesso")

        except Exception as e:
            logger.error(f"Erro ao finalizar aplicação: {str(e)}")
            raise

    return stop_app


def setup_events(app: FastAPI) -> None:
    """
    Configura eventos da aplicação.

    Args:
        app: Aplicação FastAPI
    """
    app.add_event_handler(
        "startup",
        create_start_app_handler(app)
    )

    app.add_event_handler(
        "shutdown",
        create_stop_app_handler(app)
    )
