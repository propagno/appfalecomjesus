from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Verse(Base):
    __tablename__ = 'verses'

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    number = Column(Integer)
    text = Column(Text)

    # Relacionamento
    chapter = relationship("Chapter", back_populates="verses")

    def __repr__(self):
        return f"<Verse(id={self.id}, chapter_id={self.chapter_id}, number={self.number})>"
