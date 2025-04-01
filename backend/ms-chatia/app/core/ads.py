"""
Serviço de anúncios do sistema FaleComJesus.

Este módulo implementa a integração com redes publicitárias,
gerenciando exibição, recompensas e limites de anúncios.

Features:
    - Integração com Google AdSense
    - Integração com AdMob
    - Recompensas por visualização
    - Controle de limites
    - Métricas de performance
    - Fallback automático
"""

from typing import Dict, List, Optional, Union
import logging
import json
import requests
from datetime import datetime, timedelta
from .config import settings
from .cache import cache
from .metrics import metrics
from .payment import payment

# Logger
logger = logging.getLogger(__name__)


class AdsManager:
    """
    Gerenciador de anúncios e recompensas.

    Features:
        - Múltiplas redes
        - Recompensas configuráveis
        - Controle de limites
        - Métricas
        - Fallback

    Attributes:
        ad_config: Config das redes
        metrics: Métricas de anúncios
    """

    def __init__(
        self,
        ad_client: Optional[str] = None,
        ad_slot: Optional[str] = None,
        admob_app: Optional[str] = None,
        admob_banner: Optional[str] = None,
        admob_reward: Optional[str] = None
    ):
        """
        Inicializa o gerenciador de anúncios.

        Args:
            ad_client: Client ID AdSense
            ad_slot: Slot ID AdSense
            admob_app: App ID AdMob
            admob_banner: Banner ID AdMob
            admob_reward: Reward ID AdMob
        """
        # Configuração AdSense
        self.ad_config = {
            "client": ad_client or settings.ADSENSE_CLIENT_ID,
            "slot": ad_slot or settings.ADSENSE_SLOT_ID
        }

        # Configuração AdMob
        self.admob_config = {
            "app_id": admob_app or settings.ADMOB_APP_ID,
            "banner_id": admob_banner or settings.ADMOB_BANNER_ID,
            "reward_id": admob_reward or settings.ADMOB_REWARD_ID
        }

        logger.info("Gerenciador de anúncios inicializado")

    async def get_ad_unit(
        self,
        ad_type: str,
        user_id: str,
        is_premium: bool = False
    ) -> Dict:
        """
        Obtém unidade de anúncio.

        Args:
            ad_type: Tipo do anúncio
            user_id: ID do usuário
            is_premium: Se é usuário premium

        Returns:
            Dict: Dados do anúncio

        Example:
            ad = await ads.get_ad_unit(
                ad_type="banner",
                user_id="123",
                is_premium=False
            )
        """
        try:
            # Premium não vê anúncios
            if is_premium:
                return {"type": "none"}

            # Verifica limite diário
            if not await self._check_daily_limit(user_id):
                return {"type": "limit_reached"}

            # Obtém anúncio
            if ad_type == "banner":
                return await self._get_banner_ad()

            elif ad_type == "reward":
                return await self._get_reward_ad()

            else:
                raise ValueError(f"Tipo inválido: {ad_type}")

        except Exception as e:
            logger.error(f"Erro ao obter anúncio: {str(e)}")
            return {"type": "error"}

    async def register_ad_view(
        self,
        user_id: str,
        ad_id: str,
        ad_type: str,
        reward_type: str,
        reward_value: int
    ) -> bool:
        """
        Registra visualização de anúncio.

        Args:
            user_id: ID do usuário
            ad_id: ID do anúncio
            ad_type: Tipo do anúncio
            reward_type: Tipo da recompensa
            reward_value: Valor da recompensa

        Returns:
            bool: True se registrado
        """
        try:
            # Verifica limite
            if not await self._check_daily_limit(user_id):
                return False

            # Registra visualização
            await self._save_ad_view(
                user_id,
                ad_id,
                ad_type,
                reward_type,
                reward_value
            )

            # Registra métricas
            metrics.track_ad(
                "ad_viewed",
                ad_type=ad_type,
                reward_type=reward_type
            )

            return True

        except Exception as e:
            logger.error(f"Erro ao registrar visualização: {str(e)}")
            return False

    async def get_remaining_ads(
        self,
        user_id: str
    ) -> Dict:
        """
        Obtém anúncios restantes.

        Args:
            user_id: ID do usuário

        Returns:
            Dict: Limites e contadores
        """
        try:
            # Cache de contadores
            cache_key = f"ads:count:{user_id}"
            counters = await cache.get(cache_key)

            if not counters:
                counters = {
                    "banner": 0,
                    "reward": 0,
                    "total": 0
                }

            # Limites diários
            limits = {
                "banner": settings.ADS_DAILY_LIMIT_BANNER,
                "reward": settings.ADS_DAILY_LIMIT_REWARD,
                "total": settings.ADS_DAILY_LIMIT_TOTAL
            }

            # Calcula restantes
            remaining = {
                "banner": limits["banner"] - counters["banner"],
                "reward": limits["reward"] - counters["reward"],
                "total": limits["total"] - counters["total"]
            }

            return remaining

        except Exception as e:
            logger.error(f"Erro ao obter restantes: {str(e)}")
            return {
                "banner": 0,
                "reward": 0,
                "total": 0
            }

    async def _check_daily_limit(
        self,
        user_id: str
    ) -> bool:
        """
        Verifica limite diário de anúncios.

        Args:
            user_id: ID do usuário

        Returns:
            bool: True se dentro do limite
        """
        try:
            # Cache de contadores
            cache_key = f"ads:count:{user_id}"
            counters = await cache.get(cache_key)

            if not counters:
                return True

            # Verifica limites
            if counters["total"] >= settings.ADS_DAILY_LIMIT_TOTAL:
                return False

            return True

        except Exception as e:
            logger.error(f"Erro ao verificar limite: {str(e)}")
            return False

    async def _save_ad_view(
        self,
        user_id: str,
        ad_id: str,
        ad_type: str,
        reward_type: str,
        reward_value: int
    ) -> None:
        """
        Salva visualização de anúncio.

        Args:
            user_id: ID do usuário
            ad_id: ID do anúncio
            ad_type: Tipo do anúncio
            reward_type: Tipo da recompensa
            reward_value: Valor da recompensa
        """
        try:
            # Cache de contadores
            cache_key = f"ads:count:{user_id}"
            counters = await cache.get(cache_key)

            if not counters:
                counters = {
                    "banner": 0,
                    "reward": 0,
                    "total": 0
                }

            # Atualiza contadores
            counters[ad_type] += 1
            counters["total"] += 1

            # Salva no cache
            await cache.set(
                cache_key,
                counters,
                expire=86400  # 24h
            )

            # Salva no banco
            await self._save_to_db(
                user_id,
                ad_id,
                ad_type,
                reward_type,
                reward_value
            )

        except Exception as e:
            logger.error(f"Erro ao salvar visualização: {str(e)}")

    async def _get_banner_ad(self) -> Dict:
        """
        Obtém anúncio banner.

        Returns:
            Dict: Dados do banner
        """
        try:
            # AdSense
            if settings.USE_ADSENSE:
                return {
                    "type": "adsense",
                    "client": self.ad_config["client"],
                    "slot": self.ad_config["slot"]
                }

            # AdMob
            elif settings.USE_ADMOB:
                return {
                    "type": "admob",
                    "app_id": self.admob_config["app_id"],
                    "banner_id": self.admob_config["banner_id"]
                }

            # Fallback
            else:
                return {"type": "none"}

        except Exception as e:
            logger.error(f"Erro ao obter banner: {str(e)}")
            return {"type": "none"}

    async def _get_reward_ad(self) -> Dict:
        """
        Obtém anúncio recompensado.

        Returns:
            Dict: Dados do anúncio
        """
        try:
            # AdMob Reward
            if settings.USE_ADMOB:
                return {
                    "type": "admob_reward",
                    "app_id": self.admob_config["app_id"],
                    "reward_id": self.admob_config["reward_id"]
                }

            # Fallback
            else:
                return {"type": "none"}

        except Exception as e:
            logger.error(f"Erro ao obter reward: {str(e)}")
            return {"type": "none"}


# Instância global de anúncios
ads = AdsManager()
