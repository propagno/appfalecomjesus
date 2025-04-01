"""
Serviço de banco de dados do sistema FaleComJesus.

Este módulo implementa o sistema de banco de dados da aplicação,
incluindo conexão, pool, sessões e transações.

Features:
    - Conexão PostgreSQL
    - Pool de conexões
    - Migrações
    - Sessões
    - Transações
    - Logging
"""

from typing import Any, Dict, List, Optional, Union
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from .config import settings
from .logger import logger


class DatabaseManager:
    """
    Gerenciador de banco de dados.

    Features:
        - Engine SQLAlchemy
        - Pool de conexões
        - Sessões
        - Transações
        - Migrações

    Attributes:
        engine: Engine SQLAlchemy
        session_factory: Factory de sessões
        pool: Pool de conexões
    """

    def __init__(
        self,
        database_url: Optional[str] = None,
        pool_size: int = 5,
        max_overflow: int = 10
    ):
        """
        Inicializa o gerenciador.

        Args:
            database_url: URL do banco
            pool_size: Tamanho do pool
            max_overflow: Overflow máximo
        """
        # URL do banco
        self.database_url = database_url or settings.database_url

        # Engine
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            pool_recycle=3600
        )

        # Factory de sessões
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )

        # Pool
        self.pool = self.engine.pool

    async def get_session(self) -> Session:
        """
        Obtém uma sessão do pool.

        Returns:
            Session: Sessão SQLAlchemy
        """
        try:
            return self.session_factory()

        except Exception as e:
            logger.error(f"Erro ao obter sessão: {str(e)}")
            raise

    async def execute(
        self,
        query: str,
        params: Optional[Dict] = None
    ) -> Any:
        """
        Executa uma query.

        Args:
            query: Query SQL
            params: Parâmetros da query

        Returns:
            Any: Resultado da query
        """
        try:
            async with self.get_session() as session:
                result = await session.execute(query, params or {})
                await session.commit()
                return result

        except Exception as e:
            logger.error(f"Erro ao executar query: {str(e)}")
            raise

    async def execute_many(
        self,
        query: str,
        params: List[Dict]
    ) -> Any:
        """
        Executa múltiplas queries.

        Args:
            query: Query SQL
            params: Lista de parâmetros

        Returns:
            Any: Resultado das queries
        """
        try:
            async with self.get_session() as session:
                result = await session.execute_many(query, params)
                await session.commit()
                return result

        except Exception as e:
            logger.error(f"Erro ao executar queries: {str(e)}")
            raise

    async def begin_transaction(self) -> Session:
        """
        Inicia uma transação.

        Returns:
            Session: Sessão da transação
        """
        try:
            session = self.session_factory()
            await session.begin()
            return session

        except Exception as e:
            logger.error(f"Erro ao iniciar transação: {str(e)}")
            raise

    async def commit_transaction(
        self,
        session: Session
    ) -> None:
        """
        Commit de uma transação.

        Args:
            session: Sessão da transação
        """
        try:
            await session.commit()

        except Exception as e:
            logger.error(f"Erro ao commitar transação: {str(e)}")
            raise

    async def rollback_transaction(
        self,
        session: Session
    ) -> None:
        """
        Rollback de uma transação.

        Args:
            session: Sessão da transação
        """
        try:
            await session.rollback()

        except Exception as e:
            logger.error(f"Erro ao fazer rollback: {str(e)}")
            raise

    async def check_connection(self) -> bool:
        """
        Verifica conexão com o banco.

        Returns:
            bool: True se conectado
        """
        try:
            async with self.get_session() as session:
                await session.execute("SELECT 1")
                return True

        except Exception as e:
            logger.error(f"Erro ao verificar conexão: {str(e)}")
            return False

    def get_pool_status(self) -> Dict:
        """
        Retorna status do pool.

        Returns:
            Dict: Status do pool
        """
        try:
            return {
                "size": self.pool.size(),
                "checkedin": self.pool.checkedin(),
                "checkedout": self.pool.checkedout(),
                "overflow": self.pool.overflow(),
                "checkedout_timeout": self.pool.checkedout_timeout()
            }

        except Exception as e:
            logger.error(f"Erro ao obter status do pool: {str(e)}")
            return {}

    async def close(self) -> None:
        """
        Fecha conexões.
        """
        try:
            await self.engine.dispose()

        except Exception as e:
            logger.error(f"Erro ao fechar banco: {str(e)}")


# Instância global de banco
db = DatabaseManager()
