from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import uuid

from ..models.maintenance import MaintenanceTask
from ..schemas.maintenance import MaintenanceTaskCreate, MaintenanceTaskUpdate


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    task_type: Optional[str] = None
) -> List[MaintenanceTask]:
    """
    Recupera tarefas de manutenção com opção de filtro por status, prioridade e tipo.
    """
    query = db.query(MaintenanceTask)

    if status:
        query = query.filter(MaintenanceTask.status == status)
    if priority:
        query = query.filter(MaintenanceTask.priority == priority)
    if task_type:
        query = query.filter(MaintenanceTask.task_type == task_type)

    return query.order_by(desc(MaintenanceTask.created_at)).offset(skip).limit(limit).all()


def get_task_by_id(db: Session, task_id: str) -> Optional[MaintenanceTask]:
    """
    Recupera uma tarefa de manutenção pelo ID.
    """
    return db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()


def create_task(db: Session, task: MaintenanceTaskCreate, user_id: str) -> MaintenanceTask:
    """
    Cria uma nova tarefa de manutenção.
    """
    db_task = MaintenanceTask(
        id=str(uuid.uuid4()),
        title=task.title,
        description=task.description,
        scheduled_for=task.scheduled_for,
        assigned_to=task.assigned_to,
        is_automatic=task.is_automatic,
        priority=task.priority,
        task_type=task.task_type,
        created_by=user_id,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: str, update_data: MaintenanceTaskUpdate) -> Optional[MaintenanceTask]:
    """
    Atualiza o status de uma tarefa de manutenção.
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None

    # Atualizar os campos
    db_task.status = update_data.status

    if update_data.error_message:
        db_task.error_message = update_data.error_message

    if update_data.status == "completed":
        db_task.completed_at = update_data.completed_at or datetime.now()

    db.commit()
    db.refresh(db_task)
    return db_task


def count_tasks(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    task_type: Optional[str] = None
) -> int:
    """
    Conta o número total de tarefas de manutenção com base nos filtros.
    """
    query = db.query(MaintenanceTask)

    if status:
        query = query.filter(MaintenanceTask.status == status)
    if priority:
        query = query.filter(MaintenanceTask.priority == priority)
    if task_type:
        query = query.filter(MaintenanceTask.task_type == task_type)

    return query.count()


def delete_task(db: Session, task_id: str) -> bool:
    """
    Remove uma tarefa de manutenção.
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
