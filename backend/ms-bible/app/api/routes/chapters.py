from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import VersesResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/{chapter_id}/verses", response_model=VersesResponse)
async def get_chapter_verses(
    chapter_id: int = Path(...,
                           description="The ID of the chapter to retrieve verses for"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get all verses for a specific Bible chapter.

    This endpoint returns a list of all verses in a chapter.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_verses(chapter_id)
