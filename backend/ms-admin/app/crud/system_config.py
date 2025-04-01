from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from ..models.system_config import SystemConfig
from ..schemas.system_config import SystemConfigCreate, SystemConfigUpdate


def get_configs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    is_sensitive: Optional[bool] = None
) -> List[SystemConfig]:
    """
    Recupera configurações do sistema com opção de filtro por categoria e sensibilidade.
    """
    query = db.query(SystemConfig)

    if category:
        query = query.filter(SystemConfig.category == category)
    if is_sensitive is not None:
        query = query.filter(SystemConfig.is_sensitive == is_sensitive)

    return query.offset(skip).limit(limit).all()


def get_config_by_id(db: Session, config_id: str) -> Optional[SystemConfig]:
    """
    Recupera uma configuração pelo ID.
    """
    return db.query(SystemConfig).filter(SystemConfig.id == config_id).first()


def get_config_by_key(db: Session, key: str) -> Optional[SystemConfig]:
    """
    Recupera uma configuração pela chave.
    """
    return db.query(SystemConfig).filter(SystemConfig.key == key).first()


def create_config(db: Session, config: SystemConfigCreate, user_id: str) -> SystemConfig:
    """
    Cria uma nova configuração do sistema.
    """
    db_config = SystemConfig(
        id=str(uuid.uuid4()),
        key=config.key,
        value=config.value,
        description=config.description,
        is_sensitive=config.is_sensitive,
        category=config.category,
        updated_by=user_id
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def update_config(db: Session, config_id: str, update_data: SystemConfigUpdate, user_id: str) -> Optional[SystemConfig]:
    """
    Atualiza uma configuração do sistema.
    """
    db_config = get_config_by_id(db, config_id)
    if not db_config:
        return None

    # Atualizar os campos
    db_config.value = update_data.value

    if update_data.description is not None:
        db_config.description = update_data.description

    db_config.updated_by = user_id

    db.commit()
    db.refresh(db_config)
    return db_config


def count_configs(
    db: Session,
    category: Optional[str] = None,
    is_sensitive: Optional[bool] = None
) -> int:
    """
    Conta o número total de configurações com base nos filtros.
    """
    query = db.query(SystemConfig)

    if category:
        query = query.filter(SystemConfig.category == category)
    if is_sensitive is not None:
        query = query.filter(SystemConfig.is_sensitive == is_sensitive)

    return query.count()


def delete_config(db: Session, config_id: str) -> bool:
    """
    Remove uma configuração do sistema.
    """
    db_config = get_config_by_id(db, config_id)
    if not db_config:
        return False

    db.delete(db_config)
    db.commit()
    return True
