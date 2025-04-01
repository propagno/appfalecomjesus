"""
MS-ChatIA - Arquivo principal do FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import os
import logging
from openai import OpenAI
from datetime import datetime
import random
import time
from typing import List, Dict, Optional

from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryItem,
    ChatHistoryResponse,
    ChatMessageLimit
)
from app.api.v1.api import api_router
from app.core.config import get_settings
from app.core.error_handlers import setup_error_handlers
from app.core.logging import setup_logging
from app.core.middleware import setup_middlewares

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do OpenAI com API key do ambiente
settings = get_settings()
API_KEY = os.getenv("OPENAI_API_KEY", settings.OPENAI_API_KEY)
logger.info(f"Inicializando OpenAI client com a API KEY configurada")
client = OpenAI(api_key=API_KEY)

# Para o caso de falhas na API da OpenAI (modo de emergência)
RESPOSTAS_BIBLICAS = {
    "oração": [
        "A oração é um diálogo amoroso com Deus. Como diz Filipenses 4:6-7: 'Não andem ansiosos por coisa alguma, mas em tudo, pela oração e súplicas, e com ação de graças, apresentem seus pedidos a Deus. E a paz de Deus, que excede todo o entendimento, guardará o coração e a mente de vocês em Cristo Jesus.'",
    ],
    "fé": [
        "A fé é a certeza daquilo que esperamos e a prova das coisas que não vemos (Hebreus 11:1). É através da fé que nos conectamos com Deus e recebemos Suas promessas.",
    ],
    "triste": [
        "Em momentos de tristeza, podemos encontrar conforto nas palavras do Salmo 34:18: 'O Senhor está perto dos que têm o coração quebrantado e salva os de espírito abatido.' Lembre-se que Deus está sempre ao seu lado, mesmo nos momentos mais difíceis.",
    ],
    "ansiedade": [
        "Para momentos de ansiedade, a Bíblia nos conforta em 1 Pedro 5:7: 'Lancem sobre ele toda a sua ansiedade, porque ele tem cuidado de vocês.'",
    ],
}

RESPOSTAS_GENERICAS = [
    "A jornada espiritual é um caminho de crescimento contínuo. Como diz Provérbios 4:18: 'A vereda dos justos é como a luz da aurora, que vai brilhando mais e mais até ser dia perfeito.'",
    "Deus está sempre presente em nossa vida. Deuteronômio 31:8 nos lembra: 'O Senhor é quem vai adiante de você; ele será com você, não o deixará, nem o desamparará; não temas, nem te espantes.'",
]


def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI
    """
    settings = get_settings()

    app = FastAPI(
        title="MS-ChatIA API",
        description="""
        API do Microsserviço de Chat com IA do FaleComJesus.
        
        Este serviço oferece:
        * Interação com IA para aconselhamento espiritual
        * Histórico de conversas
        * Controle de limites de uso
        * Geração de planos de estudo personalizados
        
        Para mais informações, consulte a documentação completa.
        """,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configurar logging
    setup_logging(app)

    # Configurar handlers de erro
    setup_error_handlers(app)

    # Configurar middlewares adicionais
    setup_middlewares(app)

    # Incluir rotas da API
    app.include_router(api_router, prefix="/api/v1")

    # Customizar OpenAPI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="MS-ChatIA API",
            version="1.0.0",
            description="""
            # Introdução
            
            Bem-vindo à documentação da API do MS-ChatIA, parte do sistema FaleComJesus.
            
            ## Autenticação
            
            Todas as requisições devem incluir um token JWT válido no header Authorization:
            ```
            Authorization: Bearer <token>
            ```
            
            ## Rate Limiting
            
            As requisições são limitadas por usuário e por IP:
            * Usuários Free: 100 requisições/hora
            * Usuários Premium: Sem limite
            * Por IP: 1000 requisições/hora
            
            ## Respostas de Erro
            
            Em caso de erro, a API retorna um objeto JSON com:
            * error_id: Identificador único do erro
            * code: Código do erro
            * message: Mensagem descritiva
            * details: Detalhes adicionais (opcional)
            
            ## Endpoints Principais
            
            ### Chat
            * POST /api/v1/chat/message - Envia mensagem e recebe resposta da IA
            * GET /api/v1/chat/history - Obtém histórico de mensagens
            * GET /api/v1/chat/limit - Verifica limite de mensagens
            * POST /api/v1/chat/bonus - Adiciona mensagens bônus
            
            ### Planos de Estudo
            * POST /api/v1/study/plan - Gera plano personalizado
            * GET /api/v1/study/progress - Obtém progresso do usuário
            
            ## Cache
            
            A API utiliza Redis para cache de:
            * Respostas frequentes da IA
            * Limites de uso
            * Histórico recente de mensagens
            
            ## Monitoramento
            
            Logs estruturados e métricas são coletados para:
            * Performance da API
            * Uso de recursos
            * Erros e exceções
            * Comportamento dos usuários
            """,
            routes=app.routes,
        )

        # Customizar tags
        openapi_schema["tags"] = [
            {
                "name": "chat",
                "description": "Operações relacionadas ao chat com IA"
            },
            {
                "name": "study",
                "description": "Operações relacionadas a planos de estudo"
            }
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    @app.get("/health")
    async def health_check():
        """
        Endpoint de health check
        """
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat()
        }

    return app


