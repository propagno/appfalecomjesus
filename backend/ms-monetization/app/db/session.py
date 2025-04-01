from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# Criar engine do SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW
)

# Criar SessionLocal do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar Base declarativa do SQLAlchemy
Base = declarative_base()

# Função para obter uma sessão do banco de dados


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
