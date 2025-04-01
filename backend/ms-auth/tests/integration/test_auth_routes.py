"""
Testes de integração para as rotas de autenticação.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.security import validate_token
from app.domain.auth.service import AuthService


@pytest.mark.integration
class TestAuthRoutes:
    """Testes de integração para rotas de autenticação."""

    @pytest.mark.asyncio
    async def test_register_success(self, client, init_db):
        """Deve registrar um novo usuário com sucesso."""
        # Arrange
        user_data = {
            "name": "Novo Usuário",
            "email": "novo@example.com",
            "password": "senha123"
        }

        # Act
        response = client.post("/api/auth/register", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Novo Usuário"
        assert data["email"] == "novo@example.com"
        assert "id" in data
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_register_email_already_exists(self, client, init_db):
        """Deve falhar ao registrar usuário com email já existente."""
        # Arrange - Criar primeiro usuário
        user_data = {
            "name": "Usuário Original",
            "email": "existente@example.com",
            "password": "senha123"
        }

        # Registra o primeiro usuário
        client.post("/api/auth/register", json=user_data)

        # Tenta registrar um segundo usuário com o mesmo email
        duplicate_user = {
            "name": "Usuário Duplicado",
            "email": "existente@example.com",
            "password": "senha456"
        }

        # Act
        response = client.post("/api/auth/register", json=duplicate_user)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Email already registered" in data["detail"]

    @pytest.mark.asyncio
    async def test_login_success(self, client, init_db):
        """Deve realizar login com sucesso e retornar tokens."""
        # Arrange - Criar usuário primeiro
        user_data = {
            "name": "Usuário Login",
            "email": "login@example.com",
            "password": "senha123"
        }

        # Registra o usuário
        client.post("/api/auth/register", json=user_data)

        # Act - Faz login
        login_data = {
            "username": "login@example.com",
            "password": "senha123"
        }

        response = client.post("/api/auth/login", data=login_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Verifica se os cookies foram setados
        cookies = response.cookies
        assert "access_token" in cookies
        assert "refresh_token" in cookies

        # Verifica se o token é válido
        payload = validate_token(data["access_token"])
        assert payload is not None
        assert "sub" in payload

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client, init_db):
        """Deve falhar ao fazer login com credenciais inválidas."""
        # Arrange - Criar usuário primeiro
        user_data = {
            "name": "Usuário Inválido",
            "email": "invalido@example.com",
            "password": "senha123"
        }

        # Registra o usuário
        client.post("/api/auth/register", json=user_data)

        # Act - Tenta login com senha incorreta
        login_data = {
            "username": "invalido@example.com",
            "password": "senha_errada"
        }

        response = client.post("/api/auth/login", data=login_data)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Incorrect email or password" in data["detail"]

    @pytest.mark.asyncio
    async def test_get_current_user(self, client, init_db):
        """Deve retornar informações do usuário atual após login."""
        # Arrange - Criar e logar usuário
        user_data = {
            "name": "Usuário Atual",
            "email": "atual@example.com",
            "password": "senha123"
        }

        # Registra o usuário
        client.post("/api/auth/register", json=user_data)

        # Login
        login_data = {
            "username": "atual@example.com",
            "password": "senha123"
        }

        login_response = client.post("/api/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Act - Obter informações do usuário atual
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Usuário Atual"
        assert data["email"] == "atual@example.com"
        assert "id" in data

    @pytest.mark.asyncio
    async def test_logout(self, client, init_db):
        """Deve realizar logout do usuário e limpar cookies."""
        # Arrange - Criar e logar usuário
        user_data = {
            "name": "Usuário Logout",
            "email": "logout@example.com",
            "password": "senha123"
        }

        # Registra o usuário
        client.post("/api/auth/register", json=user_data)

        # Login
        login_data = {
            "username": "logout@example.com",
            "password": "senha123"
        }

        login_response = client.post("/api/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Act - Fazer logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully logged out"

        # Verifica se os cookies foram removidos
        cookies = response.cookies

        # Verifica se os cookies têm valor vazio ou foram marcados para expirar
        for cookie_name in ['access_token', 'refresh_token']:
            if cookie_name in cookies:
                # Verifica se o valor está vazio ou se o cookie foi configurado para expirar imediatamente
                assert cookies[cookie_name] == "" or cookies[cookie_name].expires <= 0

    @pytest.mark.asyncio
    async def test_refresh_token(self, client, init_db):
        """Deve gerar um novo access token a partir do refresh token."""
        # Arrange - Criar e logar usuário
        user_data = {
            "name": "Usuário Refresh",
            "email": "refresh@example.com",
            "password": "senha123"
        }

        # Registra o usuário
        client.post("/api/auth/register", json=user_data)

        # Login
        login_data = {
            "username": "refresh@example.com",
            "password": "senha123"
        }

        login_response = client.post("/api/auth/login", data=login_data)
        refresh_token = login_response.json()["refresh_token"]

        # Configurar cookie para o teste
        cookies = {"refresh_token": refresh_token}

        # Act - Solicitar refresh do token
        response = client.post("/api/auth/refresh-token", cookies=cookies)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Verifica se os novos tokens são válidos
        payload = validate_token(data["access_token"])
        assert payload is not None
        assert "sub" in payload
