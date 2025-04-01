from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import Book, BooksResponse, ChaptersResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=BooksResponse)
async def get_books(
    testament: Optional[str] = Query(
        None, description="Filter by testament ('old' or 'new')"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get a list of all Bible books.

    This endpoint returns all books in the Bible, optionally filtered by testament.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_books(testament=testament)


@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: int = Path(..., description="The ID of the book to retrieve"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get detailed information about a specific Bible book.

    This endpoint returns information about a book, including its name, testament, and number of chapters.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_book(book_id)


@router.get("/{book_id}/chapters", response_model=ChaptersResponse)
async def get_book_chapters(
    book_id: int = Path(...,
                        description="The ID of the book to retrieve chapters for"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get all chapters for a specific Bible book.

    This endpoint returns a list of all chapters in a book.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_chapters(book_id)
