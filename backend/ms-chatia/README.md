# MS-ChatIA

Microsserviço de Chat com IA para o sistema FaleComJesus.

## Descrição

Este microsserviço fornece uma API para interação com modelos de linguagem da OpenAI, permitindo que os usuários conversem com um assistente espiritual. O serviço implementa:

- Limites diários de mensagens para usuários do plano gratuito
- Controle de limites utilizando Redis
- Armazenamento de histórico de conversas no PostgreSQL
- Autenticação via JWT integrada com o MS-Auth

## Requisitos

- Python 3.10+
- PostgreSQL
- Redis
- FastAPI
- Docker (opcional)

## Configuração

1. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme seu ambiente:

```bash
cp .env.example .env
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o serviço (modo desenvolvimento):

```bash
uvicorn app.main:app --reload
```

## Endpoints da API

### Mensagens

- `POST /api/v1/chat/message` - Envia uma mensagem e recebe resposta da IA
- `GET /api/v1/chat/history` - Obtém o histórico de mensagens do usuário
- `GET /api/v1/chat/remaining` - Consulta o número de mensagens restantes no dia
- `POST /api/v1/chat/ad-reward` - Adiciona mensagens bônus após assistir um anúncio

### Healthcheck

- `GET /health` - Verifica se o serviço está funcionando

## Docker

O serviço pode ser executado via Docker:

```bash
docker build -t ms-chatia .
docker run -p 8003:8003 --env-file .env ms-chatia
```

Ou usando Docker Compose:

```bash
docker-compose up -d
```

## Integração com outros microsserviços

- **MS-Auth**: Para validação de tokens JWT e autenticação
- **MS-Monetization**: Para verificação do status de assinatura (premium/free) 