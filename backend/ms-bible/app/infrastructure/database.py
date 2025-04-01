from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Obter a URL do banco de dados das variáveis de ambiente ou usar valor padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db-bible:5432/bibleia")

# Criar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Configurar a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para modelos ORM
Base = declarative_base()

# Função para criar conexão com o banco de dados


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para inicializar o banco de dados (criar tabelas, etc.)


def init_db():
    try:
        # Importar modelos para garantir que sejam registrados
        from app.models import bible_models

        # Criar tabelas
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {str(e)}")
        # Não lançar exceção para permitir que o serviço continue funcionando
        # mesmo se o banco não estiver disponível
