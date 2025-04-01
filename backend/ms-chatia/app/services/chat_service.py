from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.cache import ChatCache
from app.core.config import get_settings
from app.core.logging import get_logger
from app.services.openai_service import OpenAIService
from app.models.chat import ChatHistory
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    RemainingMessagesResponse,
    AdRewardResponse,
    StudyPlanRequest,
    StudyPlanResponse,
    ChatMessageCreate
)

logger = get_logger(__name__)
settings = get_settings()


class ChatService:
    """
    Serviço para gerenciamento do chat com IA.

    Responsável por:
    - Processar mensagens do usuário
    - Gerar respostas via OpenAI
    - Armazenar histórico
    - Controlar limites de uso

    Attributes:
        db: Sessão do banco de dados
        openai: Serviço da OpenAI
        redis: Cliente Redis para cache
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço de chat.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.openai = OpenAIService()
        self.chat_cache = ChatCache()
        self.settings = settings

    async def send_message(
        self,
        user_id: UUID,
        message: ChatMessageCreate
    ) -> Dict:
        """
        Processa mensagem e gera resposta.

        Args:
            user_id: ID do usuário
            message: Dados da mensagem

        Returns:
            Dict com resposta da IA

        Raises:
            HTTPException: Se erro no processamento
        """
        try:
            # Verifica limite diário
            if not await self.check_daily_limit(user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Limite diário de mensagens atingido"
                )

            # Busca histórico recente
            history = await self.get_recent_history(user_id)

            # Gera resposta
            response = await self.openai.generate_response(
                message=message.message,
                history=history,
                context={
                    "user_id": str(user_id),
                    "study_section_id": str(message.study_section_id) if message.study_section_id else None,
                    "verse_id": str(message.verse_id) if message.verse_id else None
                }
            )

            # Salva no histórico
            chat_message = ChatHistory(
                user_id=user_id,
                message=message.message,
                response=response["text"],
                study_section_id=message.study_section_id,
                verse_id=message.verse_id,
                created_at=datetime.utcnow()
            )

            self.db.add(chat_message)
            self.db.commit()
            self.db.refresh(chat_message)

            return {
                "id": chat_message.id,
                "message": chat_message.message,
                "response": chat_message.response,
                "created_at": chat_message.created_at
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar mensagem"
            )

    async def get_message(
        self,
        message_id: UUID,
        user_id: UUID
    ) -> Optional[Dict]:
        """
        Retorna detalhes da mensagem.

        Args:
            message_id: ID da mensagem
            user_id: ID do usuário

        Returns:
            Dict com detalhes ou None

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            message = self.db.query(ChatHistory).filter(
                ChatHistory.id == message_id,
                ChatHistory.user_id == user_id
            ).first()

            if not message:
                return None

            return {
                "id": message.id,
                "message": message.message,
                "response": message.response,
                "study_section_id": message.study_section_id,
                "verse_id": message.verse_id,
                "created_at": message.created_at
            }

        except Exception as e:
            logger.error(f"Error getting message: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar mensagem"
            )

    async def list_messages(
        self,
        user_id: UUID,
        study_section_id: Optional[UUID] = None,
        verse_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict]:
        """
        Lista mensagens com filtros.

        Args:
            user_id: ID do usuário
            study_section_id: Filtro por seção
            verse_id: Filtro por versículo
            start_date: Data inicial
            end_date: Data final
            limit: Limite de registros
            offset: Deslocamento

        Returns:
            Lista de mensagens

        Raises:
            HTTPException: Se erro na listagem
        """
        try:
            # Query base
            query = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            )

            # Aplica filtros
            if study_section_id:
                query = query.filter(
                    ChatHistory.study_section_id == study_section_id)

            if verse_id:
                query = query.filter(ChatHistory.verse_id == verse_id)

            if start_date:
                query = query.filter(ChatHistory.created_at >= start_date)

            if end_date:
                query = query.filter(ChatHistory.created_at <= end_date)

            # Ordena e pagina
            messages = query.order_by(
                ChatHistory.created_at.desc()
            ).offset(offset).limit(limit).all()

            return [{
                "id": m.id,
                "message": m.message,
                "response": m.response,
                "study_section_id": m.study_section_id,
                "verse_id": m.verse_id,
                "created_at": m.created_at
            } for m in messages]

        except Exception as e:
            logger.error(f"Error listing messages: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao listar mensagens"
            )

    async def get_recent_history(
        self,
        user_id: UUID,
        limit: int = 5
    ) -> List[Dict]:
        """
        Retorna histórico recente.

        Args:
            user_id: ID do usuário
            limit: Limite de mensagens

        Returns:
            Lista de mensagens

        Raises:
            HTTPException: Se erro na busca
        """
        try:
            messages = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).order_by(
                ChatHistory.created_at.desc()
            ).limit(limit).all()

            return [{
                "role": "user" if i % 2 == 0 else "assistant",
                "content": m.message if i % 2 == 0 else m.response
            } for i, m in enumerate(reversed(messages))]

        except Exception as e:
            logger.error(f"Error getting history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar histórico"
            )

    async def check_daily_limit(
        self,
        user_id: UUID
    ) -> bool:
        """
        Verifica limite diário de mensagens.

        Args:
            user_id: ID do usuário

        Returns:
            True se ainda pode enviar mensagens

        Raises:
            HTTPException: Se erro na verificação
        """
        try:
            today = datetime.utcnow().date()

            # Conta mensagens do dia
            count = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id,
                ChatHistory.created_at >= today
            ).count()

            return count < settings.MAX_DAILY_MESSAGES

        except Exception as e:
            logger.error(f"Error checking limit: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar limite"
            )

    async def get_message_stats(
        self,
        user_id: UUID
    ) -> Dict:
        """
        Retorna estatísticas de uso.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com estatísticas

        Raises:
            HTTPException: Se erro no cálculo
        """
        try:
            today = datetime.utcnow().date()
            week_ago = datetime.utcnow() - timedelta(days=7)

            # Total de mensagens
            total = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).count()

            # Mensagens hoje
            today_count = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id,
                ChatHistory.created_at >= today
            ).count()

            # Mensagens na semana
            week_count = self.db.query(ChatHistory).filter(
                ChatHistory.user_id == user_id,
                ChatHistory.created_at >= week_ago
            ).count()

            return {
                "total_messages": total,
                "messages_today": today_count,
                "messages_week": week_count,
                "daily_limit": settings.MAX_DAILY_MESSAGES,
                "remaining_today": settings.MAX_DAILY_MESSAGES - today_count
            }

        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao calcular estatísticas"
            )

    async def process_chat_message(
        self,
        user_id: UUID,
        message: ChatMessageRequest,
        is_premium: bool = False
    ) -> ChatMessageResponse:
        """
        Processa uma mensagem do usuário e retorna resposta da IA.

        Args:
            user_id: ID do usuário
            message: Mensagem e contexto
            is_premium: Se o usuário é premium

        Returns:
            ChatMessageResponse com resposta da IA

        Raises:
            HTTPException: Se limite excedido ou erro no processamento
        """
        try:
            # Verificar limite (se não for premium)
            if not is_premium:
                remaining = await self.get_remaining_messages(user_id)
                if remaining <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Limite diário de mensagens atingido"
                    )

            # Verificar cache
            cached = await self.chat_cache.get_cached_response(
                user_id=user_id,
                message=message.message
            )
            if cached:
                logger.info(f"Cache hit for message from user {user_id}")
                return cached

            # Buscar histórico recente
            history = await self.get_recent_history(user_id)

            # Gerar resposta via OpenAI
            response = await self.openai.generate_response(
                message=message.message,
                context=message.context,
                history=history
            )

            # Salvar no histórico
            await self.save_chat_history(
                user_id=user_id,
                message=message.message,
                response=response
            )

            # Decrementar contador (se não for premium)
            if not is_premium:
                await self.decrement_message_count(user_id)

            # Salvar no cache
            await self.chat_cache.cache_response(
                user_id=user_id,
                message=message.message,
                response=response
            )

            return response

        except HTTPException as e:
            # Repassar erros HTTP
            raise e
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar mensagem"
            )

    async def get_chat_history(
        self,
        user_id: UUID,
        limit: int = 50,
        skip: int = 0
    ) -> ChatHistoryResponse:
        """
        Retorna histórico de chat do usuário com paginação.

        Args:
            user_id: ID do usuário
            limit: Máximo de mensagens
            skip: Mensagens para pular

        Returns:
            ChatHistoryResponse com lista paginada
        """
        try:
            # Buscar do banco
            history = await ChatHistory.get_user_history(
                user_id=user_id,
                limit=limit,
                skip=skip
            )

            return ChatHistoryResponse(
                items=history.items,
                total=history.total,
                limit=limit,
                skip=skip
            )

        except Exception as e:
            logger.error(f"Error fetching history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar histórico"
            )

    async def get_message_limit(
        self,
        user_id: UUID
    ) -> RemainingMessagesResponse:
        """
        Retorna informações sobre limite de mensagens.

        Args:
            user_id: ID do usuário

        Returns:
            RemainingMessagesResponse com limite atual
        """
        try:
            remaining = await self.get_remaining_messages(user_id)
            reset_time = await self.get_limit_reset_time(user_id)

            return RemainingMessagesResponse(
                always_unlimited=False,
                remaining_messages=remaining,
                reset_time=reset_time
            )

        except Exception as e:
            logger.error(f"Error checking limit: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao verificar limite"
            )

    async def add_bonus_messages(
        self,
        user_id: UUID
    ) -> AdRewardResponse:
        """
        Adiciona mensagens bônus após assistir anúncio.

        Args:
            user_id: ID do usuário

        Returns:
            AdRewardResponse com novo limite

        Raises:
            HTTPException: Se máximo de bônus atingido
        """
        try:
            # Verificar bônus restantes
            remaining_rewards = await self.get_remaining_rewards(user_id)
            if remaining_rewards <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Máximo de bônus diários atingido"
                )

            # Adicionar 5 mensagens
            await self.increment_message_count(
                user_id=user_id,
                amount=5
            )

            # Decrementar bônus
            await self.decrement_reward_count(user_id)

            # Retornar novo status
            remaining = await self.get_remaining_messages(user_id)
            rewards = await self.get_remaining_rewards(user_id)

            return AdRewardResponse(
                messages_added=5,
                remaining_messages=remaining,
                remaining_rewards=rewards
            )

        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error adding bonus: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar bônus"
            )

    async def generate_study_plan(
        self,
        user_id: UUID,
        preferences: StudyPlanRequest
    ) -> StudyPlanResponse:
        """
        Gera plano de estudo personalizado.

        Args:
            user_id: ID do usuário
            preferences: Preferências do usuário

        Returns:
            StudyPlanResponse com plano gerado
        """
        try:
            # Gerar plano via OpenAI
            plan = await self.openai.generate_study_plan(
                user_id=user_id,
                preferences=preferences
            )

            # Salvar no banco
            saved_plan = await self.save_study_plan(
                user_id=user_id,
                plan=plan
            )

            return saved_plan

        except Exception as e:
            logger.error(f"Error generating plan: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao gerar plano de estudo"
            )

    # Métodos auxiliares

    async def get_remaining_messages(self, user_id: UUID) -> int:
        """Retorna número de mensagens restantes"""
        key = f"chat:limit:{user_id}"
        count = await self.chat_cache.get(key) or 0
        return self.settings.DAILY_MESSAGE_LIMIT - count

    async def get_limit_reset_time(self, user_id: UUID) -> datetime:
        """Retorna horário de reset do limite"""
        key = f"chat:limit:{user_id}"
        ttl = await self.chat_cache.get_ttl(key)
        return datetime.utcnow() + timedelta(seconds=ttl)

    async def get_remaining_rewards(self, user_id: UUID) -> int:
        """Retorna número de recompensas restantes"""
        key = f"chat:rewards:{user_id}"
        count = await self.chat_cache.get(key) or 0
        return self.settings.DAILY_REWARD_LIMIT - count

    async def increment_message_count(
        self,
        user_id: UUID,
        amount: int = 1
    ):
        """Incrementa contador de mensagens"""
        key = f"chat:limit:{user_id}"
        await self.chat_cache.increment(key, amount)

    async def decrement_message_count(self, user_id: UUID):
        """Decrementa contador de mensagens"""
        key = f"chat:limit:{user_id}"
        await self.chat_cache.increment(key)

    async def decrement_reward_count(self, user_id: UUID):
        """Decrementa contador de recompensas"""
        key = f"chat:rewards:{user_id}"
        await self.chat_cache.increment(key)

    async def save_chat_history(
        self,
        user_id: UUID,
        message: str,
        response: ChatMessageResponse
    ):
        """Salva mensagem no histórico"""
        await ChatHistory.create(
            user_id=user_id,
            message=message,
            response=response.message,
            verses=response.verses,
            suggestions=response.suggestions
        )
