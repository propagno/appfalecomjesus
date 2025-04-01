from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class Testament(str, Enum):
    ""Enum for Bible testaments.""
    OLD = "old"
    NEW = "new"

class BookBase(BaseModel):
    ""Base schema for Bible book.""
    name: str
    abbreviation: str
    testament: Testament
    position: int

class BookCreate(BookBase):
    ""Schema for creating a Bible book.""
    chapters_count: int = 0

class Book(BookBase):
    ""Schema for a Bible book.""
    id: int
    chapters_count: int

class ChapterBase(BaseModel):
    ""Base schema for a Bible chapter.""
    book_id: int
    number: int

class ChapterCreate(ChapterBase):
    ""Schema for creating a Bible chapter.""
    verses_count: int = 0

class Chapter(ChapterBase):
    ""Schema for a Bible chapter.""
    id: int
    verses_count: int
