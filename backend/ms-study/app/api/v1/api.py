from fastapi import APIRouter
from app.api.v1.endpoints import study

api_router = APIRouter()

api_router.include_router(
    study.router,
    prefix="/study",
    tags=["study"]
)
