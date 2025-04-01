from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    number = Column(Integer)

    # Relacionamentos
    book = relationship("Book", back_populates="chapters")
    verses = relationship("Verse", back_populates="chapter",
                          cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter(id={self.id}, book_id={self.book_id}, number={self.number})>"
