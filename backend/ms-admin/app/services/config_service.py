from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
from fastapi import HTTPException, status

from app.schemas.system_config import (
    SystemConfig,
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigListResponse
)


class ConfigService:
    """Service for managing system configurations."""

    @staticmethod
    async def get_system_configs(
        category: Optional[str] = None,
        include_sensitive: bool = False,
        search: Optional[str] = None
    ) -> SystemConfigListResponse:
        """
        Get system configurations with optional filtering.

        Args:
            category: Filter by configuration category
            include_sensitive: Whether to include sensitive configurations
            search: Search term for key or description

        Returns:
            SystemConfigListResponse with configurations
        """
        # TODO: Replace with actual database query
        # This is a mock implementation
        config_categories = ["security", "notification",
                             "appearance", "limits", "integration"]

        mock_configs = [
            SystemConfig(
                id=str(uuid.uuid4()),
                key=f"config.{category}.{'setting' + str(i)}",
                value="default_value" if i % 2 == 0 else "custom_value",
                description=f"Description for {category} setting {i}",
                is_sensitive=i % 3 == 0,
                category=category,
                updated_at=datetime.now(),
                updated_by="admin"
            )
            for i in range(1, 4)
            for category in config_categories
        ]

        # Apply filters
        filtered_configs = mock_configs

        if category:
            filtered_configs = [
                config for config in filtered_configs if config.category == category]

        if not include_sensitive:
            filtered_configs = [
                config for config in filtered_configs if not config.is_sensitive]

        if search:
            filtered_configs = [
                config for config in filtered_configs
                if search.lower() in config.key.lower() or
                (config.description and search.lower()
                 in config.description.lower())
            ]

        return SystemConfigListResponse(
            items=filtered_configs,
            total=len(filtered_configs)
        )

    @staticmethod
    async def create_system_config(
        config_data: SystemConfigCreate,
        admin_id: str
    ) -> SystemConfig:
        """
        Create a new system configuration.

        Args:
            config_data: Configuration data to create
            admin_id: ID of the admin creating the configuration

        Returns:
            Created SystemConfig object

        Raises:
            HTTPException: If configuration key already exists
        """
        # TODO: Replace with actual database insertion
        # This is a mock implementation

        # Check if key already exists (mock check)
        if config_data.key == "exists.test.key":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Configuration key already exists"
            )

        new_config = SystemConfig(
            id=str(uuid.uuid4()),
            **config_data.dict(),
            updated_at=datetime.now(),
            updated_by=admin_id
        )

        return new_config

    @staticmethod
    async def update_system_config(
        config_id: str,
        update_data: SystemConfigUpdate,
        admin_id: str
    ) -> SystemConfig:
        """
        Update an existing system configuration.

        Args:
            config_id: The ID of the configuration to update
            update_data: The update data
            admin_id: ID of the admin performing the update

        Returns:
            Updated SystemConfig object

        Raises:
            HTTPException: If configuration not found
        """
        # TODO: Replace with actual database query
        # This is a mock implementation
        if config_id == "notfound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System configuration not found"
            )

        # Assume we got a config from the database
        config = SystemConfig(
            id=config_id,
            key="notification.email.enabled",
            value="true",  # Current value
            description="Enable email notifications",
            is_sensitive=False,
            category="notification",
            updated_at=datetime.now(),
            updated_by="system"
        )

        # Update fields
        config.value = update_data.value
        if update_data.description is not None:
            config.description = update_data.description
        config.updated_at = datetime.now()
        config.updated_by = admin_id

        return config

    @staticmethod
    async def get_config_details(config_id: str) -> SystemConfig:
        """
        Get details of a specific system configuration.

        Args:
            config_id: The ID of the configuration to retrieve

        Returns:
            SystemConfig object with detailed information

        Raises:
            HTTPException: If configuration not found
        """
        # TODO: Replace with actual database query
        # This is a mock implementation
        if config_id == "notfound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System configuration not found"
            )

        return SystemConfig(
            id=config_id,
            key="security.password.min_length",
            value="8",
            description="Minimum password length for users",
            is_sensitive=False,
            category="security",
            updated_at=datetime.now(),
            updated_by="admin"
        )

    @staticmethod
    async def delete_system_config(config_id: str) -> bool:
        """
        Delete a system configuration.

        Args:
            config_id: The ID of the configuration to delete

        Returns:
            True if deletion was successful

        Raises:
            HTTPException: If configuration not found or is a protected configuration
        """
        # TODO: Replace with actual database query
        # This is a mock implementation
        if config_id == "notfound":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="System configuration not found"
            )

        # Check if it's a protected configuration
        if config_id == "protected":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a protected system configuration"
            )

        # In a real implementation, we would delete from database here

        return True
