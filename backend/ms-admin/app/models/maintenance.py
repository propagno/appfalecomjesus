from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
import uuid
from ..db.session import Base


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # pending, in_progress, completed, failed
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String, nullable=False)
    assigned_to = Column(String, nullable=True)
    scheduled_for = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    is_automatic = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high, critical
    # backup, data_cleanup, index_rebuild, etc.
    task_type = Column(String, nullable=False)
