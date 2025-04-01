"""
Serviço de métricas do sistema FaleComJesus.

Este módulo implementa o sistema de métricas da aplicação,
incluindo coleta, agregação e visualização de dados.

Features:
    - Métricas de usuários
    - Métricas de estudos
    - Métricas de chat
    - Métricas de gamificação
    - Métricas de monetização
    - Métricas de performance
"""

from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
from .database import db
from .logger import logger


class MetricsManager:
    """
    Gerenciador de métricas.

    Features:
        - Tracking de eventos
        - Agregação de dados
        - Relatórios
        - Alertas

    Attributes:
        metrics: Dicionário de métricas
        alerts: Lista de alertas
        reports: Lista de relatórios
    """

    def __init__(self):
        """
        Inicializa o gerenciador.
        """
        # Métricas
        self.metrics = {
            "users": {},
            "studies": {},
            "chat": {},
            "gamification": {},
            "monetization": {},
            "performance": {}
        }

        # Alertas
        self.alerts = []

        # Relatórios
        self.reports = []

    async def track_user(
        self,
        user_id: str,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de usuário.

        Args:
            user_id: ID do usuário
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "user_id": user_id,
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO user_metrics (
                    user_id, event, data, timestamp
                ) VALUES (
                    :user_id, :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"user_metric:{user_id}:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar usuário: {str(e)}")

    async def track_study(
        self,
        user_id: str,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de estudo.

        Args:
            user_id: ID do usuário
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "user_id": user_id,
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO study_metrics (
                    user_id, event, data, timestamp
                ) VALUES (
                    :user_id, :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"study_metric:{user_id}:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar estudo: {str(e)}")

    async def track_chat(
        self,
        user_id: str,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de chat.

        Args:
            user_id: ID do usuário
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "user_id": user_id,
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO chat_metrics (
                    user_id, event, data, timestamp
                ) VALUES (
                    :user_id, :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"chat_metric:{user_id}:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar chat: {str(e)}")

    async def track_gamification(
        self,
        user_id: str,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de gamificação.

        Args:
            user_id: ID do usuário
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "user_id": user_id,
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO gamification_metrics (
                    user_id, event, data, timestamp
                ) VALUES (
                    :user_id, :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"gamification_metric:{user_id}:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar gamificação: {str(e)}")

    async def track_monetization(
        self,
        user_id: str,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de monetização.

        Args:
            user_id: ID do usuário
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "user_id": user_id,
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO monetization_metrics (
                    user_id, event, data, timestamp
                ) VALUES (
                    :user_id, :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"monetization_metric:{user_id}:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar monetização: {str(e)}")

    async def track_performance(
        self,
        event: str,
        data: Optional[Dict] = None
    ) -> None:
        """
        Registra evento de performance.

        Args:
            event: Nome do evento
            data: Dados do evento
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            # Prepara dados
            metric = {
                "event": event,
                "data": data or {},
                "timestamp": datetime.utcnow()
            }

            # Salva no banco
            await db.execute(
                """
                INSERT INTO performance_metrics (
                    event, data, timestamp
                ) VALUES (
                    :event, :data, :timestamp
                )
                """,
                metric
            )

            # Atualiza cache
            await cache.set(
                f"performance_metric:{event}",
                metric,
                expire=3600  # 1 hora
            )

        except Exception as e:
            logger.error(f"Erro ao trackar performance: {str(e)}")

    async def get_metrics(
        self,
        category: Optional[str] = None,
        period: Optional[str] = None
    ) -> Dict:
        """
        Retorna métricas.

        Args:
            category: Categoria (users, studies, etc)
            period: Período (day, week, month)

        Returns:
            Dict: Métricas
        """
        try:
            # Filtra categoria
            if category:
                metrics = self.metrics.get(category, {})
            else:
                metrics = self.metrics

            # Filtra período
            if period:
                now = datetime.utcnow()
                if period == "day":
                    start = now - timedelta(days=1)
                elif period == "week":
                    start = now - timedelta(weeks=1)
                elif period == "month":
                    start = now - timedelta(days=30)
                else:
                    start = now - timedelta(days=1)

                # Filtra por data
                filtered = {}
                for key, value in metrics.items():
                    if isinstance(value, dict) and "timestamp" in value:
                        if value["timestamp"] >= start:
                            filtered[key] = value
                metrics = filtered

            return metrics

        except Exception as e:
            logger.error(f"Erro ao obter métricas: {str(e)}")
            return {}

    async def check_alerts(self) -> List[Dict]:
        """
        Verifica alertas configurados.

        Returns:
            List[Dict]: Lista de alertas
        """
        try:
            triggered = []

            # Verifica cada alerta
            for alert in self.alerts:
                # Obtém métrica
                metric = await self.get_metrics(
                    category=alert["category"],
                    period=alert["period"]
                )

                # Verifica condição
                if alert["condition"](metric):
                    triggered.append(alert)

            return triggered

        except Exception as e:
            logger.error(f"Erro ao verificar alertas: {str(e)}")
            return []

    async def generate_report(
        self,
        metrics: List[str],
        period: str = "day"
    ) -> Dict:
        """
        Gera relatório.

        Args:
            metrics: Lista de métricas
            period: Período (day, week, month)

        Returns:
            Dict: Relatório
        """
        try:
            report = {
                "timestamp": datetime.utcnow(),
                "period": period,
                "metrics": {}
            }

            # Coleta métricas
            for metric in metrics:
                data = await self.get_metrics(
                    category=metric,
                    period=period
                )
                report["metrics"][metric] = data

            return report

        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {str(e)}")
            return {}

    async def close(self) -> None:
        """
        Fecha conexões.
        """
        try:
            # Importação local para evitar circularidade
            from .cache import cache

            await db.close()
            await cache.close()

        except Exception as e:
            logger.error(f"Erro ao fechar métricas: {str(e)}")


# Instância global de métricas
metrics = MetricsManager()
