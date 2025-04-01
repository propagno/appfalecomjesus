from fastapi import APIRouter, Depends, HTTPException, status, Path, Body, Response
from fastapi.responses import FileResponse
from typing import Optional, List
import os

from app.services.backup_service import BackupService
from app.schemas.backup import (
    BackupJobCreate,
    BackupJobResponse,
    BackupInfo,
    BackupListResponse
)
from app.api.deps import get_current_admin_user

router = APIRouter()


@router.post("/", response_model=BackupJobResponse)
async def trigger_backup(
    backup_data: BackupJobCreate = Body(...,
                                        description="Backup configuration"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Trigger a new backup process.

    This endpoint initiates a backup of the system, which may include database and/or file backups 
    depending on the configuration provided.
    """
    return await BackupService.trigger_backup(
        backup_data=backup_data,
        admin_id=current_user["id"]
    )


@router.get("/{job_id}/status", response_model=BackupJobResponse)
async def check_backup_status(
    job_id: str = Path(..., description="The ID of the backup job to check"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Check the status of a running backup job.

    This endpoint returns the current status, progress, and other information about a specific 
    backup job. Once the job is complete, it will provide a download URL.
    """
    return await BackupService.check_backup_status(job_id)


@router.get("/", response_model=BackupListResponse)
async def list_backups(
    current_user: dict = Depends(get_current_admin_user)
):
    """
    List all available backups.

    This endpoint returns a list of all completed backups available for download.
    """
    return await BackupService.list_backups()


@router.get("/{backup_id}", response_model=BackupInfo)
async def get_backup_details(
    backup_id: str = Path(..., description="The ID of the backup to retrieve"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Get detailed information about a specific backup.

    This endpoint returns information about a backup, including size, date, and download link.
    """
    return await BackupService.get_backup(backup_id)


@router.delete("/{backup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_backup(
    backup_id: str = Path(..., description="The ID of the backup to delete"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete a backup.

    This endpoint removes a backup from the system. This operation cannot be undone.
    """
    await BackupService.delete_backup(backup_id)
    return None


@router.get("/download/{backup_id}")
async def download_backup(
    backup_id: str = Path(..., description="The ID of the backup to download"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Download a backup file.

    This endpoint streams the backup file for download.
    In a real implementation, this would stream a zip or tar.gz file.
    """
    # Check if backup exists
    backup = await BackupService.get_backup(backup_id)

    # In a real implementation, we would check if the file exists and stream it
    # For mock purposes, we'll just return a text response

    # Mock file response - in a real app, this would be a file download
    return Response(
        content=f"This is a mock backup file for backup ID: {backup_id}",
        media_type="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename=backup-{backup_id}.txt"
        }
    )
