/**
 * Configuração dos tipos de rotas e navegação
 * Define as rotas públicas, privadas e configurações de navegação
 */

// Rotas Públicas
export const publicRoutes = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/reset-password',
  ABOUT: '/about',
  CONTACT: '/contact',
  PRIVACY: '/privacy',
  TERMS: '/terms',
} as const;

// Rotas Privadas
export const privateRoutes = {
  // Dashboard
  DASHBOARD: '/dashboard',

  // Onboarding
  ONBOARDING: '/onboarding-new',

  // Estudo
  STUDY: {
    HOME: '/study-new',
    PLAN: '/study-new/plan/:id',
    SESSION: '/study-new/session/:id',
    REFLECTIONS: '/study-new/reflections',
    CERTIFICATES: '/study-new/certificates',
  },

  // Chat
  CHAT: {
    HOME: '/chat',
    HISTORY: '/chat/history',
  },

  // Bíblia
  BIBLE: {
    EXPLORER: '/bible',
    BOOK: '/bible/book/:id',
    CHAPTER: '/bible/chapter/:id',
    VERSE: '/bible/verse/:id',
    SEARCH: '/bible/search',
  },

  // Perfil
  PROFILE: {
    HOME: '/profile',
    SETTINGS: '/profile/settings',
    PREFERENCES: '/profile/preferences',
    ACHIEVEMENTS: '/profile/achievements',
    POINTS: '/profile/points',
  },

  // Monetização
  MONETIZATION: {
    PLANS: '/plans',
    SUBSCRIPTION: '/monetization/subscription',
    PAYMENT: '/monetization/payment',
  },
} as const;

// Rotas de Acessibilidade
export const accessibilityRoutes = {
  SETTINGS: '/accessibility',
  HELP: '/accessibility/help',
} as const;

// Rotas de Erro
export const errorRoutes = {
  NOT_FOUND: '/404',
  UNAUTHORIZED: '/401',
  FORBIDDEN: '/403',
  SERVER_ERROR: '/500',
  BAD_REQUEST: '/400',
  BAD_GATEWAY: '/502',
  SERVICE_UNAVAILABLE: '/503',
  GATEWAY_TIMEOUT: '/504',
  TOO_MANY_REQUESTS: '/429',
  NOT_IMPLEMENTED: '/501',
} as const;

// Configuração de Navegação
export const navigation = {
  // Duração das Animações (ms)
  animationDuration: 300,

  // Comportamento do Scroll
  scrollBehavior: 'smooth',

  // Configuração de Breadcrumbs
  breadcrumbs: {
    enabled: true,
    separator: '/',
    homeLabel: 'Início',
  },

  // Guardas de Rota
  guards: {
    // Rotas que requerem autenticação
    auth: Object.values(privateRoutes),

    // Rotas que requerem plano premium
    premium: [
      privateRoutes.CHAT.HOME,
      privateRoutes.STUDY.PLAN,
      privateRoutes.STUDY.SESSION,
    ],

    // Rotas que requerem onboarding completo
    onboarding: [
      privateRoutes.DASHBOARD,
      privateRoutes.STUDY.HOME,
      privateRoutes.CHAT.HOME,
    ],
  },

  // Redirecionamentos
  redirects: {
    // Após login
    afterLogin: privateRoutes.DASHBOARD,

    // Após registro
    afterRegister: privateRoutes.ONBOARDING,

    // Após logout
    afterLogout: publicRoutes.HOME,

    // Em caso de erro
    onError: errorRoutes.SERVER_ERROR,
  },

  // Configuração de Tabs
  tabs: {
    // Tabs principais
    main: [
      { path: privateRoutes.DASHBOARD, label: 'Início', icon: 'home' },
      { path: privateRoutes.STUDY.HOME, label: 'Estudo', icon: 'book' },
      { path: privateRoutes.CHAT.HOME, label: 'Chat', icon: 'chat' },
      { path: privateRoutes.BIBLE.EXPLORER, label: 'Bíblia', icon: 'bible' },
      { path: privateRoutes.PROFILE.HOME, label: 'Perfil', icon: 'user' },
    ],

    // Tabs de estudo
    study: [
      { path: privateRoutes.STUDY.HOME, label: 'Meus Estudos' },
      { path: privateRoutes.STUDY.REFLECTIONS, label: 'Reflexões' },
      { path: privateRoutes.STUDY.CERTIFICATES, label: 'Certificados' },
    ],
  },
} as const;

export default {
  publicRoutes,
  privateRoutes,
  accessibilityRoutes,
  errorRoutes,
  navigation,
}; 
