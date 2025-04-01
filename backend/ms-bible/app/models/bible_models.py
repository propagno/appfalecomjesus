from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class Book(Base):
    __tablename__ = "bible_books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    testament = Column(String(50))  # "Antigo" ou "Novo"

    # Relacionamento com capítulos
    chapters = relationship(
        "Chapter", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, name='{self.name}', testament='{self.testament}')>"


class Chapter(Base):
    __tablename__ = "bible_chapters"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("bible_books.id"))
    number = Column(Integer)  # Número do capítulo

    # Relacionamentos
    book = relationship("Book", back_populates="chapters")
    verses = relationship("Verse", back_populates="chapter",
                          cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter(id={self.id}, book_id={self.book_id}, number={self.number})>"


class Verse(Base):
    __tablename__ = "bible_verses"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("bible_chapters.id"))
    number = Column(Integer)  # Número do versículo
    text = Column(Text)  # Texto do versículo

    # Relacionamento
    chapter = relationship("Chapter", back_populates="verses")

    def __repr__(self):
        return f"<Verse(id={self.id}, chapter_id={self.chapter_id}, number={self.number})>"
