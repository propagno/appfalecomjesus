from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Criação do engine do SQLAlchemy
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# Fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos
Base = declarative_base()


def init_db():
    """Inicializa o banco de dados, criando as tabelas se não existirem"""
    # Importar modelos para que sejam registrados na Base
    from app.models.user_point import UserPoint
    from app.models.point_history import PointHistory
    from app.models.achievement import Achievement
    from app.models.user_achievement import UserAchievement

    # Criar tabelas
    Base.metadata.create_all(bind=engine)
