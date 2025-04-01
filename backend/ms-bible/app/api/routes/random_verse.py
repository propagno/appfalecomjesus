from fastapi import APIRouter, Depends
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import VerseDetail
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=VerseDetail)
async def get_random_verse(
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get a random verse from the Bible.

    This endpoint returns a randomly selected verse from the Bible.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_random_verse()
