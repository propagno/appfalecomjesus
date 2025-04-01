from fastapi import APIRouter
from app.api.v1 import points, achievements, leaderboard

api_router = APIRouter()

# Incluir rotas de pontos
api_router.include_router(
    points.router,
    prefix="/points",
    tags=["points"]
)

# Incluir rotas de conquistas
api_router.include_router(
    achievements.router,
    prefix="/achievements",
    tags=["achievements"]
)

# Incluir rotas de ranking
api_router.include_router(
    leaderboard.router,
    prefix="/leaderboard",
    tags=["leaderboard"]
)
