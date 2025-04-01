from fastapi import APIRouter, Depends
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import VerseOfDayResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=VerseOfDayResponse)
async def get_verse_of_day(
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Get the verse of the day.

    This endpoint returns a specially selected verse for the current day,
    along with a theme and reflection. The verse changes daily.
    No authentication is required for this endpoint.
    """
    return await BibleService.get_verse_of_day()
