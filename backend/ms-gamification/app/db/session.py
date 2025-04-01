from typing import Generator
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Usar diretamente a variável de ambiente, que contém o nome do serviço Docker correto
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@gamification-db:5432/gamification_db"
)

# Criar engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()

# Tabelas existentes


def get_tables() -> list:
    """
    Retorna lista de tabelas existentes.
    """
    inspector = inspect(engine)
    return inspector.get_table_names()


def get_db() -> Generator:
    """
    Obtém conexão com o banco de dados.

    Yields:
        db: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
