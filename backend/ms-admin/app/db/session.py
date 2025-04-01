from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obter variáveis de ambiente
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin_user:admin_password@admin-db/admin_db")

# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar factory de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos
Base = declarative_base()

# Função para criar todas as tabelas no banco de dados


def create_tables():
    # Importar todos os modelos aqui
    from ..models.maintenance import MaintenanceTask
    from ..models.system_config import SystemConfig

    Base.metadata.create_all(bind=engine)
