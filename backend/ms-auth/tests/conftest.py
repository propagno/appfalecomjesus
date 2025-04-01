"""
Configurações globais para testes do MS-Auth.
Este arquivo contém fixtures compartilhadas entre testes unitários e de integração.
"""
import asyncio
import os
from typing import Dict, Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.infrastructure.database.base import Base
from app.infrastructure.database.session import get_session
from app.main import app as main_app

# Define variáveis de ambiente para testes
os.environ["APP_ENV"] = "test"
os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "15"
os.environ["JWT_REFRESH_TOKEN_EXPIRE_DAYS"] = "7"


# Configuração do banco de dados de teste
TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL)
async_engine = create_async_engine(
    TEST_ASYNC_DATABASE_URL,
    poolclass=NullPool,
    connect_args={"check_same_thread": False},
)

TestingAsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


# Fixture para inicializar e limpar o banco de dados
@pytest.fixture(scope="function")
async def init_db():
    """
    Inicializar e limpar o banco de dados para cada teste.
    """
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)

    yield

    # Limpa todas as tabelas após o teste
    Base.metadata.drop_all(bind=engine)


# Override da dependência do banco de dados
@pytest.fixture
async def override_get_session():
    """
    Sobrescreve a dependência get_session para usar o banco de teste.
    """
    async def _override_get_session():
        async with TestingAsyncSessionLocal() as session:
            yield session

    return _override_get_session


# Fixture para o cliente de teste
@pytest.fixture
async def client(override_get_session) -> Generator:
    """
    Cria um cliente TestClient para os testes de integração.
    """
    app = FastAPI()
    app.dependency_overrides[get_session] = override_get_session

    # Use a versão mais simples do aplicativo para testes
    app = main_app
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client


# Fixture para criar usuário de teste
@pytest.fixture
async def test_user() -> Dict[str, Any]:
    """
    Retorna dados de um usuário de teste.
    """
    return {
        "email": "test@example.com",
        "password": "test_password",
        "name": "Test User",
    }


# Fixture para evento de loop
@pytest.fixture(scope="session")
def event_loop():
    """
    Cria um novo loop de evento para testes assíncronos.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
