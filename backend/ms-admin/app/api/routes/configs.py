from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from typing import Optional

from app.services.config_service import ConfigService
from app.schemas.system_config import (
    SystemConfig,
    SystemConfigCreate,
    SystemConfigUpdate,
    SystemConfigListResponse
)
from app.api.deps import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=SystemConfigListResponse)
async def get_system_configs(
    category: Optional[str] = Query(
        None, description="Filter by configuration category"),
    include_sensitive: bool = Query(
        False, description="Whether to include sensitive configurations"),
    search: Optional[str] = Query(
        None, description="Search term for key or description"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve system configurations with optional filtering.

    This endpoint allows administrators to view and filter system configurations.
    Sensitive configurations are hidden by default unless explicitly requested.
    """
    return await ConfigService.get_system_configs(
        category=category,
        include_sensitive=include_sensitive,
        search=search
    )


@router.post("/", response_model=SystemConfig, status_code=status.HTTP_201_CREATED)
async def create_system_config(
    config_data: SystemConfigCreate = Body(...,
                                           description="Configuration data to create"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Create a new system configuration.

    This endpoint allows administrators to add a new configuration to the system.
    Keys must be unique and follow the format `category.subcategory.name`.
    """
    return await ConfigService.create_system_config(
        config_data=config_data,
        admin_id=current_user["id"]
    )


@router.get("/{config_id}", response_model=SystemConfig)
async def get_config_details(
    config_id: str = Path(...,
                          description="The ID of the configuration to retrieve"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Retrieve detailed information about a specific system configuration.

    This endpoint returns complete information about a configuration, including 
    when it was last updated and by whom.
    """
    return await ConfigService.get_config_details(config_id)


@router.patch("/{config_id}", response_model=SystemConfig)
async def update_system_config(
    config_id: str = Path(...,
                          description="The ID of the configuration to update"),
    update_data: SystemConfigUpdate = Body(...,
                                           description="Configuration update data"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Update an existing system configuration.

    This endpoint allows administrators to update the value and description of 
    an existing configuration. The configuration key cannot be changed.
    """
    return await ConfigService.update_system_config(
        config_id=config_id,
        update_data=update_data,
        admin_id=current_user["id"]
    )


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_system_config(
    config_id: str = Path(...,
                          description="The ID of the configuration to delete"),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete a system configuration.

    This endpoint allows administrators to remove a configuration from the system.
    Protected configurations cannot be deleted.
    """
    await ConfigService.delete_system_config(config_id)
    return None
