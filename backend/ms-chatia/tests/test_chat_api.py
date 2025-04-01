import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
import json
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings
from app.core.redis import get_redis_client
from app.core.rate_limit import RateLimitData, RateLimitMiddleware, ChatRateLimiter

# Cliente de teste
client = TestClient(app)

# Mock do Redis para testes


class MockRedis:
    def __init__(self):
        self.data = {}
        self.ttl_data = {}

    async def get(self, key):
        return self.data.get(key)

    async def setex(self, key, ttl, value):
        self.data[key] = value
        self.ttl_data[key] = ttl

    async def incr(self, key):
        value = int(self.data.get(key, 0))
        self.data[key] = str(value + 1)
        return value + 1

    async def ttl(self, key):
        return self.ttl_data.get(key, 0)

    async def delete(self, key):
        if key in self.data:
            del self.data[key]
        if key in self.ttl_data:
            del self.ttl_data[key]

    async def scan_iter(self, pattern):
        for key in self.data.keys():
            if pattern.replace("*", "") in key:
                yield key

# Mock do OpenAI para testes


class MockOpenAI:
    async def create_chat_completion(self, *args, **kwargs):
        return {
            "choices": [
                {
                    "message": {
                        "content": "Resposta simulada da IA com referência bíblica João 14:27 e sugestão para ler sobre paz."
                    }
                }
            ]
        }

# Fixtures


@pytest.fixture
def mock_redis():
    return MockRedis()


@pytest.fixture
def mock_openai():
    return MockOpenAI()


@pytest.fixture
def auth_headers():
    return {
        "Authorization": "Bearer test_token",
        "User-Agent": "Test Browser"
    }

# Testes dos Endpoints


def test_health_check():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_rate_limit_middleware():
    """Testa o middleware de rate limit"""
    redis = MockRedis()
    middleware = RateLimitMiddleware(requests_per_minute=2)
    middleware.redis = redis

    # Primeira requisição
    result1 = await middleware.check_rate_limit("test_key", 2, 60)
    assert result1.allowed == True
    assert result1.remaining == 1
    assert result1.reset_in > 0

    # Segunda requisição
    result2 = await middleware.check_rate_limit("test_key", 2, 60)
    assert result2.allowed == True
    assert result2.remaining == 0

    # Terceira requisição (deve exceder limite)
    result3 = await middleware.check_rate_limit("test_key", 2, 60)
    assert result3.allowed == False
    assert result3.remaining == 0
    assert result3.retry_after is not None


