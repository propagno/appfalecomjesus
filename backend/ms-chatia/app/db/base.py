from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

# Obter configurações
settings = get_settings()

# Criar engine do SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Criar classe de sessão para injeção de dependência
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar classe base para modelos declarativos
Base = declarative_base()


# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
