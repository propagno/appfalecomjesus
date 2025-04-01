from fastapi import APIRouter
from app.api.v1.study import study_router

api_router = APIRouter()

api_router.include_router(study_router, prefix="/study", tags=["study"])
