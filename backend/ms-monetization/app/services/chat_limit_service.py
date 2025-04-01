import logging
from typing import Optional
from datetime import datetime
from app.services.redis_client import RedisClient
from app.services.auth_service import AuthService
from app.services.subscription_service import SubscriptionService
from app.models.subscription import SubscriptionStatus

logger = logging.getLogger(__name__)

# Constantes para limites de mensagens
DEFAULT_FREE_LIMIT = 5  # Número padrão de mensagens para usuários Free
DEFAULT_REWARD_LIMIT = 5  # Número padrão de mensagens por recompensa


class ChatLimitService:
    """
    Serviço para gerenciar os limites de mensagens do chat.

    Este serviço usa o Redis para armazenar e gerenciar os limites diários de mensagens
    dos usuários do plano Free, permitindo que assistam anúncios para ganhar mais mensagens.
    """

    def __init__(self, redis_client: RedisClient):
        """Inicializa o serviço de limite de chat."""
        self.redis = redis_client
        logger.info("ChatLimitService inicializado")

    async def get_user_chat_limit(self, user_id: str) -> int:
        """
        Obtém o limite atual de mensagens de um usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Número de mensagens disponíveis para o usuário
        """
        key = f"chat_limit:{user_id}"
        value = self.redis.get(key)
        return int(value) if value else 0

    async def is_premium_user(self, user_id: str, subscription_service: SubscriptionService) -> bool:
        """
        Verifica se o usuário possui assinatura premium.

        Args:
            user_id: ID do usuário
            subscription_service: Serviço de assinatura para consulta

        Returns:
            True se o usuário for premium, False caso contrário
        """
        # Obter assinatura atual do usuário
        subscription = subscription_service.get_current_subscription(user_id)

        # Verificar se existe e está ativa
        return (
            subscription is not None and
            subscription.status == SubscriptionStatus.ACTIVE
        )

    async def check_limit(self, user_id: str, subscription_service: SubscriptionService) -> dict:
        """
        Verifica o limite de mensagens de um usuário.

        Args:
            user_id: ID do usuário
            subscription_service: Serviço de assinatura para consulta

        Returns:
            Dicionário com status do limite e mensagens disponíveis
        """
        # Verificar se o usuário é premium
        is_premium = await self.is_premium_user(user_id, subscription_service)

        if is_premium:
            # Usuários premium têm acesso ilimitado
            return {
                "has_limit": True,
                "is_premium": True,
                "available_messages": -1,  # -1 indica ilimitado
                "message": "Você tem acesso ilimitado ao chat como usuário Premium."
            }

        # Para usuários Free, verificar limite no Redis
        available = await self.get_user_chat_limit(user_id)

        if available <= 0:
            # Verificar se já foi configurado hoje
            # Se não foi, definir o limite padrão
            key = f"chat_limit:{user_id}"
            if not self.redis.exists(key):
                # Configurar limite padrão para hoje
                available = await self.initialize_daily_limit(user_id)

                return {
                    "has_limit": True,
                    "is_premium": False,
                    "available_messages": available,
                    "message": f"Seu limite diário foi renovado. Você tem {available} mensagens disponíveis hoje."
                }

            # Se já foi configurado e está zerado, não há mais mensagens disponíveis
            return {
                "has_limit": False,
                "is_premium": False,
                "available_messages": 0,
                "message": "Você atingiu seu limite diário. Assista a um anúncio para ganhar mais mensagens ou faça upgrade para Premium."
            }

        # Usuário Free com mensagens disponíveis
        return {
            "has_limit": True,
            "is_premium": False,
            "available_messages": available,
            "message": f"Você tem {available} mensagens disponíveis hoje."
        }

    async def decrement_limit(self, user_id: str, subscription_service: SubscriptionService) -> dict:
        """
        Decrementa o limite de mensagens de um usuário após uso.

        Args:
            user_id: ID do usuário
            subscription_service: Serviço de assinatura para consulta

        Returns:
            Dicionário com resultado da operação
        """
        # Verificar se o usuário é premium
        is_premium = await self.is_premium_user(user_id, subscription_service)

        if is_premium:
            # Usuários premium não têm limite
            return {
                "success": True,
                "is_premium": True,
                "available_messages": -1,
                "message": "Mensagem enviada com sucesso."
            }

        # Para usuários Free, verificar e decrementar limite no Redis
        available = await self.get_user_chat_limit(user_id)

        if available <= 0:
            # Verificar se já foi configurado hoje
            key = f"chat_limit:{user_id}"
            if not self.redis.exists(key):
                # Configurar limite padrão para hoje
                available = await self.initialize_daily_limit(user_id)

                # Decrementar o limite
                new_limit = self.redis.decrement(key)

                return {
                    "success": True,
                    "is_premium": False,
                    "available_messages": new_limit,
                    "message": "Mensagem enviada com sucesso."
                }

            # Se já foi configurado e está zerado, não há mais mensagens disponíveis
            return {
                "success": False,
                "is_premium": False,
                "available_messages": 0,
                "message": "Você atingiu seu limite diário. Assista a um anúncio para ganhar mais mensagens ou faça upgrade para Premium."
            }

        # Decrementar o limite
        key = f"chat_limit:{user_id}"
        new_limit = self.redis.decrement(key)

        return {
            "success": True,
            "is_premium": False,
            "available_messages": new_limit,
            "message": "Mensagem enviada com sucesso."
        }

    async def increment_limit_from_ad(self, user_id: str, messages: int = DEFAULT_REWARD_LIMIT) -> dict:
        """
        Incrementa o limite de mensagens após o usuário assistir a um anúncio.

        Args:
            user_id: ID do usuário
            messages: Número de mensagens a adicionar (padrão: 5)

        Returns:
            Dicionário com resultado da operação
        """
        key = f"chat_limit:{user_id}"

        if not self.redis.exists(key):
            # Se a chave não existe, criar com o valor de recompensa
            # e definir a expiração para o final do dia
            success = await self.initialize_daily_limit(user_id, initial_value=messages)
            if not success:
                return {
                    "success": False,
                    "available_messages": 0,
                    "message": "Erro ao registrar recompensa. Tente novamente."
                }

            return {
                "success": True,
                "available_messages": messages,
                "message": f"Você ganhou {messages} mensagens adicionais de chat!"
            }

        # Incrementar o limite existente
        new_limit = self.redis.increment(key, messages)

        return {
            "success": True,
            "available_messages": new_limit,
            "message": f"Você ganhou {messages} mensagens adicionais de chat!"
        }

    async def initialize_daily_limit(self, user_id: str, initial_value: int = DEFAULT_FREE_LIMIT) -> int:
        """
        Inicializa o limite diário de mensagens para um usuário.

        Args:
            user_id: ID do usuário
            initial_value: Valor inicial do limite (padrão: 5)

        Returns:
            Novo limite de mensagens ou 0 se falhar
        """
        key = f"chat_limit:{user_id}"

        # Calcular tempo até o final do dia
        now = datetime.utcnow()
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)
        seconds_until_eod = int((end_of_day - now).total_seconds())

        # Definir o limite com expiração no final do dia
        success = self.redis.set(key, str(initial_value), seconds_until_eod)

        if success:
            logger.info(
                f"Limite diário de chat inicializado para usuário {user_id}: {initial_value}")
            return initial_value
        else:
            logger.error(
                f"Erro ao inicializar limite diário para usuário {user_id}")
            return 0