@pytest.mark.asyncio
async def test_chat_message_success(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": "Como lidar com ansiedade?",
            "context": {
                "user_id": "test-user",
                "bible_experience": "iniciante",
                "preferred_topics": ["ansiedade", "paz"]
            }
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "references" in data
        assert "suggestions" in data
        assert "remaining_messages" in data
        assert "metadata" in data
        assert isinstance(data["references"], list)
        assert isinstance(data["suggestions"], list)
        assert isinstance(data["metadata"], dict)
        assert "João 14:27" in str(data["references"])


@pytest.mark.asyncio
async def test_chat_message_without_context(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": "Como ter mais fé?"
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["references"] == []
        assert isinstance(data["suggestions"], list)
        assert data["metadata"]["model"] == "gpt-3.5-turbo"


@pytest.mark.asyncio
async def test_chat_message_empty(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": ""
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 422  # Validação do Pydantic


@pytest.mark.asyncio
async def test_chat_history(mock_redis, auth_headers):
    response = client.get(
        "/api/chat/history?user_id=test-user-id",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert isinstance(data["items"], list)
    assert isinstance(data["count"], int)


@pytest.mark.asyncio
async def test_remaining_messages(mock_redis, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis):
        response = client.get(
            "/api/chat/remaining",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "remaining_messages" in data
        assert "limit" in data
        assert "reset_in" in data
        assert "can_watch_ad" in data
        assert isinstance(data["remaining_messages"], int)
        assert isinstance(data["limit"], int)
        assert isinstance(data["reset_in"], int)
        assert isinstance(data["can_watch_ad"], bool)


@pytest.mark.asyncio
async def test_ad_reward(mock_redis, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis):
        # Primeiro, verifica mensagens restantes
        initial = client.get(
            "/api/chat/remaining",
            headers=auth_headers
        )
        initial_remaining = initial.json()["remaining_messages"]

        # Assiste anúncio
        response = client.post(
            "/api/chat/ad-reward",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()

        # Verifica se ganhou mensagens
        assert data["remaining_messages"] > initial_remaining
        assert data["remaining_messages"] <= settings.CHAT_LIMIT_MAX_BONUS
        assert "limit" in data
        assert "reset_in" in data
        assert "can_watch_ad" in data


@pytest.mark.asyncio
async def test_chat_message_with_bible_reference(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": "O que a Bíblia diz sobre paz?",
            "context": {
                "user_id": "test-user",
                "bible_experience": "intermediário"
            }
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["references"]) > 0
        for ref in data["references"]:
            assert "reference" in ref
            assert "text" in ref


@pytest.mark.asyncio
async def test_chat_message_suggestions(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": "Como orar?",
            "context": {
                "user_id": "test-user",
                "bible_experience": "iniciante"
            }
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["suggestions"]) > 0
        for suggestion in data["suggestions"]:
            assert isinstance(suggestion, str)


@pytest.mark.asyncio
async def test_chat_message_metadata(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        message = {
            "message": "Como crescer na fé?",
            "context": {
                "user_id": "test-user",
                "bible_experience": "avançado"
            }
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        metadata = data["metadata"]
        assert "model" in metadata
        assert "processing_time" in metadata
        assert "token_count" in metadata
        assert isinstance(metadata["processing_time"], float)


@pytest.mark.asyncio
async def test_chat_message_limit_exceeded(mock_redis, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis):
        # Simular limite excedido
        limit_data = {
            "count": settings.CHAT_LIMIT_FREE_USERS,
            "bonus_used": 0,
            "reset_at": (datetime.utcnow() + timedelta(days=1)).timestamp()
        }
        await mock_redis.setex(
            "chat_limit:test-user",
            86400,
            json.dumps(limit_data)
        )

        message = {
            "message": "Teste após limite",
            "context": {"user_id": "test-user"}
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 429
        data = response.json()
        assert "error" in data
        assert "can_watch_ad" in data
        assert data["can_watch_ad"] == True


@pytest.mark.asyncio
async def test_emergency_response(mock_redis, mock_openai, auth_headers):
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService.create_chat_completion", side_effect=Exception("API Error")):

        message = {
            "message": "Preciso de ajuda urgente",
            "context": {"user_id": "test-user"}
        }

        response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["metadata"]["model"] == "emergency"
        assert data["references"] == []


@pytest.mark.asyncio
async def test_chat_rate_limiter():
    """Testa a classe ChatRateLimiter"""
    redis = MockRedis()
    limiter = ChatRateLimiter(redis)
    user_id = "test-user"

    # Teste inicial
    result = await limiter.check_chat_limit(user_id)
    assert result["allowed"] == True
    assert result["remaining"] == settings.CHAT_LIMIT_FREE_USERS
    assert result["can_watch_ad"] == True

    # Adicionar bônus
    bonus_result = await limiter.add_bonus_messages(user_id)
    assert bonus_result["success"] == True
    assert bonus_result["current_bonus"] == settings.CHAT_BONUS_PER_AD

    # Verificar limite após bônus
    result = await limiter.check_chat_limit(user_id)
    assert result["remaining"] > settings.CHAT_LIMIT_FREE_USERS

    # Testar reset
    await limiter.reset_limits()
    result = await limiter.check_chat_limit(user_id)
    assert result["remaining"] == settings.CHAT_LIMIT_FREE_USERS


@pytest.mark.asyncio
async def test_full_chat_flow(mock_redis, mock_openai, auth_headers):
    """Testa o fluxo completo de chat com limite, bônus e respostas"""
    with patch("app.core.redis.get_redis_client", return_value=mock_redis), \
            patch("app.services.openai_service.OpenAIService", return_value=mock_openai):

        # 1. Verificar mensagens restantes
        remaining = client.get(
            "/api/chat/remaining",
            headers=auth_headers
        )
        assert remaining.status_code == 200
        initial_remaining = remaining.json()["remaining_messages"]

        # 2. Enviar mensagem
        message = {
            "message": "Como ter paz?",
            "context": {"user_id": "test-user"}
        }
        chat_response = client.post(
            "/api/chat/message",
            json=message,
            headers=auth_headers
        )
        assert chat_response.status_code == 200
        assert "João 14:27" in str(chat_response.json()["references"])

        # 3. Verificar histórico
        history = client.get(
            "/api/chat/history?user_id=test-user",
            headers=auth_headers
        )
        assert history.status_code == 200
        assert len(history.json()["items"]) > 0

        # 4. Assistir anúncio e ganhar bônus
        ad_reward = client.post(
            "/api/chat/ad-reward",
            headers=auth_headers
        )
        assert ad_reward.status_code == 200
        assert ad_reward.json()["remaining_messages"] > initial_remaining
