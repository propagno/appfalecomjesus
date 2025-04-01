from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional

from app.services.bible_service import BibleService
from app.schemas.bible import SearchResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search_bible(
    q: str = Query(..., min_length=2, description="Search query"),
    testament: Optional[str] = Query(
        None, description="Filter by testament ('old' or 'new')"),
    book_id: Optional[int] = Query(None, description="Filter by book ID"),
    current_user: Optional[dict] = Depends(get_current_user)
):
    """
    Search the Bible for a specific text.

    This endpoint allows searching the Bible for specific words or phrases,
    optionally filtered by testament or book.
    No authentication is required for this endpoint.
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters long"
        )

    return await BibleService.search_bible(
        query=q,
        testament=testament,
        book_id=book_id
    )
