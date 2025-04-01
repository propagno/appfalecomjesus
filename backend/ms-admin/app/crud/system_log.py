from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.system_log import SystemLog
from ..schemas.system_log import SystemLogCreate, SystemLogUpdate


def get_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    source: Optional[str] = None,
    user_id: Optional[str] = None,
    resolved: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[SystemLog]:
    """
    Recupera logs do sistema com opções de filtro.
    """
    query = db.query(SystemLog)

    if level:
        query = query.filter(SystemLog.level == level)
    if source:
        query = query.filter(SystemLog.source == source)
    if user_id:
        query = query.filter(SystemLog.user_id == user_id)
    if resolved is not None:
        query = query.filter(SystemLog.resolved == resolved)
    if start_date:
        query = query.filter(SystemLog.timestamp >= start_date)
    if end_date:
        query = query.filter(SystemLog.timestamp <= end_date)

    return query.order_by(desc(SystemLog.timestamp)).offset(skip).limit(limit).all()


def get_log_by_id(db: Session, log_id: str) -> Optional[SystemLog]:
    """
    Recupera um log pelo ID.
    """
    return db.query(SystemLog).filter(SystemLog.id == log_id).first()


def create_log(db: Session, log: SystemLogCreate) -> SystemLog:
    """
    Cria um novo log no sistema.
    """
    db_log = SystemLog(
        id=str(uuid.uuid4()),
        level=log.level,
        source=log.source,
        message=log.message,
        details=log.details,
        user_id=log.user_id,
        resolved=False
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_log_resolution(db: Session, log_id: str, update_data: SystemLogUpdate, user_id: str) -> Optional[SystemLog]:
    """
    Atualiza a resolução de um log.
    """
    db_log = get_log_by_id(db, log_id)
    if not db_log:
        return None

    # Atualizar os campos
    db_log.resolved = update_data.resolved

    if update_data.resolved:
        db_log.resolved_by = user_id
        db_log.resolved_at = datetime.now()

    if update_data.resolution_notes:
        db_log.resolution_notes = update_data.resolution_notes

    db.commit()
    db.refresh(db_log)
    return db_log


def count_logs(
    db: Session,
    level: Optional[str] = None,
    source: Optional[str] = None,
    user_id: Optional[str] = None,
    resolved: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> int:
    """
    Conta o número total de logs com base nos filtros.
    """
    query = db.query(SystemLog)

    if level:
        query = query.filter(SystemLog.level == level)
    if source:
        query = query.filter(SystemLog.source == source)
    if user_id:
        query = query.filter(SystemLog.user_id == user_id)
    if resolved is not None:
        query = query.filter(SystemLog.resolved == resolved)
    if start_date:
        query = query.filter(SystemLog.timestamp >= start_date)
    if end_date:
        query = query.filter(SystemLog.timestamp <= end_date)

    return query.count()


def get_log_statistics(db: Session) -> Dict[str, Any]:
    """
    Retorna estatísticas sobre os logs do sistema.
    """
    total = db.query(SystemLog).count()
    unresolved = db.query(SystemLog).filter(
        SystemLog.resolved == False).count()
    error_count = db.query(SystemLog).filter(
        SystemLog.level == "error").count()
    critical_count = db.query(SystemLog).filter(
        SystemLog.level == "critical").count()

    sources = db.query(SystemLog.source, db.func.count(SystemLog.id))\
        .group_by(SystemLog.source)\
        .all()

    return {
        "total": total,
        "unresolved": unresolved,
        "error_count": error_count,
        "critical_count": critical_count,
        "by_source": {source: count for source, count in sources}
    }
