from fastapi import APIRouter
from .routes import books, chapters, verses, search, random_verse, verse_of_day

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(
    chapters.router, prefix="/chapters", tags=["chapters"])
api_router.include_router(verses.router, prefix="/verses", tags=["verses"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(
    random_verse.router, prefix="/random-verse", tags=["random-verse"])
api_router.include_router(
    verse_of_day.router, prefix="/verse-of-day", tags=["verse-of-day"])
