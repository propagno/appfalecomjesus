# Importar a classe Base do session.py
from app.db.session import Base

# Importar todos os modelos que devem ser registrados no SQLAlchemy
from app.models.user_point import UserPoint
from app.models.point_history import PointHistory
from app.models.achievement import Achievement
from app.models.user_achievement import UserAchievement
