/**
 * Configuração dos endpoints da API
 * Define todas as rotas disponíveis para cada microsserviço
 */

export const endpoints = {
  // MS-Auth
  auth: {
    register: '/api/auth/register',
    login: '/api/auth/login',
    logout: '/api/auth/logout',
    refresh: '/api/auth/refresh',
    resetPassword: '/api/auth/reset-password',
    updateProfile: '/api/auth/profile',
    preferences: '/api/auth/preferences',
  },

  // MS-Study
  study: {
    currentPlan: '/api/study/current',
    plans: '/api/study/plans',
    sections: '/api/study/sections',
    progress: '/api/study/progress',
    complete: '/api/study/complete',
    certificates: '/api/study/certificates',
  },

  // MS-ChatIA
  chat: {
    message: '/api/chat/message',
    history: '/api/chat/history',
    limit: '/api/chat/limit',
  },

  // MS-Bible
  bible: {
    books: '/api/bible/books',
    chapters: '/api/bible/chapters',
    verses: '/api/bible/verses',
    search: '/api/bible/search',
    themes: '/api/bible/themes',
  },

  // MS-Gamification
  gamification: {
    points: '/api/gamification/points',
    achievements: '/api/gamification/achievements',
    rewards: '/api/gamification/rewards',
    leaderboard: '/api/gamification/leaderboard',
  },

  // MS-Monetization
  monetization: {
    plans: '/api/monetization/plans',
    subscription: '/api/monetization/subscription',
    payment: '/api/monetization/payment',
    adReward: '/api/monetization/ad-reward',
    webhook: '/api/monetization/webhook',
  },

  // MS-Reflections
  reflections: {
    list: '/api/reflections',
    create: '/api/reflections',
    update: '/api/reflections/:id',
    delete: '/api/reflections/:id',
  },

  // MS-Support
  support: {
    feedback: '/api/support/feedback',
    contact: '/api/support/contact',
    faq: '/api/support/faq',
  },

  // MS-Admin
  admin: {
    users: '/api/admin/users',
    metrics: '/api/admin/metrics',
    logs: '/api/admin/logs',
    settings: '/api/admin/settings',
  },
};

export default endpoints; 
