from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from typing import Optional
from datetime import datetime
import uuid

from app.services.log_service import LogService
from app.schemas.system_log import SystemLog, SystemLogCreate, SystemLogUpdate, SystemLogListResponse
from app.api.deps import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=SystemLogListResponse)
async def get_logs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"),
    level: Optional[str] = Query(
        None, description="Filter by log level (ERROR, WARNING, INFO)"),
    source: Optional[str] = Query(
        None, description="Filter by log source (e.g., ms-auth, ms-study)"),
    start_date: Optional[datetime] = Query(
        None, description="Filter logs after this date"),
    end_date: Optional[datetime] = Query(
        None, description="Filter logs before this date"),
    resolved: Optional[bool] = Query(
        None, description="Filter by resolution status"),
    search: Optional[str] = Query(
        None, description="Search term for message content"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve system logs with filtering and pagination.

    This endpoint allows administrators to view and filter system logs based on various criteria.
    """
    return await LogService.get_logs(
        skip=skip,
        limit=limit,
        level=level,
        source=source,
        start_date=start_date,
        end_date=end_date,
        resolved=resolved,
        search=search
    )


@router.get("/{log_id}", response_model=SystemLog)
async def get_log_details(
    log_id: str = Path(..., description="The ID of the log to retrieve"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve detailed information about a specific log entry.

    This endpoint returns complete information about a log entry, including resolution status and detailed error information.
    """
    return await LogService.get_log_details(log_id)


@router.patch("/{log_id}/resolve", response_model=SystemLog)
async def update_log_resolution(
    log_id: str = Path(..., description="The ID of the log to update"),
    resolution_data: SystemLogUpdate = Body(...,
                                            description="Resolution information"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Update the resolution status of a log entry.

    This endpoint allows administrators to mark a log as resolved and add resolution notes.
    """
    return await LogService.update_log_resolution(
        log_id=log_id,
        resolution_data=resolution_data,
        admin_id=current_user["id"]
    )


@router.post("/", response_model=SystemLog, status_code=status.HTTP_201_CREATED)
async def add_log(
    log_data: SystemLogCreate = Body(..., description="Log data to add"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Add a new system log entry.

    This endpoint allows administrators to manually add a log entry to the system.
    """
    return await LogService.add_system_log(log_data)
