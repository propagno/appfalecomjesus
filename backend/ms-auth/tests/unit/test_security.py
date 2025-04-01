"""
Testes unitários para as funções de segurança do MS-Auth.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from jose import jwt

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    validate_token,
    check_premium_subscription,
    get_premium_status
)
from app.domain.auth.models import UserSubscription, SubscriptionType, SubscriptionStatus
from app.core.config import get_settings

settings = get_settings()


@pytest.mark.unit
class TestPasswordFunctions:
    """Testes para funções relacionadas a senhas."""

    def test_password_hash_different_from_original(self):
        """O hash da senha deve ser diferente da senha original."""
        password = "test_password"
        hashed = get_password_hash(password)
        assert password != hashed
        assert len(hashed) > len(password)

    def test_verify_password_success(self):
        """Verificação de senha deve retornar True para senha correta."""
        password = "test_password"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_failure(self):
        """Verificação de senha deve retornar False para senha incorreta."""
        password = "test_password"
        wrong_password = "wrong_password"
        hashed = get_password_hash(password)
        assert verify_password(wrong_password, hashed) is False


@pytest.mark.unit
class TestTokenFunctions:
    """Testes para funções relacionadas a tokens JWT."""

    def test_create_access_token(self):
        """Deve criar um token de acesso válido."""
        # Arrange
        data = {"sub": "test_user_id"}
        expires_delta = timedelta(minutes=15)

        # Act
        token = create_access_token(data, expires_delta)

        # Assert
        assert token is not None
        # Decodificando o token
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        assert payload["sub"] == "test_user_id"
        assert "exp" in payload

    def test_create_refresh_token(self):
        """Deve criar um token de atualização válido."""
        # Arrange
        data = {"sub": "test_user_id"}
        expires_delta = timedelta(days=7)

        # Act
        token = create_refresh_token(data, expires_delta)

        # Assert
        assert token is not None
        # Decodificando o token
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        assert payload["sub"] == "test_user_id"
        assert "exp" in payload

    def test_validate_token_success(self):
        """Deve validar com sucesso um token válido."""
        # Arrange
        data = {"sub": "test_user_id"}
        token = create_access_token(data)

        # Act
        payload = validate_token(token)

        # Assert
        assert payload is not None
        assert payload["sub"] == "test_user_id"

    def test_validate_token_failure(self):
        """Deve falhar ao validar um token inválido."""
        # Arrange
        invalid_token = "invalid_token"

        # Act
        payload = validate_token(invalid_token)

        # Assert
        assert payload is None


@pytest.mark.unit
class TestSubscriptionFunctions:
    """Testes para funções relacionadas a assinaturas Premium."""

    def test_check_premium_subscription_active(self):
        """Deve retornar True para assinatura premium ativa."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"
        subscription_mock = MagicMock()
        subscription_mock.subscription_type = SubscriptionType.PREMIUM
        subscription_mock.status = SubscriptionStatus.ACTIVE
        subscription_mock.expiration_date = datetime.utcnow() + timedelta(days=30)

        db_mock.query.return_value.filter.return_value.first.return_value = subscription_mock

        # Act
        result = check_premium_subscription(user_id, db_mock)

        # Assert
        assert result is True
        db_mock.query.assert_called_once_with(UserSubscription)
        db_mock.query.return_value.filter.assert_called_once()

    def test_check_premium_subscription_expired(self):
        """Deve retornar False para assinatura premium expirada."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"
        subscription_mock = MagicMock()
        subscription_mock.subscription_type = SubscriptionType.PREMIUM
        subscription_mock.status = SubscriptionStatus.ACTIVE
        subscription_mock.expiration_date = datetime.utcnow() - timedelta(days=1)

        db_mock.query.return_value.filter.return_value.first.return_value = subscription_mock

        # Act
        result = check_premium_subscription(user_id, db_mock)

        # Assert
        assert result is False

    def test_check_premium_subscription_free(self):
        """Deve retornar False para assinatura gratuita."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"
        subscription_mock = MagicMock()
        subscription_mock.subscription_type = SubscriptionType.FREE
        subscription_mock.status = SubscriptionStatus.ACTIVE

        db_mock.query.return_value.filter.return_value.first.return_value = subscription_mock

        # Act
        result = check_premium_subscription(user_id, db_mock)

        # Assert
        assert result is False

    def test_check_premium_subscription_canceled(self):
        """Deve retornar False para assinatura premium cancelada."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"
        subscription_mock = MagicMock()
        subscription_mock.subscription_type = SubscriptionType.PREMIUM
        subscription_mock.status = SubscriptionStatus.CANCELED

        db_mock.query.return_value.filter.return_value.first.return_value = subscription_mock

        # Act
        result = check_premium_subscription(user_id, db_mock)

        # Assert
        assert result is False

    def test_check_premium_subscription_no_subscription(self):
        """Deve retornar False quando não há assinatura."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"

        db_mock.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = check_premium_subscription(user_id, db_mock)

        # Assert
        assert result is False

    def test_get_premium_status_active(self):
        """Deve retornar status completo para assinatura premium ativa."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"
        subscription_mock = MagicMock()
        subscription_mock.subscription_type = SubscriptionType.PREMIUM
        subscription_mock.status = SubscriptionStatus.ACTIVE
        expiration_date = datetime.utcnow() + timedelta(days=30)
        subscription_mock.expiration_date = expiration_date
        subscription_mock.payment_gateway = "stripe"

        db_mock.query.return_value.filter.return_value.first.return_value = subscription_mock

        # Act
        result = get_premium_status(user_id, db_mock)

        # Assert
        assert result["is_premium"] is True
        assert result["active"] is True
        assert result["subscription_type"] == "premium"
        # Pode ser 29 ou 30 dependendo do tempo exato
        assert result["days_remaining"] >= 29
        assert result["payment_gateway"] == "stripe"

    def test_get_premium_status_free(self):
        """Deve retornar status gratuito quando não há assinatura."""
        # Arrange
        db_mock = MagicMock()
        user_id = "test_user_id"

        db_mock.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = get_premium_status(user_id, db_mock)

        # Assert
        assert result["is_premium"] is False
        assert result["active"] is False
        assert result["subscription_type"] == "free"
        assert result["days_remaining"] == 0
