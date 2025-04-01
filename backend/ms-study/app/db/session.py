from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Verificar se a URI é uma string válida
db_uri = settings.SQLALCHEMY_DATABASE_URI
if not isinstance(db_uri, str):
    # Montar manualmente se não for string
    db_uri = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Cria a engine do SQLAlchemy apontando para a URL do banco de dados
engine = create_engine(db_uri)

# Cria a classe de sessão que será usada para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos de dados
Base = declarative_base()

# Dependência para obter sessão do banco de dados


def get_db() -> Generator[Session, None, None]:
    """
    Função para obter uma sessão do banco de dados.
    Yield: SQLAlchemy Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
