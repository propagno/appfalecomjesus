import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.monetization import AdReward
from app.schemas.monetization import AdRewardCreate

logger = logging.getLogger(__name__)


class AdsService:
    """
    Serviço para gerenciamento de anúncios e recompensas.

    Responsável por:
    - Controlar limites diários de anúncios
    - Registrar visualizações
    - Gerenciar recompensas
    - Validar elegibilidade

    Attributes:
        db: Sessão do banco de dados
        redis: Cliente Redis para cache
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de anúncios.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    async def check_daily_limit(
        self,
        user_id: UUID
    ) -> bool:
        """
        Verifica se usuário atingiu limite diário.

        Args:
            user_id: ID do usuário

        Returns:
            True se ainda pode assistir anúncios

        Raises:
            HTTPException: Se erro na verificação
        """
        try:
            today = datetime.utcnow().date()

            # Conta anúncios assistidos hoje
            count = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.watched_at >= today
            ).count()

            return count < settings.MAX_DAILY_ADS

        except Exception as e:
            logger.error(f"Error checking daily limit: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar limite diário"
            )

    async def register_ad_view(
        self,
        user_id: UUID,
        ad_type: str,
        reward_type: str,
        reward_value: int
    ) -> Dict:
        """
        Registra visualização de anúncio.

        Args:
            user_id: ID do usuário
            ad_type: Tipo do anúncio (vídeo, banner)
            reward_type: Tipo da recompensa (chat, estudo)
            reward_value: Valor da recompensa

        Returns:
            Dict com detalhes da recompensa

        Raises:
            HTTPException: Se erro no registro
        """
        try:
            # Verifica limite diário
            if not await self.check_daily_limit(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Limite diário de anúncios atingido"
                )

            # Cria registro
            reward = AdReward(
                user_id=user_id,
                ad_type=ad_type,
                reward_type=reward_type,
                reward_value=reward_value,
                watched_at=datetime.utcnow()
            )

            self.db.add(reward)
            self.db.commit()
            self.db.refresh(reward)

            return {
                "id": reward.id,
                "reward_type": reward.reward_type,
                "reward_value": reward.reward_value,
                "watched_at": reward.watched_at
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error registering ad view: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao registrar visualização"
            )

    async def get_remaining_rewards(
        self,
        user_id: UUID
    ) -> Dict:
        """
        Retorna recompensas restantes do dia.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com total e restantes

        Raises:
            HTTPException: Se erro na consulta
        """
        try:
            today = datetime.utcnow().date()

            # Conta anúncios assistidos hoje
            count = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.watched_at >= today
            ).count()

            return {
                "total_daily": settings.MAX_DAILY_ADS,
                "watched_today": count,
                "remaining": settings.MAX_DAILY_ADS - count
            }

        except Exception as e:
            logger.error(f"Error getting remaining rewards: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar recompensas restantes"
            )

    async def get_reward_history(
        self,
        user_id: UUID,
        days: int = 7
    ) -> List[Dict]:
        """
        Retorna histórico de recompensas.

        Args:
            user_id: ID do usuário
            days: Dias para buscar histórico

        Returns:
            Lista de recompensas

        Raises:
            HTTPException: Se erro na consulta
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            rewards = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.watched_at >= start_date
            ).order_by(AdReward.watched_at.desc()).all()

            return [{
                "id": r.id,
                "ad_type": r.ad_type,
                "reward_type": r.reward_type,
                "reward_value": r.reward_value,
                "watched_at": r.watched_at
            } for r in rewards]

        except Exception as e:
            logger.error(f"Error getting reward history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar histórico"
            )

    async def validate_reward_eligibility(
        self,
        user_id: UUID,
        reward_type: str
    ) -> bool:
        """
        Valida se usuário pode receber recompensa.

        Args:
            user_id: ID do usuário
            reward_type: Tipo da recompensa

        Returns:
            True se elegível

        Raises:
            HTTPException: Se erro na validação
        """
        try:
            # Verifica limite diário
            if not await self.check_daily_limit(user_id):
                return False

            # Verifica cooldown entre recompensas
            last_reward = self.db.query(AdReward).filter(
                AdReward.user_id == user_id,
                AdReward.reward_type == reward_type
            ).order_by(AdReward.watched_at.desc()).first()

            if last_reward:
                cooldown = datetime.utcnow() - last_reward.watched_at
                if cooldown < timedelta(minutes=settings.REWARD_COOLDOWN_MINUTES):
                    return False

            return True

        except Exception as e:
            logger.error(f"Error validating eligibility: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao validar elegibilidade"
            )
