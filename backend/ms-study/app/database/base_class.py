from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Classe base para todos os modelos SQLAlchemy.
    Fornece o __tablename__ automático baseado no nome da classe.
    """
    id: Any
    __name__: str

    # Gera o __tablename__ automaticamente baseado no nome da classe
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
