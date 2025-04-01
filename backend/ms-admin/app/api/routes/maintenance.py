from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from typing import Optional
from datetime import datetime

from app.services.maintenance_service import MaintenanceService
from app.schemas.maintenance import (
    MaintenanceTask,
    MaintenanceTaskCreate,
    MaintenanceTaskUpdate,
    MaintenanceTaskListResponse
)
from app.api.deps import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=MaintenanceTaskListResponse)
async def get_maintenance_tasks(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"),
    status: Optional[str] = Query(
        None, description="Filter by status (pending, in_progress, completed, failed)"),
    priority: Optional[str] = Query(
        None, description="Filter by priority (low, medium, high, critical)"),
    task_type: Optional[str] = Query(
        None, description="Filter by task type (backup, cleanup, index_rebuild, etc.)"),
    is_automatic: Optional[bool] = Query(
        None, description="Filter by whether task is automatic"),
    search: Optional[str] = Query(
        None, description="Search term for title or description"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve maintenance tasks with filtering and pagination.

    This endpoint allows administrators to view and filter system maintenance tasks 
    based on various criteria.
    """
    return await MaintenanceService.get_maintenance_tasks(
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        task_type=task_type,
        is_automatic=is_automatic,
        search=search
    )


@router.post("/", response_model=MaintenanceTask, status_code=status.HTTP_201_CREATED)
async def create_maintenance_task(
    task_data: MaintenanceTaskCreate = Body(...,
                                            description="Task data to create"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Create a new maintenance task.

    This endpoint allows administrators to create a new maintenance task, either 
    for manual execution or automatic scheduling.
    """
    return await MaintenanceService.create_maintenance_task(
        task_data=task_data,
        admin_id=current_user["id"]
    )


@router.get("/{task_id}", response_model=MaintenanceTask)
async def get_task_details(
    task_id: str = Path(..., description="The ID of the task to retrieve"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve detailed information about a specific maintenance task.

    This endpoint returns complete information about a maintenance task, including 
    status, scheduling, and completion details.
    """
    return await MaintenanceService.get_task_details(task_id)


@router.patch("/{task_id}/status", response_model=MaintenanceTask)
async def update_task_status(
    task_id: str = Path(..., description="The ID of the task to update"),
    update_data: MaintenanceTaskUpdate = Body(
        ..., description="Status update information"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Update the status of a maintenance task.

    This endpoint allows administrators to mark a task as in_progress, completed or 
    failed, and provide any relevant status information.
    """
    return await MaintenanceService.update_task_status(
        task_id=task_id,
        update_data=update_data
    )
