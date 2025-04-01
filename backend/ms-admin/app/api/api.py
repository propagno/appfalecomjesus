from fastapi import APIRouter
from .routes import dashboard, users, logs, maintenance, configs, backups, reports

api_router = APIRouter()

api_router.include_router(
    dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(
    maintenance.router, prefix="/maintenance", tags=["maintenance"])
api_router.include_router(configs.router, prefix="/configs", tags=["configs"])
api_router.include_router(backups.router, prefix="/backup", tags=["backups"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
