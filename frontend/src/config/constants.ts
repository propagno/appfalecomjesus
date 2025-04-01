// Configurações gerais do sistema
export const APP_CONFIG = {
  NAME: 'FaleComJesus',
  DESCRIPTION: 'Sua jornada espiritual personalizada com IA',
  VERSION: '1.0.0',
  API_URL: process.env.REACT_APP_API_URL || 'http://localhost/api',
  ENV: process.env.NODE_ENV || 'development',
};

// Configurações de autenticação
export const AUTH_CONFIG = {
  TOKEN_EXPIRY: 15 * 60 * 1000, // 15 minutos
  REFRESH_TOKEN_EXPIRY: 7 * 24 * 60 * 60 * 1000, // 7 dias
  MAX_LOGIN_ATTEMPTS: 3,
  LOCKOUT_DURATION: 15 * 60 * 1000, // 15 minutos
};

// Configurações de estudo
export const STUDY_CONFIG = {
  MAX_DAILY_STUDY_TIME: 60 * 60 * 1000, // 1 hora
  MIN_STUDY_TIME: 15 * 60 * 1000, // 15 minutos
  DEFAULT_SESSION_DURATION: 30 * 60 * 1000, // 30 minutos
  MAX_SESSIONS_PER_DAY: 3,
};

// Configurações de chat
export const CHAT_CONFIG = {
  FREE_TIER_LIMIT: 5, // mensagens por dia
  PREMIUM_TIER_LIMIT: Infinity,
  MAX_MESSAGE_LENGTH: 500,
  MIN_MESSAGE_LENGTH: 10,
  TYPING_INDICATOR_DELAY: 1000, // 1 segundo
};

// Configurações de gamificação
export const GAMIFICATION_CONFIG = {
  POINTS_PER_STUDY_SESSION: 10,
  POINTS_PER_REFLECTION: 5,
  POINTS_PER_ACHIEVEMENT: 50,
  POINTS_PER_STREAK_DAY: 2,
  MAX_STREAK_BONUS: 10,
};

// Configurações de monetização
export const MONETIZATION_CONFIG = {
  FREE_TIER: {
    NAME: 'Free',
    PRICE: 0,
    FEATURES: [
      '5 mensagens por dia no chat',
      '10 dias de estudo',
      'Reflexões básicas',
      'Acesso à Bíblia',
    ],
  },
  PREMIUM_TIER: {
    NAME: 'Premium',
    PRICE: 29.90,
    FEATURES: [
      'Chat ilimitado',
      'Estudos ilimitados',
      'Reflexões avançadas',
      'Acesso à Bíblia',
      'Certificados personalizados',
      'Sem anúncios',
    ],
  },
};

// Configurações de cache
export const CACHE_CONFIG = {
  BIBLE_CACHE_DURATION: 24 * 60 * 60 * 1000, // 24 horas
  STUDY_PLAN_CACHE_DURATION: 60 * 60 * 1000, // 1 hora
  USER_PREFERENCES_CACHE_DURATION: 12 * 60 * 60 * 1000, // 12 horas
};

// Configurações de acessibilidade
export const ACCESSIBILITY_CONFIG = {
  MIN_FONT_SIZE: 12,
  MAX_FONT_SIZE: 24,
  DEFAULT_FONT_SIZE: 16,
  HIGH_CONTRAST_MODE: false,
  SCREEN_READER_SUPPORT: true,
};

// Configurações de performance
export const PERFORMANCE_CONFIG = {
  LAZY_LOAD_THRESHOLD: 100, // pixels
  INFINITE_SCROLL_THRESHOLD: 200, // pixels
  DEBOUNCE_DELAY: 300, // ms
  THROTTLE_DELAY: 500, // ms
};

// Configurações de erro
export const ERROR_CONFIG = {
  MAX_RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // ms
  ERROR_MESSAGE_DURATION: 5000, // ms
  NETWORK_TIMEOUT: 15000, // ms
};

// Configurações de analytics
export const ANALYTICS_CONFIG = {
  TRACKING_ID: process.env.REACT_APP_GA_TRACKING_ID,
  EVENTS: {
    STUDY_START: 'study_start',
    STUDY_COMPLETE: 'study_complete',
    CHAT_MESSAGE: 'chat_message',
    REFLECTION_SAVE: 'reflection_save',
    ACHIEVEMENT_UNLOCK: 'achievement_unlock',
    SUBSCRIPTION_START: 'subscription_start',
    SUBSCRIPTION_CANCEL: 'subscription_cancel',
  },
};

// Configurações de SEO
export const SEO_CONFIG = {
  DEFAULT_TITLE: 'FaleComJesus - Sua Jornada Espiritual Personalizada',
  DEFAULT_DESCRIPTION: 'Conecte-se com Deus através de estudos bíblicos personalizados, chat com IA e reflexões diárias.',
  DEFAULT_KEYWORDS: 'bíblia, estudo bíblico, espiritualidade, cristianismo, IA, chat, reflexão',
  SOCIAL_IMAGE: '/images/social-preview.jpg',
};

// Configurações de notificações
export const NOTIFICATION_CONFIG = {
  ENABLED: true,
  PERMISSION_REQUIRED: true,
  DEFAULT_SOUND: true,
  VIBRATION: true,
  TYPES: {
    STUDY_REMINDER: 'study_reminder',
    ACHIEVEMENT: 'achievement',
    CHAT_MESSAGE: 'chat_message',
    SYSTEM: 'system',
  },
};

// Configurações de compartilhamento
export const SHARE_CONFIG = {
  PLATFORMS: {
    WHATSAPP: 'whatsapp',
    FACEBOOK: 'facebook',
    TWITTER: 'twitter',
    LINKEDIN: 'linkedin',
    EMAIL: 'email',
  },
  CONTENT_TYPES: {
    VERSE: 'verse',
    REFLECTION: 'reflection',
    ACHIEVEMENT: 'achievement',
    CERTIFICATE: 'certificate',
  },
}; 
