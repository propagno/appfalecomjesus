from fastapi import APIRouter, Depends, Path, Body, HTTPException, status
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import Verse, VerseDetail
from app.api.deps import get_current_user, get_current_active_user

router = APIRouter()


@router.get("/{verse_id}", response_model=VerseDetail)
async def get_verse(
    verse_id: int = Path(..., description="The ID of the verse to retrieve"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get detailed information about a specific Bible verse.

    This endpoint returns a verse with detailed book information.
    No authentication is required for this endpoint.
    """
    # In a real implementation, this would fetch from the database
    # For this example, we'll use a mock implementation as this endpoint isn't provided
    # in the BibleService yet

    # Extract book_id and chapter_id from verse_id
    chapter_id = verse_id // 1000
    book_id = chapter_id // 1000
    verse_number = verse_id % 1000
    chapter_number = chapter_id % 1000

    # Get book info
    book = await BibleService.get_book(book_id)

    # Create a mock verse
    return VerseDetail(
        id=verse_id,
        chapter_id=chapter_id,
        book_id=book_id,
        chapter_number=chapter_number,
        verse_number=verse_number,
        text=f"Este é o texto do versículo {verse_number} do capítulo {chapter_number} de {book.name}.",
        book_name=book.name,
        book_abbreviation=book.abbreviation,
        testament=book.testament
    )


@router.post("/{verse_id}/favorite", status_code=status.HTTP_200_OK)
async def toggle_favorite(
    verse_id: int = Path(...,
                         description="The ID of the verse to favorite/unfavorite"),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Toggle a verse as favorite for the current user.

    This endpoint allows users to mark/unmark a verse as a favorite.
    Authentication is required for this endpoint.
    """
    # In a real implementation, this would toggle the favorite status in the database
    # For this example, we'll return a mock response
    return {"success": True, "message": "Verse favorite status toggled successfully"}
