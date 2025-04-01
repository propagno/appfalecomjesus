from typing import Optional, Dict, Tuple
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Any
from app.models.ad_reward import AdReward, AdType, RewardType
from app.schemas.ad_reward import AdRewardCreate
from uuid import UUID, uuid4
from sqlalchemy.sql import func

from app.repositories import AdRewardRepository
from app.models import AdReward as AdRewardModel
from app.schemas import AdWatchedRequest, AdWatchedResponse
from app.services.redis_client import RedisClient
from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)

# Configurações padrão
DEFAULT_REWARD_VALUE = 5  # Quantidade padrão de recompensas
# Limite de recompensas diárias assistindo anúncios
MAX_DAILY_REWARDS = settings.MAX_DAILY_AD_REWARDS


class AdRewardService:
    def __init__(self, db: Session, redis_client: RedisClient):
        self.db = db
        self.reward_repo = AdRewardRepository(db)
        self.redis_client = redis_client
        logger.info("AdRewardService inicializado")

    async def process_ad_watched(self, user_id: str, request: AdWatchedRequest) -> Tuple[AdWatchedResponse, bool]:
        """
        Processa um anúncio assistido, registrando a recompensa e atualizando os limites.
        Retorna a resposta e um booleano indicando se a recompensa foi concedida.
        """
        # Verificar se o usuário já atingiu o limite diário de recompensas
        count = await self.reward_repo.count_user_rewards_today(user_id)

        if count >= MAX_DAILY_REWARDS:
            logger.warning(
                f"Usuário {user_id} tentou obter mais recompensas do que o permitido hoje ({count}/{MAX_DAILY_REWARDS})")
            return AdWatchedResponse(
                success=False,
                reward_type=request.reward_type,
                reward_value=0,
                message="Você já atingiu o limite diário de anúncios. Tente novamente amanhã ou faça upgrade para Premium."
            ), False

        # Determinar o valor da recompensa
        reward_value = DEFAULT_REWARD_VALUE

        # Registrar a recompensa no banco
        try:
            ad_reward = await self.reward_repo.create(
                user_id=user_id,
                reward_type=request.reward_type,
                reward_value=reward_value,
                ad_provider=request.ad_provider,
                ad_id=request.ad_id,
                ip_address=request.ip_address
            )

            # Atualizar o Redis com a nova contagem de mensagens
            updated_count = None
            if request.reward_type == RewardType.CHAT_MESSAGES:
                # Adicionar a recompensa ao limite de mensagens no Redis
                chat_key = f"chat_limit:{user_id}"

                # Verificar se a chave existe
                exists = await self.redis_client.exists(chat_key)

                if exists:
                    # Incrementar o valor existente
                    updated_count = await self.redis_client.increment(chat_key, reward_value)
                    logger.info(
                        f"Incrementado limite de chat para usuário {user_id}: {updated_count}")
                else:
                    # Criar novo valor com TTL até o final do dia
                    midnight = datetime.utcnow().replace(hour=23, minute=59, second=59)
                    seconds_until_midnight = int(
                        (midnight - datetime.utcnow()).total_seconds())

                    await self.redis_client.set(
                        chat_key,
                        reward_value,
                        expire=seconds_until_midnight
                    )
                    updated_count = reward_value
                    logger.info(
                        f"Criado novo limite de chat para usuário {user_id}: {reward_value}")

            # Construir resposta
            response = AdWatchedResponse(
                success=True,
                reward_type=request.reward_type,
                reward_value=reward_value,
                message=f"Você ganhou {reward_value} " +
                ("mensagens adicionais de chat!" if request.reward_type == RewardType.CHAT_MESSAGES
                 else "dias de estudo!" if request.reward_type == RewardType.STUDY_DAYS
                 else "pontos!"),
                updated_chat_limit=updated_count
            )

            logger.info(
                f"Recompensa registrada com sucesso para usuário {user_id}: {reward_value} {request.reward_type}")
            return response, True

        except Exception as e:
            logger.error(
                f"Erro ao registrar recompensa para usuário {user_id}: {str(e)}")
            return AdWatchedResponse(
                success=False,
                reward_type=request.reward_type,
                reward_value=0,
                message="Erro ao processar recompensa. Tente novamente mais tarde."
            ), False

    async def get_user_remaining_rewards(self, user_id: str) -> int:
        """Retorna quantas recompensas ainda podem ser obtidas no dia."""
        count = await self.reward_repo.count_user_rewards_today(user_id)
        return max(0, MAX_DAILY_REWARDS - count)

    def create_ad_reward(
        self,
        db: Session,
        user_id: str,
        ad_type: str,
        reward_type: str = "chat_messages",
        reward_value: int = 5
    ) -> Optional[AdReward]:
        """
        Registra uma nova recompensa por anúncio.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário que ganhou a recompensa
            ad_type: Tipo de anúncio (video, banner, etc)
            reward_type: Tipo de recompensa (chat_messages, study_days, points)
            reward_value: Quantidade da recompensa

        Returns:
            Objeto AdReward criado ou None se falhar
        """
        try:
            # Validar tipos de enum
            valid_ad_type = AdType(ad_type.lower())
            valid_reward_type = RewardType(reward_type.lower())

            # Criar o objeto de recompensa
            ad_reward = AdReward(
                id=uuid4(),
                user_id=user_id,
                ad_type=valid_ad_type,
                reward_type=valid_reward_type,
                reward_value=reward_value,
                watched_at=datetime.utcnow()
            )

            # Salvar no banco de dados
            db.add(ad_reward)
            db.commit()
            db.refresh(ad_reward)

            logger.info(
                f"Recompensa registrada para usuário {user_id}: {reward_value} {reward_type}")
            return ad_reward

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao registrar recompensa: {str(e)}")
            return None

    def get_user_rewards(
        self,
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Obtém o histórico de recompensas de um usuário.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            skip: Número de registros a pular (para paginação)
            limit: Limite de registros a retornar

        Returns:
            Dicionário com os itens e contagem total
        """
        try:
            # Consultar total
            total = db.query(AdReward).filter(
                AdReward.user_id == user_id).count()

            # Consultar registros com paginação
            rewards = db.query(AdReward)\
                .filter(AdReward.user_id == user_id)\
                .order_by(AdReward.watched_at.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()

            return {
                "items": rewards,
                "total": total
            }

        except Exception as e:
            logger.error(
                f"Erro ao buscar recompensas do usuário {user_id}: {str(e)}")
            return {
                "items": [],
                "total": 0
            }

    def get_today_reward_count(self, db: Session, user_id: str) -> int:
        """
        Conta quantas recompensas o usuário recebeu hoje.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário

        Returns:
            Número de recompensas recebidas hoje
        """
        try:
            # Obter a data de hoje (sem a hora)
            today = datetime.utcnow().date()

            # Consultar recompensas de hoje
            count = db.query(AdReward)\
                .filter(
                    AdReward.user_id == user_id,
                    func.date(AdReward.watched_at) == today
            )\
                .count()

            return count

        except Exception as e:
            logger.error(
                f"Erro ao contar recompensas do dia para o usuário {user_id}: {str(e)}")
            return 0

    def can_receive_reward(self, db: Session, user_id: str, max_daily: int = 3) -> bool:
        """
        Verifica se o usuário pode receber mais recompensas hoje.

        Args:
            db: Sessão do banco de dados
            user_id: ID do usuário
            max_daily: Máximo de recompensas diárias (padrão: 3)

        Returns:
            True se o usuário pode receber mais recompensas, False caso contrário
        """
        # Contar recompensas do dia
        today_count = self.get_today_reward_count(db, user_id)

        # Verificar se está abaixo do limite
        return today_count < max_daily

    def get_user_ad_rewards(self, user_id: str) -> List[AdReward]:
        """
        Obtém todas as recompensas por anúncios de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de recompensas por anúncios
        """
        logger.info(
            f"Buscando recompensas por anúncios para usuário {user_id}")

        return self.db.query(AdReward).filter(AdReward.user_id == user_id).all()

    def get_user_ad_rewards_today(self, user_id: str) -> List[AdReward]:
        """
        Obtém as recompensas por anúncios de um usuário para o dia atual.

        Args:
            user_id: ID do usuário

        Returns:
            Lista de recompensas por anúncios do dia
        """
        logger.info(
            f"Buscando recompensas por anúncios de hoje para usuário {user_id}")

        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        return (
            self.db.query(AdReward)
            .filter(
                AdReward.user_id == user_id,
                AdReward.created_at >= start_of_day,
                AdReward.created_at <= end_of_day
            )
            .all()
        )

    def get_user_ad_rewards_count_today(self, user_id: str) -> int:
        """
        Obtém a contagem de recompensas por anúncios de um usuário para o dia atual.

        Args:
            user_id: ID do usuário

        Returns:
            Contagem de recompensas por anúncios do dia
        """
        logger.info(
            f"Contando recompensas por anúncios de hoje para usuário {user_id}")

        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        return (
            self.db.query(AdReward)
            .filter(
                AdReward.user_id == user_id,
                AdReward.created_at >= start_of_day,
                AdReward.created_at <= end_of_day
            )
            .count()
        )

    def get_user_rewards_by_type(self, user_id: str, reward_type: str) -> List[AdReward]:
        """
        Obtém as recompensas por anúncios de um usuário por tipo de recompensa.

        Args:
            user_id: ID do usuário
            reward_type: Tipo de recompensa (chat_messages, study_content, etc.)

        Returns:
            Lista de recompensas por anúncios do tipo especificado
        """
        logger.info(
            f"Buscando recompensas do tipo {reward_type} para usuário {user_id}")

        return (
            self.db.query(AdReward)
            .filter(
                AdReward.user_id == user_id,
                AdReward.reward_type == reward_type
            )
            .all()
        )

    def get_user_rewards_by_type_today(self, user_id: str, reward_type: str) -> List[AdReward]:
        """
        Obtém as recompensas por anúncios de um usuário por tipo de recompensa para o dia atual.

        Args:
            user_id: ID do usuário
            reward_type: Tipo de recompensa (chat_messages, study_content, etc.)

        Returns:
            Lista de recompensas por anúncios do tipo especificado para o dia atual
        """
        logger.info(
            f"Buscando recompensas do tipo {reward_type} para hoje para usuário {user_id}")

        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        return (
            self.db.query(AdReward)
            .filter(
                AdReward.user_id == user_id,
                AdReward.reward_type == reward_type,
                AdReward.created_at >= start_of_day,
                AdReward.created_at <= end_of_day
            )
            .all()
        )

    def get_total_rewards_value_by_type_today(self, user_id: str, reward_type: str) -> int:
        """
        Obtém o valor total de recompensas por anúncios de um usuário por tipo de recompensa para o dia atual.

        Args:
            user_id: ID do usuário
            reward_type: Tipo de recompensa (chat_messages, study_content, etc.)

        Returns:
            Valor total de recompensas por anúncios do tipo especificado para o dia atual
        """
        logger.info(
            f"Calculando valor total de recompensas do tipo {reward_type} para hoje para usuário {user_id}")

        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        result = (
            self.db.query(AdReward)
            .filter(
                AdReward.user_id == user_id,
                AdReward.reward_type == reward_type,
                AdReward.created_at >= start_of_day,
                AdReward.created_at <= end_of_day
            )
            .with_entities(AdReward.reward_value)
            .all()
        )

        total = sum(reward.reward_value for reward in result) if result else 0
        logger.info(
            f"Total de recompensas do tipo {reward_type} para hoje para usuário {user_id}: {total}")

        return total
