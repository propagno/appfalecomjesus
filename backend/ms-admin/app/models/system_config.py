from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
import uuid
from ..db.session import Base


class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(String, primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    key = Column(String, nullable=False, unique=True, index=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    is_sensitive = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=False)
    # system, email, limits, payment, etc.
    category = Column(String, nullable=True)
