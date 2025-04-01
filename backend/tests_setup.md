# Guia de Implementação de Testes - FaleComJesus Backend

Este documento descreve o processo para implementar testes unitários e de integração para todos os microsserviços do projeto FaleComJesus.

## Estrutura de Testes Padronizada

Cada microsserviço deve seguir a mesma estrutura de testes:

```
ms-exemplo/
├── app/                # Código do microsserviço
├── tests/              # Diretório de testes
│   ├── conftest.py     # Configurações e fixtures compartilhadas
│   ├── unit/           # Testes unitários
│   ├── integration/    # Testes de integração
│   └── README.md       # Documentação dos testes
├── pytest.ini          # Configuração do pytest
└── run_tests.bat/sh    # Scripts para execução de testes
```

## Passos para Implementação

1. **Copiar a Estrutura Base**: Utilize a estrutura já implementada no MS-Auth como base.

2. **Adaptar conftest.py**: Ajuste as configurações para as necessidades específicas de cada microsserviço.

3. **Identificar Componentes Críticos**: Priorize os testes para componentes críticos do microsserviço:
   - Funções de segurança
   - APIs públicas
   - Lógica de negócios complexa
   - Integrações com APIs externas

4. **Implementar Testes Unitários**: Teste componentes individuais isoladamente.

5. **Implementar Testes de Integração**: Teste a interação entre componentes e APIs.

6. **Configurar CI/CD**: Integre os testes ao pipeline de CI/CD.

## Implementação por Microsserviço

### MS-Auth (✅ Concluído)

- Testes unitários para funções de segurança (tokens, hashing)
- Testes de integração para rotas de autenticação (registro, login)

### MS-Study (🔲 Pendente)

- Testes unitários para:
  - Geração de planos de estudo
  - Cálculo de progresso
  - Integração com IA
- Testes de integração para:
  - Rotas de planos de estudo
  - Rotas de progresso
  - Rotas de reflexões

### MS-ChatIA (🔲 Pendente)

- Testes unitários para:
  - Integração com OpenAI
  - Formatação de prompts
  - Limites de uso diário
- Testes de integração para:
  - Rotas de chat
  - Histórico de conversas
  - Limites de requisições

### MS-Bible (🔲 Pendente)

- Testes unitários para:
  - Busca por versículos
  - Formatação de textos bíblicos
- Testes de integração para:
  - Rotas de livros e capítulos
  - Rotas de busca
  - Rotas de versículo do dia

### MS-Gamification (🔲 Pendente)

- Testes unitários para:
  - Cálculo de pontos
  - Desbloqueio de conquistas
- Testes de integração para:
  - Rotas de pontos
  - Rotas de conquistas
  - Rotas de rankings

### MS-Monetization (🔲 Pendente)

- Testes unitários para:
  - Verificação de assinaturas
  - Processamento de webhooks
  - Gestão de recompensas de anúncios
- Testes de integração para:
  - Rotas de assinaturas
  - Rotas de webhooks
  - Rotas de recompensas

### MS-Admin (🔲 Pendente)

- Testes unitários para:
  - Geração de métricas
  - Formatação de relatórios
- Testes de integração para:
  - Rotas de métricas
  - Rotas de gerenciamento de usuários
  - Rotas de configurações

## Dependências Comuns de Testes

Cada microsserviço deve incluir as seguintes dependências em seu arquivo `requirements.txt`:

```
# Dependências de testes
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
pytest-cov==4.1.0
asyncio==3.4.3
faker==20.0.0
pytest-mock==3.12.0
pytest-dependency==0.5.1
```

## Melhores Práticas

1. **Isolamento**: Garanta que cada teste seja independente e não dependa do estado de outros testes.

2. **Mocking**: Use mocks para simular APIs externas e componentes que não estão sendo testados diretamente.

3. **Cobertura**: Busque pelo menos 80% de cobertura de código para componentes críticos.

4. **Padrão AAA**: Siga o padrão Arrange-Act-Assert para estruturar seus testes.

5. **Testes em Paralelo**: Configure os testes para rodar em paralelo quando possível.

6. **Banco de Dados**: Use bancos de dados em memória (SQLite) para testes sempre que possível.

## Exemplo de Teste Unitário

```python
@pytest.mark.unit
class TestUserService:
    def test_create_user_success(self):
        # Arrange
        user_data = {"name": "Teste", "email": "teste@example.com", "password": "senha123"}
        db_mock = MagicMock()
        service = UserService(db_mock)
        
        # Act
        result = service.create_user(user_data)
        
        # Assert
        assert result is not None
        assert result.email == "teste@example.com"
        assert result.name == "Teste"
```

## Exemplo de Teste de Integração

```python
@pytest.mark.integration
class TestUserRoutes:
    @pytest.mark.asyncio
    async def test_create_user_api(self, client, init_db):
        # Arrange
        user_data = {"name": "Teste", "email": "teste@example.com", "password": "senha123"}
        
        # Act
        response = client.post("/api/users", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "teste@example.com"
```

## Cronograma de Implementação

| Microsserviço | Testes Unitários | Testes de Integração | Prazo |
|---------------|------------------|----------------------|-------|
| MS-Auth | ✅ Concluído | ✅ Concluído | - |
| MS-Study | 🔲 Pendente | 🔲 Pendente | 15/05 |
| MS-ChatIA | 🔲 Pendente | 🔲 Pendente | 18/05 |
| MS-Bible | 🔲 Pendente | 🔲 Pendente | 20/05 |
| MS-Gamification | 🔲 Pendente | 🔲 Pendente | 22/05 |
| MS-Monetization | 🔲 Pendente | 🔲 Pendente | 25/05 |
| MS-Admin | 🔲 Pendente | �� Pendente | 28/05 | 