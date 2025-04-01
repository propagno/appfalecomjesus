/**
 * Configuração dos tipos de eventos e notificações
 * Define os eventos que podem ser disparados e as notificações que podem ser exibidas
 */

export const events = {
  // Eventos de Autenticação
  auth: {
    LOGIN_SUCCESS: 'auth:login:success',
    LOGIN_ERROR: 'auth:login:error',
    LOGOUT: 'auth:logout',
    REGISTER_SUCCESS: 'auth:register:success',
    REGISTER_ERROR: 'auth:register:error',
    PASSWORD_RESET: 'auth:password:reset',
    PROFILE_UPDATE: 'auth:profile:update',
  },

  // Eventos de Estudo
  study: {
    PLAN_START: 'study:plan:start',
    PLAN_COMPLETE: 'study:plan:complete',
    SECTION_COMPLETE: 'study:section:complete',
    REFLECTION_SAVE: 'study:reflection:save',
    CERTIFICATE_EARNED: 'study:certificate:earned',
    PROGRESS_UPDATE: 'study:progress:update',
  },

  // Eventos do Chat
  chat: {
    MESSAGE_SENT: 'chat:message:sent',
    MESSAGE_RECEIVED: 'chat:message:received',
    LIMIT_REACHED: 'chat:limit:reached',
    LIMIT_RESET: 'chat:limit:reset',
    ERROR: 'chat:error',
  },

  // Eventos de Gamificação
  gamification: {
    POINTS_EARNED: 'gamification:points:earned',
    ACHIEVEMENT_UNLOCKED: 'gamification:achievement:unlocked',
    REWARD_CLAIMED: 'gamification:reward:claimed',
    LEVEL_UP: 'gamification:level:up',
  },

  // Eventos de Monetização
  monetization: {
    SUBSCRIPTION_START: 'monetization:subscription:start',
    SUBSCRIPTION_END: 'monetization:subscription:end',
    PAYMENT_SUCCESS: 'monetization:payment:success',
    PAYMENT_ERROR: 'monetization:payment:error',
    AD_REWARD_EARNED: 'monetization:ad:reward:earned',
  },

  // Eventos de Acessibilidade
  accessibility: {
    FONT_SIZE_CHANGE: 'accessibility:font:size:change',
    CONTRAST_MODE_TOGGLE: 'accessibility:contrast:mode:toggle',
    SCREEN_READER_TOGGLE: 'accessibility:screen:reader:toggle',
  },

  // Eventos de Sistema
  system: {
    ERROR: 'system:error',
    WARNING: 'system:warning',
    INFO: 'system:info',
    MAINTENANCE: 'system:maintenance',
    UPDATE: 'system:update',
  },
};

export const notifications = {
  // Notificações de Sucesso
  success: {
    LOGIN: 'Login realizado com sucesso!',
    REGISTER: 'Cadastro realizado com sucesso!',
    PROFILE_UPDATE: 'Perfil atualizado com sucesso!',
    REFLECTION_SAVE: 'Reflexão salva com sucesso!',
    SUBSCRIPTION: 'Assinatura ativada com sucesso!',
    ACHIEVEMENT: 'Nova conquista desbloqueada!',
  },

  // Notificações de Erro
  error: {
    LOGIN: 'Erro ao fazer login. Verifique suas credenciais.',
    REGISTER: 'Erro ao cadastrar. Tente novamente.',
    NETWORK: 'Erro de conexão. Verifique sua internet.',
    SERVER: 'Erro no servidor. Tente novamente mais tarde.',
    PAYMENT: 'Erro no processamento do pagamento.',
  },

  // Notificações de Aviso
  warning: {
    SESSION_EXPIRING: 'Sua sessão expirará em breve.',
    STORAGE_LOW: 'Espaço de armazenamento baixo.',
    UPDATE_AVAILABLE: 'Nova versão disponível.',
  },

  // Notificações de Informação
  info: {
    WELCOME: 'Bem-vindo ao FaleComJesus!',
    STUDY_REMINDER: 'Hora de fazer seu estudo diário!',
    ACHIEVEMENT_PROGRESS: 'Você está próximo de uma nova conquista!',
    NEW_CONTENT: 'Novo conteúdo disponível!',
  },
};

export default {
  events,
  notifications,
}; 
