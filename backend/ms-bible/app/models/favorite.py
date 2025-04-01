from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # ID do usuário do MS-Auth
    verse_id = Column(Integer, ForeignKey("verses.id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento
    verse = relationship("Verse")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, verse_id={self.verse_id})>"
