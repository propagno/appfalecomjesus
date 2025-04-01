"""
Constantes globais do sistema.

Este módulo define todas as constantes utilizadas no sistema FaleComJesus,
organizadas por categoria para facilitar manutenção e referência.

Categories:
    - Limites e Configurações
    - Planos e Preços
    - Tipos de Conteúdo
    - Status e Estados
    - Mensagens de Erro
    - Mensagens de Sucesso
    - Formatos e Padrões
"""

# Limites e Configurações
MAX_DAILY_MESSAGES = 5  # Mensagens por dia no plano Free
MAX_DAILY_ADS = 3  # Anúncios por dia no plano Free
MAX_CHAT_HISTORY = 50  # Mensagens no histórico
MAX_REFLECTION_LENGTH = 1000  # Caracteres por reflexão
MAX_STUDY_SECTIONS = 7  # Seções por plano de estudo
MAX_SECTION_DURATION = 30  # Minutos por seção
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB para uploads
MAX_CACHE_TTL = 3600  # 1 hora em segundos
MAX_TOKEN_LENGTH = 500  # Tokens por resposta da IA
MAX_RETRY_ATTEMPTS = 3  # Tentativas de retry

# Planos e Preços
PLAN_FREE = "free"
PLAN_PREMIUM = "premium"
PLAN_PRICES = {
    "mensal": 2990,  # R$ 29,90
    "anual": 19900   # R$ 199,00
}
REWARD_PER_AD = 5  # Mensagens ganhas por anúncio

# Tipos de Conteúdo
CONTENT_TYPE_TEXT = "text"
CONTENT_TYPE_AUDIO = "audio"
CONTENT_TYPE_VIDEO = "video"
CONTENT_TYPE_IMAGE = "image"
CONTENT_TYPE_PDF = "pdf"

# Status e Estados
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_CANCELED = "canceled"
STATUS_FAILED = "failed"

# Mensagens de Erro
ERROR_INVALID_CREDENTIALS = "Credenciais inválidas"
ERROR_USER_NOT_FOUND = "Usuário não encontrado"
ERROR_INVALID_TOKEN = "Token de acesso inválido"
ERROR_PERMISSION_DENIED = "Permissão negada"
ERROR_RESOURCE_NOT_FOUND = "Recurso não encontrado"
ERROR_INVALID_REQUEST = "Requisição inválida"
ERROR_INTERNAL_SERVER = "Erro interno do servidor"
ERROR_SERVICE_UNAVAILABLE = "Serviço temporariamente indisponível"
ERROR_RATE_LIMIT = "Limite de requisições excedido"
ERROR_DUPLICATE_ENTRY = "Registro duplicado"
ERROR_VALIDATION = "Erro de validação"
ERROR_DATABASE = "Erro no banco de dados"
ERROR_OPENAI = "Erro na API da OpenAI"

# Mensagens de Sucesso
SUCCESS_LOGIN = "Login realizado com sucesso"
SUCCESS_LOGOUT = "Logout realizado com sucesso"
SUCCESS_REGISTER = "Cadastro realizado com sucesso"
SUCCESS_UPDATE = "Atualização realizada com sucesso"
SUCCESS_DELETE = "Exclusão realizada com sucesso"
SUCCESS_PAYMENT = "Pagamento processado com sucesso"
SUCCESS_SUBSCRIPTION = "Assinatura ativada com sucesso"
SUCCESS_PLAN_CREATED = "Plano de estudo criado com sucesso"
SUCCESS_REFLECTION_SAVED = "Reflexão salva com sucesso"
SUCCESS_CERTIFICATE_GENERATED = "Certificado gerado com sucesso"

# Formatos e Padrões
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
UUID_REGEX = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
PHONE_REGEX = r"^\+?1?\d{9,15}$"
CPF_REGEX = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
CNPJ_REGEX = r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$"
CEP_REGEX = r"^\d{5}-\d{3}$"
CURRENCY_REGEX = r"^\d+\.\d{2}$"

# Configurações de Cache
CACHE_KEY_PREFIX = "fcj:"
CACHE_KEYS = {
    "user": "user:{id}",
    "study_plan": "study_plan:{id}",
    "chat_limit": "chat_limit:{user_id}",
    "reflection": "reflection:{id}",
    "certificate": "certificate:{id}",
    "bible_verse": "bible_verse:{id}",
    "daily_devotional": "daily_devotional:{date}"
}

# Headers e Cookies
HEADER_TOKEN = "Authorization"
HEADER_REFRESH = "X-Refresh-Token"
COOKIE_ACCESS = "access_token"
COOKIE_REFRESH = "refresh_token"
COOKIE_SESSION = "session_id"

# Configurações de Upload
ALLOWED_EXTENSIONS = {
    "image": ["jpg", "jpeg", "png", "gif"],
    "audio": ["mp3", "wav", "ogg"],
    "video": ["mp4", "avi", "mov"],
    "document": ["pdf", "doc", "docx"]
}
UPLOAD_FOLDER = "uploads"
TEMP_FOLDER = "temp"

# Configurações de Email
EMAIL_TEMPLATES = {
    "welcome": "welcome.html",
    "reset_password": "reset_password.html",
    "verify_email": "verify_email.html",
    "payment_success": "payment_success.html",
    "payment_failed": "payment_failed.html",
    "study_reminder": "study_reminder.html",
    "certificate": "certificate.html"
}

# Configurações de Notificação
NOTIFICATION_TYPES = {
    "study_reminder": "Lembrete de Estudo",
    "reflection_reminder": "Lembrete de Reflexão",
    "payment_success": "Pagamento Confirmado",
    "payment_failed": "Falha no Pagamento",
    "plan_completed": "Plano Concluído",
    "certificate_ready": "Certificado Disponível"
}

# Configurações de SEO
META_TITLE = "FaleComJesus - Sua Jornada Espiritual"
META_DESCRIPTION = "Estude a Bíblia com ajuda de IA, faça reflexões e cresça espiritualmente."
META_KEYWORDS = "bíblia, estudo bíblico, reflexão, espiritualidade, jesus, deus, fé"
META_AUTHOR = "FaleComJesus"
META_ROBOTS = "index, follow"
