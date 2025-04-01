/**
 * Configuração dos tipos de erros e exceções
 * Define os erros que podem ocorrer e suas mensagens
 */

export const errors = {
  // Erros de Autenticação
  auth: {
    INVALID_CREDENTIALS: {
      code: 'AUTH_001',
      message: 'Credenciais inválidas',
      description: 'Email ou senha incorretos',
    },
    TOKEN_EXPIRED: {
      code: 'AUTH_002',
      message: 'Sessão expirada',
      description: 'Sua sessão expirou. Faça login novamente.',
    },
    UNAUTHORIZED: {
      code: 'AUTH_003',
      message: 'Não autorizado',
      description: 'Você não tem permissão para acessar este recurso.',
    },
    ACCOUNT_LOCKED: {
      code: 'AUTH_004',
      message: 'Conta bloqueada',
      description: 'Muitas tentativas de login. Tente novamente mais tarde.',
    },
  },

  // Erros de Validação
  validation: {
    INVALID_EMAIL: {
      code: 'VAL_001',
      message: 'Email inválido',
      description: 'Digite um email válido',
    },
    WEAK_PASSWORD: {
      code: 'VAL_002',
      message: 'Senha fraca',
      description: 'A senha deve ter no mínimo 8 caracteres',
    },
    REQUIRED_FIELD: {
      code: 'VAL_003',
      message: 'Campo obrigatório',
      description: 'Este campo é obrigatório',
    },
    INVALID_FORMAT: {
      code: 'VAL_004',
      message: 'Formato inválido',
      description: 'O formato do campo está incorreto',
    },
  },

  // Erros de API
  api: {
    NETWORK_ERROR: {
      code: 'API_001',
      message: 'Erro de conexão',
      description: 'Não foi possível conectar ao servidor',
    },
    SERVER_ERROR: {
      code: 'API_002',
      message: 'Erro no servidor',
      description: 'Ocorreu um erro interno no servidor',
    },
    TIMEOUT: {
      code: 'API_003',
      message: 'Tempo limite excedido',
      description: 'A requisição demorou muito para responder',
    },
    RATE_LIMIT: {
      code: 'API_004',
      message: 'Limite de requisições excedido',
      description: 'Muitas requisições em um curto período',
    },
  },

  // Erros de Negócio
  business: {
    STUDY_LIMIT: {
      code: 'BUS_001',
      message: 'Limite de estudos atingido',
      description: 'Você atingiu o limite diário de estudos',
    },
    CHAT_LIMIT: {
      code: 'BUS_002',
      message: 'Limite de mensagens atingido',
      description: 'Você atingiu o limite diário de mensagens',
    },
    SUBSCRIPTION_EXPIRED: {
      code: 'BUS_003',
      message: 'Assinatura expirada',
      description: 'Sua assinatura expirou. Renove para continuar.',
    },
    CONTENT_NOT_FOUND: {
      code: 'BUS_004',
      message: 'Conteúdo não encontrado',
      description: 'O conteúdo solicitado não existe',
    },
  },

  // Erros de Sistema
  system: {
    STORAGE_FULL: {
      code: 'SYS_001',
      message: 'Armazenamento cheio',
      description: 'O armazenamento local está cheio',
    },
    BROWSER_NOT_SUPPORTED: {
      code: 'SYS_002',
      message: 'Navegador não suportado',
      description: 'Seu navegador não suporta esta funcionalidade',
    },
    FEATURE_NOT_AVAILABLE: {
      code: 'SYS_003',
      message: 'Funcionalidade não disponível',
      description: 'Esta funcionalidade não está disponível no seu plano',
    },
  },
};

export default errors; 
