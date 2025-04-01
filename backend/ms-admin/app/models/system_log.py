from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
import uuid
from ..db.session import Base


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    level = Column(String, nullable=False)  # info, warning, error, critical
    # service name (ms-auth, ms-study, etc)
    source = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    user_id = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True),
                       server_default=func.now(), index=True)
    resolved = Column(Boolean, default=False)
    resolved_by = Column(String, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
