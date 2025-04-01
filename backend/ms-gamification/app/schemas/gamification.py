from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from uuid import UUID


class PointCategory(str, Enum):
    """Categorias possíveis para pontos"""
    PRAYER = "prayer"
    STUDY = "study"
    SHARE = "share"
    READING = "reading"
    REFLECTION = "reflection"
    CHALLENGE = "challenge"
    STREAK = "streak"
    OTHER = "other"


class ActionSource(str, Enum):
    """Fontes possíveis para ações que geram pontos"""
    BIBLE = "bible"
    STUDY = "study"
    PRAYER = "prayer"
    REWARD = "reward"
    ADMIN = "admin"
    SYSTEM = "system"
    OTHER = "other"


class AchievementDifficulty(str, Enum):
    """Níveis de dificuldade para conquistas"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class TimePeriod(str, Enum):
    """Períodos de tempo para rankings"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"


# UserPoint Schemas
class UserPointBase(BaseModel):
    user_id: str
    total_points: int = 0


class UserPointCreate(UserPointBase):
    pass


class UserPoint(UserPointBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# PointHistory Schemas
class PointHistoryBase(BaseModel):
    user_id: str
    amount: int
    reason: str


class PointHistoryCreate(PointHistoryBase):
    pass


class PointHistory(PointHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# Achievement Schemas
class AchievementBase(BaseModel):
    badge_name: str
    description: str
    category: str
    points_required: int = 0
    condition_type: str
    condition_value: int = 0
    icon_url: Optional[str] = None


class AchievementCreate(AchievementBase):
    pass


class Achievement(AchievementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


# UserAchievement Schemas
class UserAchievementBase(BaseModel):
    user_id: str
    achievement_id: int


class UserAchievementCreate(UserAchievementBase):
    pass


class UserAchievement(UserAchievementBase):
    id: int
    earned_at: datetime
    notified: int = 0

    class Config:
        orm_mode = True
        from_attributes = True


# Esquemas para respostas da API
class AddPointsRequest(BaseModel):
    amount: int
    reason: str


class AddPointsResponse(BaseModel):
    total_points: int
    amount_added: int
    message: str


class AchievementResponse(BaseModel):
    id: int
    badge_name: str
    description: str
    category: str
    icon_url: Optional[str] = None
    earned_at: datetime


class CheckAchievementsResponse(BaseModel):
    new_achievements: List[AchievementResponse] = []
    total_achievements: int


# Schemas para pontos

class PointCategoryDetail(BaseModel):
    """Detalhes de pontos por categoria"""
    category: str = Field(..., description="Nome da categoria")
    points: int = Field(...,
                        description="Quantidade de pontos nesta categoria")
    percentage: float = Field(..., description="Percentual do total de pontos")


class PointHistoryItem(BaseModel):
    """Um item no histórico de pontos"""
    id: str = Field(..., description="ID único da transação")
    amount: int = Field(...,
                        description="Quantidade de pontos (positivo ou negativo)")
    category: str = Field(..., description="Categoria dos pontos")
    description: str = Field(..., description="Descrição da ação")
    action_source: str = Field(...,
                               description="Fonte da ação que gerou os pontos")
    created_at: datetime = Field(..., description="Data e hora da transação")

    class Config:
        orm_mode = True


class UserPointsDetail(BaseModel):
    """Detalhes dos pontos de um usuário"""
    user_id: str = Field(..., description="ID do usuário")
    total_points: int = Field(..., description="Total de pontos do usuário")
    categories: List[PointCategoryDetail] = Field(
        ..., description="Pontos por categoria")
    last_updated: datetime = Field(
        ..., description="Última atualização dos pontos")

    class Config:
        orm_mode = True


class UserPointsResponse(BaseModel):
    """Resposta com os pontos do usuário"""
    points: UserPointsDetail = Field(..., description="Detalhes dos pontos")
    rank: Optional[int] = Field(None, description="Posição no ranking global")
    level: int = Field(..., description="Nível atual do usuário")
    next_level_points: int = Field(
        ..., description="Pontos necessários para o próximo nível")
    level_progress: float = Field(
        ..., description="Progresso percentual para o próximo nível")

    class Config:
        orm_mode = True


class PointsHistoryResponse(BaseModel):
    """Resposta com o histórico de transações de pontos"""
    items: List[PointHistoryItem] = Field(
        ..., description="Lista de transações")
    total: int = Field(..., description="Total de transações")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")


class PointsAddRequest(BaseModel):
    """Requisição para adicionar pontos ao usuário"""
    amount: int = Field(..., gt=0,
                        description="Quantidade de pontos a adicionar")
    category: str = Field(..., description="Categoria dos pontos")
    description: str = Field(..., description="Descrição da ação")
    action_source: str = Field(...,
                               description="Fonte da ação que gerou os pontos")


class PointsSubtractRequest(BaseModel):
    """Requisição para subtrair pontos do usuário"""
    amount: int = Field(..., gt=0,
                        description="Quantidade de pontos a subtrair")
    category: str = Field(..., description="Categoria dos pontos")
    description: str = Field(..., description="Descrição da ação")
    action_source: str = Field(..., description="Fonte da ação")


# Schemas para conquistas

class AchievementProgressDetail(BaseModel):
    """Detalhes do progresso em uma conquista"""
    current_value: int = Field(..., description="Valor atual")
    target_value: int = Field(..., description="Valor alvo para completar")
    percentage: float = Field(..., description="Percentual de progresso")
    completed: bool = Field(..., description="Se foi concluída")
    completed_at: Optional[datetime] = Field(
        None, description="Data e hora de conclusão")


class AchievementListResponse(BaseModel):
    """Resposta com lista paginada de conquistas"""
    items: List[AchievementResponse] = Field(
        ..., description="Lista de conquistas")
    total: int = Field(..., description="Total de conquistas")
    page: int = Field(..., description="Página atual")
    page_size: int = Field(..., description="Tamanho da página")


class UserAchievementSummary(BaseModel):
    """Resumo das conquistas de um usuário"""
    total_achievements: int = Field(
        ..., description="Total de conquistas disponíveis")
    completed_achievements: int = Field(
        ..., description="Conquistas já obtidas")
    completion_percentage: float = Field(
        ..., description="Percentual de conclusão")
    total_points_from_achievements: int = Field(
        ..., description="Total de pontos obtidos com conquistas")


class UserAchievementResponse(BaseModel):
    """Resposta com conquistas de um usuário"""
    summary: UserAchievementSummary = Field(
        ..., description="Resumo das conquistas")
    completed: List[AchievementResponse] = Field(
        ..., description="Conquistas já obtidas")
    in_progress: List[AchievementResponse] = Field(
        ..., description="Conquistas em andamento")
    recent: List[AchievementResponse] = Field(
        ..., description="Conquistas recentemente obtidas")


# Schemas para leaderboard (ranking)

class LeaderboardEntryResponse(BaseModel):
    """Uma entrada no ranking"""
    position: int = Field(..., description="Posição no ranking")
    user_id: str = Field(..., description="ID do usuário")
    username: str = Field(..., description="Nome de usuário")
    points: int = Field(..., description="Total de pontos")
    level: int = Field(..., description="Nível atual")
    avatar_url: Optional[str] = Field(None, description="URL do avatar")
    is_current_user: bool = Field(
        False, description="Se é o usuário atual")

    class Config:
        orm_mode = True


class UserRankingResponse(BaseModel):
    """Resposta com a posição do usuário no ranking"""
    position: int = Field(..., description="Posição no ranking global")
    total_users: int = Field(..., description="Total de usuários no ranking")
    percentile: float = Field(
        ..., description="Percentil (top X% dos usuários)")
    points: int = Field(..., description="Total de pontos")
    points_to_next: Optional[int] = Field(
        None, description="Pontos para alcançar a próxima posição")
    points_above_previous: Optional[int] = Field(
        None, description="Pontos acima da posição anterior")


class LeaderboardResponse(BaseModel):
    """Resposta com o ranking"""
    entries: List[LeaderboardEntryResponse] = Field(
        ..., description="Entradas do ranking")
    total: int = Field(..., description="Total de usuários no ranking")
    category: Optional[str] = Field(
        None, description="Categoria do ranking (se aplicável)")
    time_period: str = Field(..., description="Período de tempo")
    user_ranking: Optional[UserRankingResponse] = Field(
        None, description="Posição do usuário (se autenticado)")

    class Config:
        orm_mode = True


# ===== Schemas de Point (Pontos) =====

class PointBase(BaseModel):
    """Schema base para pontos"""
    category: str
    amount: int


class PointCreate(PointBase):
    """Schema para criação de pontos"""
    user_id: str
    action: str
    description: Optional[str] = None
    related_entity_id: Optional[str] = None


class PointUpdate(BaseModel):
    """Schema para atualização de pontos"""
    amount: int


class PointResponse(PointBase):
    """Schema para resposta de pontos"""
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PointHistoryBase(BaseModel):
    """Schema base para histórico de pontos"""
    category: str
    amount: int
    action: str
    description: Optional[str] = None
    related_entity_id: Optional[str] = None


class PointHistoryCreate(PointHistoryBase):
    """Schema para criação de registro de histórico de pontos"""
    user_id: str


class PointHistoryResponse(PointHistoryBase):
    """Schema para resposta de histórico de pontos"""
    id: UUID
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserPointsResponse(BaseModel):
    """Schema para resposta de pontos totais do usuário"""
    total_points: int
    categories: Dict[str, int]  # Mapa de categoria -> pontos


class PointOperationRequest(BaseModel):
    """Schema para solicitar operação de adição/subtração de pontos"""
    amount: int = Field(..., gt=0,
                        description="Quantidade de pontos a adicionar/subtrair")
    category: str = Field(...,
                          description="Categoria dos pontos (ex: estudo_diario, chat_ia)")
    action: str = Field(...,
                        description="Fonte da ação (ex: completar_estudo, responder_chat)")
    description: Optional[str] = Field(None, description="Descrição adicional")
    related_entity_id: Optional[str] = Field(
        None, description="ID da entidade relacionada")


# ===== Schemas de Achievement (Conquistas) =====

class AchievementBase(BaseModel):
    """Schema base para conquistas"""
    code: str
    name: str
    description: str
    category: str
    difficulty: str
    points_required: int
    criteria: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    reward_points: int
    is_hidden: bool = False


class AchievementCreate(AchievementBase):
    """Schema para criação de conquistas"""
    pass


class AchievementUpdate(BaseModel):
    """Schema para atualização de conquistas"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    points_required: Optional[int] = None
    criteria: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    reward_points: Optional[int] = None
    is_hidden: Optional[bool] = None


class AchievementResponse(AchievementBase):
    """Schema para resposta de conquistas"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserAchievementBase(BaseModel):
    """Schema base para conquistas de usuário"""
    achievement_id: UUID
    progress: float
    current_points: int
    unlocked_at: Optional[datetime] = None


class UserAchievementCreate(UserAchievementBase):
    """Schema para criação de conquistas de usuário"""
    user_id: str


class UserAchievementUpdate(BaseModel):
    """Schema para atualização de conquistas de usuário"""
    progress: Optional[float] = None
    current_points: Optional[int] = None
    unlocked_at: Optional[datetime] = None


class UserAchievementResponse(UserAchievementBase):
    """Schema para resposta de conquistas de usuário"""
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    is_unlocked: bool

    # Informações adicionais da conquista
    achievement: Optional[AchievementResponse] = None

    class Config:
        from_attributes = True


class AchievementProgressResponse(BaseModel):
    """Schema para resposta de progresso de conquista"""
    achievement_id: UUID
    current_points: int
    points_required: int
    progress: float
    is_unlocked: bool
    unlocked_at: Optional[datetime] = None


class AchievementUnlockedResponse(BaseModel):
    """Schema para resposta de conquista desbloqueada"""
    achievement: AchievementResponse
    unlocked_at: datetime
    reward_points: int


# ===== Schemas de Leaderboard (Ranking) =====

class LeaderboardEntryResponse(BaseModel):
    """Schema para entrada no ranking"""
    rank: int
    user_id: str
    points: int
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    """Schema para resposta do ranking"""
    entries: List[LeaderboardEntryResponse]
    total: int
    skip: int
    limit: int
    period: str  # daily, weekly, monthly, all_time
    category: Optional[str] = None


class UserRankingResponse(BaseModel):
    """Schema para resposta de ranking do usuário"""
    user_id: str
    rank: int
    points: int
    total_participants: int
    category: Optional[str] = None
    period: str
    points_to_advance: int  # Pontos para subir no ranking
    points_advantage: int  # Vantagem para o usuário abaixo
    next_user: Optional[str] = None  # Usuário acima
    previous_user: Optional[str] = None  # Usuário abaixo


class AchievementDetail(BaseModel):
    """Schema detalhado de uma conquista"""
    id: int
    badge_name: str
    description: str
    category: str
    icon_url: Optional[str] = None
    earned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserAchievementDetail(BaseModel):
    """Schema detalhado de uma conquista do usuário"""
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    icon_url: Optional[str] = None
    badge_url: Optional[str] = None
    unlocked_at: datetime

    class Config:
        from_attributes = True
