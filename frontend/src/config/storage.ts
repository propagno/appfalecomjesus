/**
 * Configuração dos tipos de cache e armazenamento local
 * Define as chaves e configurações para armazenamento local e cache
 */

// Chaves de Armazenamento Local
export const storageKeys = {
  // Autenticação
  auth: {
    token: 'auth_token',
    refreshToken: 'auth_refresh_token',
    user: 'auth_user',
    preferences: 'auth_preferences',
  },

  // Estudo
  study: {
    currentPlan: 'study_current_plan',
    progress: 'study_progress',
    lastSession: 'study_last_session',
    reflections: 'study_reflections',
  },

  // Chat
  chat: {
    history: 'chat_history',
    settings: 'chat_settings',
    limits: 'chat_limits',
  },

  // Bíblia
  bible: {
    bookmarks: 'bible_bookmarks',
    lastRead: 'bible_last_read',
    searchHistory: 'bible_search_history',
  },

  // Gamificação
  gamification: {
    points: 'gamification_points',
    achievements: 'gamification_achievements',
    rewards: 'gamification_rewards',
  },

  // Monetização
  monetization: {
    subscription: 'monetization_subscription',
    ads: 'monetization_ads',
    payments: 'monetization_payments',
  },

  // Acessibilidade
  accessibility: {
    settings: 'accessibility_settings',
    preferences: 'accessibility_preferences',
  },

  // Cache
  cache: {
    bible: 'cache_bible_data',
    study: 'cache_study_data',
    chat: 'cache_chat_data',
    user: 'cache_user_data',
  },
} as const;

// Configuração do Cache
export const cacheConfig = {
  // Habilitar/Desabilitar Cache
  enabled: true,

  // Tamanho Máximo do Cache (MB)
  maxSize: 50,

  // Intervalo de Limpeza (horas)
  cleanupInterval: 24,

  // Duração do Cache
  duration: {
    short: 5 * 60 * 1000, // 5 minutos
    medium: 30 * 60 * 1000, // 30 minutos
    long: 2 * 60 * 60 * 1000, // 2 horas
    veryLong: 24 * 60 * 60 * 1000, // 24 horas
  },

  // Prioridade do Cache
  priority: {
    high: 1,
    medium: 2,
    low: 3,
  },

  // Chaves de Cache
  keys: {
    // Bíblia
    bible: {
      books: 'bible_books',
      chapters: 'bible_chapters',
      verses: 'bible_verses',
      search: 'bible_search',
    },

    // Estudo
    study: {
      plans: 'study_plans',
      sections: 'study_sections',
      progress: 'study_progress',
    },

    // Chat
    chat: {
      history: 'chat_history',
      settings: 'chat_settings',
    },

    // Usuário
    user: {
      profile: 'user_profile',
      preferences: 'user_preferences',
    },
  },

  // Configurações de Limpeza
  cleanup: {
    // Limpar cache após logout
    onLogout: true,

    // Limpar cache após erro
    onError: true,

    // Limpar cache antigo
    onExpire: true,
  },
} as const;

// Configuração do Armazenamento Local
export const localStorageConfig = {
  // Habilitar/Desabilitar Armazenamento Local
  enabled: true,

  // Prefixo para todas as chaves
  prefix: 'falecomjesus_',

  // Versão do Schema
  version: '1.0.0',

  // Configurações de Limpeza
  cleanup: {
    // Limpar dados após logout
    onLogout: true,

    // Limpar dados após erro
    onError: true,

    // Limpar dados antigos
    onExpire: true,
  },
} as const;

export default {
  storageKeys,
  cacheConfig,
  localStorageConfig,
}; 