app = create_app()

# Dados mock para histórico de chat (usado apenas quando não há banco de dados)
MOCK_HISTORY = []

# Variável global para controle de mensagens (deve ser substituída por Redis em produção)
remaining_messages_mock = 5


def extract_bible_references(text: str) -> List[str]:
    """Extrai referências bíblicas do texto da resposta"""
    # Implementação básica - deve ser melhorada com regex ou NLP
    references = []
    if "(" in text and ")" in text:
        # Exemplo simples - extrair texto entre parênteses
        start = text.find("(")
        end = text.find(")")
        if start > -1 and end > start:
            ref = text[start+1:end].strip()
            references.append(ref)
    return references


def generate_suggestions(message: str, response: str) -> List[str]:
    """Gera sugestões de próximas perguntas baseadas no contexto"""
    # Implementação básica - deve ser melhorada com IA
    suggestions = [
        "Como posso aplicar isso na minha vida?",
        "Existe outro versículo sobre esse tema?",
        "Pode me explicar melhor esse conceito?"
    ]
    return suggestions


def get_emergency_response(message: str) -> str:
    message_lower = message.lower()

    # Verificar palavras-chave
    for keyword, responses in RESPOSTAS_BIBLICAS.items():
        if keyword in message_lower:
            return random.choice(responses)

    # Se não encontrar palavras-chave, retorna resposta genérica
    return random.choice(RESPOSTAS_GENERICAS)


@app.on_event("startup")
async def startup_event():
    logger.info("MS-CHATIA iniciando")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("MS-CHATIA finalizando")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/chat/health")
async def api_chat_health():
    """Endpoint de health check para a rota /api/chat/health"""
    return {"status": "healthy", "service": "ms-chatia"}


@app.get("/api/chat/history", response_model=ChatHistoryResponse)
async def get_history():
    """Retorna histórico de chat"""
    return ChatHistoryResponse(
        items=MOCK_HISTORY,
        total=len(MOCK_HISTORY),
        limit=20,
        skip=0
    )


@app.get("/api/chat/remaining", response_model=ChatMessageLimit)
async def get_remaining():
    """Retorna informações sobre limite de mensagens"""
    global remaining_messages_mock
    return ChatMessageLimit(
        remaining_messages=remaining_messages_mock,
        limit=5,
        reset_in=86400,  # 24 horas em segundos
        can_watch_ad=remaining_messages_mock < 5
    )


@app.post("/api/chat/message", response_model=ChatMessageResponse)
async def chat_message(message: ChatMessageCreate):
    try:
        global remaining_messages_mock
        start_time = time.time()
        logger.info(f"Mensagem recebida: {message.message}")

        if remaining_messages_mock > 0:
            remaining_messages_mock -= 1

        # System message aprimorado com contexto
        system_message = """
        Você é um conselheiro espiritual cristão que responde sempre de forma acolhedora, 
        positiva e baseada em princípios bíblicos. Ao responder:
        1. Cite pelo menos um versículo bíblico relevante
        2. Inclua uma breve reflexão prática
        3. Evite julgamentos
        4. Seja gentil e paciente
        5. Incentive a fé e esperança
        6. Use linguagem simples e acessível
        7. Formate o versículo entre parênteses para fácil extração
        """

        # Preparação do prompt com contexto
        user_message = message.message
        if message.context:
            user_message = f"Contexto adicional: {message.context}\n\nPergunta: {message.message}"

        try:
            # Chamada à API da OpenAI
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "800"))
            )

            ai_response = response.choices[0].message.content

            # Extração de referências e geração de sugestões
            verses = extract_bible_references(ai_response)
            suggestions = generate_suggestions(message.message, ai_response)

        except Exception as api_error:
            logger.error(f"Erro na API da OpenAI: {str(api_error)}")
            ai_response = get_emergency_response(message.message)
            verses = []
            suggestions = []

        # Adicionar ao histórico
        import uuid
        from datetime import datetime

        new_history_item = ChatHistoryItem(
            id=uuid.uuid4(),
            message=message.message,
            response=ai_response,
            created_at=datetime.now()
        )
        MOCK_HISTORY.append(new_history_item)

        # Limitar histórico mock
        if len(MOCK_HISTORY) > 20:
            MOCK_HISTORY.pop(0)

        return ChatMessageResponse(
            message=ai_response,
            verses=verses,
            suggestions=suggestions
        )

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        emergency_response = get_emergency_response(message.message)
        return ChatMessageResponse(
            message=emergency_response,
            verses=[],
            suggestions=[]
        )


@app.post("/api/chat/ad-reward", response_model=ChatMessageLimit)
async def ad_reward():
    """Recompensa após assistir anúncio"""
    global remaining_messages_mock
    # Limite máximo de 20 mensagens
    remaining_messages_mock = min(remaining_messages_mock + 5, 20)

    return ChatMessageLimit(
        remaining_messages=remaining_messages_mock,
        limit=5,
        reset_in=86400,  # 24 horas em segundos
        # Só pode assistir se não atingiu o limite máximo
        can_watch_ad=remaining_messages_mock < 20
    )
