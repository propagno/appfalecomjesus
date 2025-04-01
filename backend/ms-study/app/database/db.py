import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# Obter a URL de conexão com o banco de dados da variável de ambiente ou usar um valor padrão
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ms_study")

# Criar o engine do SQLAlchemy com opções de conexão
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica a conexão antes de usar
    # Exibe as queries SQL se SQL_ECHO=1
    echo=os.getenv("SQL_ECHO", "0") == "1",
)

# Criar a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

# Função para obter uma instância da sessão do banco de dados


def get_db():
    """
    Função geradora que fornece uma sessão de banco de dados.
    Garante o fechamento da sessão ao final do uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas.
    Deve ser chamada no evento de startup da aplicação.
    """
    try:
        # Importar todos os modelos aqui para que o SQLAlchemy os conheça
        from app.models.study_plan import StudyPlan  # noqa
        from app.models.study_section import StudySection  # noqa
        from app.models.study_content import StudyContent  # noqa
        from app.models.user_study_progress import UserStudyProgress  # noqa
        from app.models.reflection import Reflection  # noqa
        from app.models.certificate import Certificate  # noqa

        # Criar as tabelas
        from app.database.base_class import Base
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas do banco de dados criadas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise
