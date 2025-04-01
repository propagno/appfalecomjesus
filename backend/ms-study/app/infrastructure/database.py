from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger("database")

# Create SQLAlchemy engine and session
engine = create_engine(
    settings.DATABASE_URL,
    # Connect args for SQLite
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith(
        "sqlite") else {},
    echo=settings.DEBUG,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Create a new database session and close it when done.
    """
    db = SessionLocal()
    try:
        # Se não estiver usando SQLite, configure o schema de pesquisa
        if not settings.DATABASE_URL.startswith("sqlite"):
            db.execute(text("SET search_path TO study_schema, public"))
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    """
    try:
        # Import all models here to ensure they are registered with SQLAlchemy
        from app.domain.study.models import (
            UserPreferences,
            StudyPlan,
            StudySection,
            StudyContent,
            UserStudyProgress,
            UserReflection
        )

        # Log para depuração
        logger.info(f"Connecting to database: {settings.DATABASE_URL}")

        # Se não estiver usando SQLite, crie o schema se não existir
        if not settings.DATABASE_URL.startswith("sqlite"):
            with engine.connect() as conn:
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS study_schema"))
                conn.execute(text("SET search_path TO study_schema"))
                conn.commit()
                logger.info("Study schema created or already exists")

        # Create all tables with schema prefix for PostgreSQL
        for table in Base.metadata.tables.values():
            if not settings.DATABASE_URL.startswith("sqlite") and not table.schema:
                table.schema = "study_schema"

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
