from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import random
from fastapi import HTTPException, status

from app.schemas.report import (
    ReportJobRequest,
    ReportJobResponse,
    ReportInfo,
    ReportListResponse
)


class ReportService:
    """Service for managing system reports."""

    # Mock database to store report job statuses
    _report_jobs = {}
    _reports = []

    @staticmethod
    async def generate_report(report_data: ReportJobRequest, admin_id: str) -> ReportJobResponse:
        """
        Generate a new report.

        Args:
            report_data: Report configuration and parameters
            admin_id: ID of the admin requesting the report

        Returns:
            ReportJobResponse with job ID and initial status
        """
        # Validate report type
        valid_report_types = [
            "user_activity",
            "study_progress",
            "chat_usage",
            "system_performance",
            "financial"
        ]

        if report_data.type not in valid_report_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid report type. Must be one of: {', '.join(valid_report_types)}"
            )

        # Validate date range
        try:
            start_date = datetime.strptime(report_data.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(report_data.end_date, "%Y-%m-%d")

            if start_date > end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Start date must be before end date"
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )

        # Generate a new job ID
        job_id = str(uuid.uuid4())

        # In a real implementation, this would start a background task
        # For now, we'll just store the job in our mock database
        ReportService._report_jobs[job_id] = {
            "status": "pending",
            "message": "Report generation queued",
            "admin_id": admin_id,
            "report_type": report_data.type,
            "start_date": report_data.start_date,
            "end_date": report_data.end_date,
            "custom_params": report_data.custom_params,
            "created_at": datetime.now()
        }

        # For demonstration purposes, we'll immediately "complete" some reports
        # In a real implementation, this would be done by a background task
        if random.random() > 0.7:  # 30% chance of immediate completion
            report_id = str(uuid.uuid4())
            ReportService._reports.append({
                "id": report_id,
                "type": report_data.type,
                "date_range": {
                    "start": report_data.start_date,
                    "end": report_data.end_date
                },
                "created_at": datetime.now(),
                "created_by": admin_id,
                # Random size between 10KB and 1MB
                "size": random.randint(10000, 1000000),
                "download_url": f"/api/admin/reports/download/{report_id}"
            })

            ReportService._report_jobs[job_id]["status"] = "completed"
            ReportService._report_jobs[job_id]["message"] = "Report generated successfully"

        return ReportJobResponse(
            job_id=job_id,
            status=ReportService._report_jobs[job_id]["status"],
            message=ReportService._report_jobs[job_id]["message"]
        )

    @staticmethod
    async def check_report_status(job_id: str) -> ReportJobResponse:
        """
        Check the status of a report generation job.

        Args:
            job_id: The ID of the report job

        Returns:
            ReportJobResponse with current status

        Raises:
            HTTPException: If job not found
        """
        # Check if job exists in our mock database
        if job_id not in ReportService._report_jobs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report job not found"
            )

        job = ReportService._report_jobs[job_id]

        # Simulate progress for demo purposes
        # In a real implementation, we would check the actual report generation process
        if job["status"] == "pending":
            job["status"] = "in_progress"
            job["message"] = "Generating report - gathering data"
        elif job["status"] == "in_progress" and random.random() > 0.5:  # 50% chance of completion
            job["status"] = "completed"
            job["message"] = "Report generated successfully"

            # Create a completed report
            report_id = str(uuid.uuid4())
            ReportService._reports.append({
                "id": report_id,
                "type": job["report_type"],
                "date_range": {
                    "start": job["start_date"],
                    "end": job["end_date"]
                },
                "created_at": datetime.now(),
                "created_by": job["admin_id"],
                # Random size between 10KB and 1MB
                "size": random.randint(10000, 1000000),
                "download_url": f"/api/admin/reports/download/{report_id}"
            })

        return ReportJobResponse(
            job_id=job_id,
            status=job["status"],
            message=job["message"]
        )

    @staticmethod
    async def list_reports() -> ReportListResponse:
        """
        List all available reports.

        Returns:
            ReportListResponse with list of available reports
        """
        # Use the mock reports list
        # In a real implementation, we would query the database

        # Generate some additional mock reports if our list is empty
        if not ReportService._reports:
            report_types = ["user_activity", "study_progress",
                            "chat_usage", "system_performance", "financial"]

            for i in range(5):
                report_id = str(uuid.uuid4())
                ReportService._reports.append({
                    "id": report_id,
                    "type": report_types[i % len(report_types)],
                    "date_range": {
                        "start": "2023-01-01",
                        "end": "2023-01-31"
                    },
                    "created_at": datetime.now().replace(day=datetime.now().day - i),
                    "created_by": "admin",
                    "size": random.randint(10000, 1000000),
                    "download_url": f"/api/admin/reports/download/{report_id}"
                })

        # Convert to ReportInfo objects
        report_items = [ReportInfo(**report)
                        for report in ReportService._reports]

        return ReportListResponse(
            items=report_items,
            total=len(report_items)
        )

    @staticmethod
    async def get_report(report_id: str) -> ReportInfo:
        """
        Get information about a specific report.

        Args:
            report_id: The ID of the report

        Returns:
            ReportInfo object

        Raises:
            HTTPException: If report not found
        """
        # Check if report exists in our mock database
        for report in ReportService._reports:
            if report["id"] == report_id:
                return ReportInfo(**report)

        # If not found, raise an exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    @staticmethod
    async def delete_report(report_id: str) -> bool:
        """
        Delete a report.

        Args:
            report_id: The ID of the report to delete

        Returns:
            True if deletion was successful

        Raises:
            HTTPException: If report not found
        """
        # Check if report exists in our mock database
        for i, report in enumerate(ReportService._reports):
            if report["id"] == report_id:
                del ReportService._reports[i]
                return True

        # If not found, raise an exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
