from typing import Dict, List, Optional
from datetime import datetime
import uuid
import random
from fastapi import HTTPException, status

from app.schemas.backup import (
    BackupJobCreate,
    BackupJobResponse,
    BackupInfo,
    BackupListResponse
)


class BackupService:
    """Service for managing system backups."""

    # Mock database to store backup job statuses
    _backup_jobs = {}

    @staticmethod
    async def trigger_backup(backup_data: BackupJobCreate, admin_id: str) -> BackupJobResponse:
        """
        Trigger a new backup job.

        Args:
            backup_data: Backup configuration
            admin_id: ID of the admin triggering the backup

        Returns:
            BackupJobResponse with job ID and initial status
        """
        # Generate a new job ID
        job_id = str(uuid.uuid4())

        # In a real implementation, this would start a background task
        # For now, we'll just store the job in our mock database
        BackupService._backup_jobs[job_id] = {
            "status": "pending",
            "progress": 0,
            "message": "Backup job created and queued",
            "admin_id": admin_id,
            "description": backup_data.description,
            "include_files": backup_data.include_files,
            "include_database": backup_data.include_database,
            "created_at": datetime.now()
        }

        return BackupJobResponse(
            job_id=job_id,
            status="pending",
            message="Backup job created and queued"
        )

    @staticmethod
    async def check_backup_status(job_id: str) -> BackupJobResponse:
        """
        Check the status of a backup job.

        Args:
            job_id: The ID of the backup job

        Returns:
            BackupJobResponse with current status and progress

        Raises:
            HTTPException: If job not found
        """
        # Check if job exists in our mock database
        if job_id not in BackupService._backup_jobs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Backup job not found"
            )

        job = BackupService._backup_jobs[job_id]

        # Simulate progress for demo purposes
        # In a real implementation, we would check the actual backup process
        if job["status"] == "pending":
            job["status"] = "in_progress"
            job["progress"] = 10
            job["message"] = "Backup in progress - preparing files"
        elif job["status"] == "in_progress":
            progress = job["progress"] + random.randint(10, 30)
            if progress >= 100:
                job["status"] = "completed"
                job["progress"] = 100
                job["message"] = "Backup completed successfully"
                job["download_url"] = f"/api/admin/backup/download/{job_id}"
            else:
                job["progress"] = progress
                job["message"] = f"Backup in progress - {progress}% complete"

        return BackupJobResponse(
            job_id=job_id,
            status=job["status"],
            message=job["message"],
            progress=job["progress"],
            download_url=job.get("download_url")
        )

    @staticmethod
    async def list_backups() -> BackupListResponse:
        """
        List all completed backups.

        Returns:
            BackupListResponse with list of available backups
        """
        # In a real implementation, we would query the filesystem or database
        # For now, we'll generate some mock backups

        # First, check if any jobs in our mock database have completed
        completed_jobs = [
            {
                "id": job_id,
                "date": job["created_at"],
                # Random size between 1MB and 100MB
                "size": random.randint(1000000, 100000000),
                "description": job.get("description"),
                "created_by": job["admin_id"],
                "download_url": f"/api/admin/backup/download/{job_id}",
                "includes_files": job["include_files"],
                "includes_database": job["include_database"]
            }
            for job_id, job in BackupService._backup_jobs.items()
            if job["status"] == "completed"
        ]

        # Add some additional mock backups
        mock_backups = [
            {
                "id": str(uuid.uuid4()),
                "date": datetime.now().replace(day=datetime.now().day - i),
                "size": random.randint(1000000, 100000000),
                "description": f"Scheduled backup {i}",
                "created_by": "system",
                "download_url": f"/api/admin/backup/download/{uuid.uuid4()}",
                "includes_files": True,
                "includes_database": True
            }
            for i in range(1, 6)
        ]

        all_backups = completed_jobs + mock_backups

        # Convert to BackupInfo objects
        backup_items = [BackupInfo(**backup) for backup in all_backups]

        return BackupListResponse(
            items=backup_items,
            total=len(backup_items)
        )

    @staticmethod
    async def get_backup(backup_id: str) -> BackupInfo:
        """
        Get information about a specific backup.

        Args:
            backup_id: The ID of the backup

        Returns:
            BackupInfo object

        Raises:
            HTTPException: If backup not found
        """
        # In a real implementation, we would query the filesystem or database
        # For now, we'll generate a mock backup

        # Check if it's a completed job in our mock database
        for job_id, job in BackupService._backup_jobs.items():
            if job_id == backup_id and job["status"] == "completed":
                return BackupInfo(
                    id=job_id,
                    date=job["created_at"],
                    size=random.randint(1000000, 100000000),
                    description=job.get("description"),
                    created_by=job["admin_id"],
                    download_url=f"/api/admin/backup/download/{job_id}",
                    includes_files=job["include_files"],
                    includes_database=job["include_database"]
                )

        # If not found, generate a mock or raise an error
        if backup_id == "notfound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Backup not found"
            )

        return BackupInfo(
            id=backup_id,
            date=datetime.now(),
            size=random.randint(1000000, 100000000),
            description="Daily automated backup",
            created_by="system",
            download_url=f"/api/admin/backup/download/{backup_id}",
            includes_files=True,
            includes_database=True
        )

    @staticmethod
    async def delete_backup(backup_id: str) -> bool:
        """
        Delete a backup.

        Args:
            backup_id: The ID of the backup to delete

        Returns:
            True if deletion was successful

        Raises:
            HTTPException: If backup not found or deletion failed
        """
        # In a real implementation, we would delete the backup files

        # Check if it's a completed job in our mock database
        for job_id, job in BackupService._backup_jobs.items():
            if job_id == backup_id:
                if job["status"] == "in_progress":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cannot delete a backup that is in progress"
                    )
                del BackupService._backup_jobs[job_id]
                return True

        # If not found, raise an error
        if backup_id == "notfound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Backup not found"
            )

        return True
