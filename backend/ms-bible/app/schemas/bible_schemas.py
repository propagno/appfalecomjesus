from typing import List, Optional
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    name: str
    testament: str


class BookCreate(BookBase):
    pass


class BookSchema(BookBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Gênesis",
                "testament": "Antigo"
            }
        }


class ChapterBase(BaseModel):
    book_id: int
    number: int


class ChapterCreate(ChapterBase):
    pass


class ChapterSchema(ChapterBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "book_id": 1,
                "number": 1
            }
        }


class VerseBase(BaseModel):
    chapter_id: int
    number: int
    text: str


class VerseCreate(VerseBase):
    pass


class VerseSchema(VerseBase):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "chapter_id": 1,
                "number": 1,
                "text": "No princípio, Deus criou os céus e a terra."
            }
        }


class SearchResponseSchema(BaseModel):
    verses: List[VerseSchema]
    count: int

    class Config:
        schema_extra = {
            "example": {
                "verses": [
                    {
                        "id": 1,
                        "chapter_id": 1,
                        "number": 1,
                        "text": "No princípio, Deus criou os céus e a terra."
                    }
                ],
                "count": 1
            }
        }
