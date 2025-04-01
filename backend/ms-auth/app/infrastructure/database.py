from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings

settings = get_settings()

# Create sync engine
engine = create_engine(
    # Convertendo para string para evitar erros com o objeto URL
    str(settings.database_url),
    echo=settings.debug,
    future=True,
)

# Create sync session factory
session_factory = sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create base class for declarative models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function that yields db sessions.
    """
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
