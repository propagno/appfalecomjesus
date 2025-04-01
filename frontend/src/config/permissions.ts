/**
 * Configuração dos tipos de permissões e roles
 * Define as permissões e roles disponíveis no sistema
 */

export const roles = {
  // Roles do Sistema
  ADMIN: 'admin',
  USER: 'user',
  MODERATOR: 'moderator',
  SUPPORT: 'support',
} as const;

export const permissions = {
  // Permissões de Autenticação
  auth: {
    LOGIN: 'auth:login',
    REGISTER: 'auth:register',
    LOGOUT: 'auth:logout',
    RESET_PASSWORD: 'auth:reset_password',
    UPDATE_PROFILE: 'auth:update_profile',
    DELETE_ACCOUNT: 'auth:delete_account',
  },

  // Permissões de Estudo
  study: {
    CREATE_PLAN: 'study:create_plan',
    READ_PLAN: 'study:read_plan',
    UPDATE_PLAN: 'study:update_plan',
    DELETE_PLAN: 'study:delete_plan',
    START_STUDY: 'study:start_study',
    COMPLETE_STUDY: 'study:complete_study',
    CREATE_REFLECTION: 'study:create_reflection',
    READ_REFLECTION: 'study:read_reflection',
    UPDATE_REFLECTION: 'study:update_reflection',
    DELETE_REFLECTION: 'study:delete_reflection',
    GENERATE_CERTIFICATE: 'study:generate_certificate',
  },

  // Permissões de Chat
  chat: {
    SEND_MESSAGE: 'chat:send_message',
    READ_HISTORY: 'chat:read_history',
    CLEAR_HISTORY: 'chat:clear_history',
    SET_LIMITS: 'chat:set_limits',
  },

  // Permissões de Bíblia
  bible: {
    READ_BOOK: 'bible:read_book',
    READ_CHAPTER: 'bible:read_chapter',
    READ_VERSE: 'bible:read_verse',
    SEARCH: 'bible:search',
    BOOKMARK: 'bible:bookmark',
    SHARE: 'bible:share',
  },

  // Permissões de Gamificação
  gamification: {
    EARN_POINTS: 'gamification:earn_points',
    READ_POINTS: 'gamification:read_points',
    READ_ACHIEVEMENTS: 'gamification:read_achievements',
    UNLOCK_ACHIEVEMENT: 'gamification:unlock_achievement',
  },

  // Permissões de Monetização
  monetization: {
    READ_PLANS: 'monetization:read_plans',
    SUBSCRIBE: 'monetization:subscribe',
    CANCEL_SUBSCRIPTION: 'monetization:cancel_subscription',
    READ_PAYMENTS: 'monetization:read_payments',
    WATCH_ADS: 'monetization:watch_ads',
  },

  // Permissões de Administração
  admin: {
    READ_USERS: 'admin:read_users',
    UPDATE_USER: 'admin:update_user',
    DELETE_USER: 'admin:delete_user',
    READ_METRICS: 'admin:read_metrics',
    READ_LOGS: 'admin:read_logs',
    UPDATE_SETTINGS: 'admin:update_settings',
  },
} as const;

// Mapeamento de Roles para Permissões
export const rolePermissions = {
  [roles.ADMIN]: Object.values(permissions).flatMap(group => Object.values(group)),
  [roles.MODERATOR]: [
    permissions.auth.LOGIN,
    permissions.auth.LOGOUT,
    permissions.study.READ_PLAN,
    permissions.study.READ_REFLECTION,
    permissions.chat.READ_HISTORY,
    permissions.bible.READ_BOOK,
    permissions.bible.READ_CHAPTER,
    permissions.bible.READ_VERSE,
    permissions.gamification.READ_POINTS,
    permissions.gamification.READ_ACHIEVEMENTS,
    permissions.monetization.READ_PLANS,
    permissions.admin.READ_USERS,
    permissions.admin.READ_METRICS,
  ],
  [roles.SUPPORT]: [
    permissions.auth.LOGIN,
    permissions.auth.LOGOUT,
    permissions.study.READ_PLAN,
    permissions.study.READ_REFLECTION,
    permissions.chat.READ_HISTORY,
    permissions.bible.READ_BOOK,
    permissions.bible.READ_CHAPTER,
    permissions.bible.READ_VERSE,
    permissions.gamification.READ_POINTS,
    permissions.gamification.READ_ACHIEVEMENTS,
    permissions.monetization.READ_PLANS,
    permissions.admin.READ_USERS,
  ],
  [roles.USER]: [
    permissions.auth.LOGIN,
    permissions.auth.LOGOUT,
    permissions.auth.UPDATE_PROFILE,
    permissions.study.CREATE_PLAN,
    permissions.study.READ_PLAN,
    permissions.study.START_STUDY,
    permissions.study.COMPLETE_STUDY,
    permissions.study.CREATE_REFLECTION,
    permissions.study.READ_REFLECTION,
    permissions.study.UPDATE_REFLECTION,
    permissions.study.DELETE_REFLECTION,
    permissions.chat.SEND_MESSAGE,
    permissions.chat.READ_HISTORY,
    permissions.bible.READ_BOOK,
    permissions.bible.READ_CHAPTER,
    permissions.bible.READ_VERSE,
    permissions.bible.SEARCH,
    permissions.bible.BOOKMARK,
    permissions.bible.SHARE,
    permissions.gamification.EARN_POINTS,
    permissions.gamification.READ_POINTS,
    permissions.gamification.READ_ACHIEVEMENTS,
    permissions.monetization.READ_PLANS,
    permissions.monetization.SUBSCRIBE,
    permissions.monetization.CANCEL_SUBSCRIPTION,
    permissions.monetization.WATCH_ADS,
  ],
} as const;

export default {
  roles,
  permissions,
  rolePermissions,
}; 
