/**
 * Configuração dos tipos de métricas e analytics
 * Define os eventos e métricas que serão rastreados
 */

export const metrics = {
  // Métricas de Usuário
  user: {
    REGISTRATION: 'user_registration',
    LOGIN: 'user_login',
    LOGOUT: 'user_logout',
    PROFILE_UPDATE: 'user_profile_update',
    PREFERENCE_UPDATE: 'user_preference_update',
    SUBSCRIPTION_CHANGE: 'user_subscription_change',
  },

  // Métricas de Estudo
  study: {
    PLAN_START: 'study_plan_start',
    PLAN_COMPLETE: 'study_plan_complete',
    SECTION_COMPLETE: 'study_section_complete',
    REFLECTION_CREATE: 'study_reflection_create',
    CERTIFICATE_EARNED: 'study_certificate_earned',
    TIME_SPENT: 'study_time_spent',
    PROGRESS_UPDATE: 'study_progress_update',
  },

  // Métricas de Chat
  chat: {
    MESSAGE_SENT: 'chat_message_sent',
    MESSAGE_RECEIVED: 'chat_message_received',
    LIMIT_REACHED: 'chat_limit_reached',
    LIMIT_RESET: 'chat_limit_reset',
    ERROR: 'chat_error',
    TIME_SPENT: 'chat_time_spent',
  },

  // Métricas de Gamificação
  gamification: {
    POINTS_EARNED: 'gamification_points_earned',
    ACHIEVEMENT_UNLOCKED: 'gamification_achievement_unlocked',
    REWARD_CLAIMED: 'gamification_reward_claimed',
    LEVEL_UP: 'gamification_level_up',
    STREAK_UPDATE: 'gamification_streak_update',
  },

  // Métricas de Monetização
  monetization: {
    SUBSCRIPTION_START: 'monetization_subscription_start',
    SUBSCRIPTION_END: 'monetization_subscription_end',
    PAYMENT_SUCCESS: 'monetization_payment_success',
    PAYMENT_ERROR: 'monetization_payment_error',
    AD_REWARD_EARNED: 'monetization_ad_reward_earned',
    PLAN_VIEW: 'monetization_plan_view',
  },

  // Métricas de Performance
  performance: {
    PAGE_LOAD: 'performance_page_load',
    API_CALL: 'performance_api_call',
    ERROR: 'performance_error',
    RESOURCE_LOAD: 'performance_resource_load',
  },

  // Métricas de Acessibilidade
  accessibility: {
    FONT_SIZE_CHANGE: 'accessibility_font_size_change',
    CONTRAST_MODE_TOGGLE: 'accessibility_contrast_mode_toggle',
    SCREEN_READER_TOGGLE: 'accessibility_screen_reader_toggle',
  },
};

export const analytics = {
  // Configurações do Google Analytics
  googleAnalytics: {
    TRACKING_ID: process.env.REACT_APP_GA_TRACKING_ID,
    EVENTS: {
      PAGE_VIEW: 'page_view',
      EVENT: 'event',
      EXCEPTION: 'exception',
      TIMING: 'timing',
    },
  },

  // Configurações do Hotjar
  hotjar: {
    SITE_ID: process.env.REACT_APP_HOTJAR_SITE_ID,
    HOTJAR_VERSION: process.env.REACT_APP_HOTJAR_VERSION,
  },

  // Configurações de Logs
  logs: {
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info',
    DEBUG: 'debug',
  },

  // Configurações de Métricas
  tracking: {
    ENABLED: process.env.REACT_APP_ANALYTICS_ENABLED === 'true',
    SAMPLE_RATE: 0.1, // 10% dos usuários
    MAX_EVENTS_PER_SESSION: 100,
  },
};

export default {
  metrics,
  analytics,
}; 
