from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    testament = Column(String)  # "old" ou "new"
    position = Column(Integer)  # Ordem do livro na Bíblia
    abbreviation = Column(String)

    # Relacionamento com capítulos
    chapters = relationship(
        "Chapter", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}, testament={self.testament})>"
