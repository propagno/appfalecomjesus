/**
 * Configurações globais da aplicação
 * Centraliza o acesso às variáveis de ambiente com valores padrão seguros
 */

// URLs dos microsserviços
export const API_URLS = {
  auth: '/api/auth',
  study: '/api/study',
  chat: '/api/chat',
  bible: '/api/bible',
  gamification: '/api/gamification',
  monetization: '/api/monetization',
  admin: '/api/admin',
};

// Modo mock (para desenvolvimento sem backend)
export const USE_MOCKS = false; // Desativado para usar o backend real

// Configurações de monitoramento e erros
export const ERROR_REPORTING = {
  enabled: process.env.REACT_APP_ENABLE_ERROR_REPORTING === 'true',
  sentryDsn: process.env.REACT_APP_SENTRY_DSN || '',
  logToConsole: process.env.NODE_ENV !== 'production',
  captureAllErrors: process.env.REACT_APP_CAPTURE_ALL_ERRORS === 'true',
};

// Configurações de recursos
export const FEATURES = {
  streamingResponses: process.env.REACT_APP_ENABLE_STREAMING_RESPONSES === 'true',
  offlineMode: process.env.REACT_APP_ENABLE_OFFLINE_MODE === 'true',
  chatStreaming: process.env.REACT_APP_FEATURE_CHAT_STREAMING === 'true',
  offlineBible: process.env.REACT_APP_FEATURE_OFFLINE_BIBLE === 'true',
  newStudyInterface: process.env.REACT_APP_FEATURE_NEW_STUDY_INTERFACE === 'true',
  caching: process.env.REACT_APP_ENABLE_CACHING !== 'false', // habilitado por padrão
  advancedCache: process.env.REACT_APP_ENABLE_ADVANCED_CACHE === 'true', // usar IndexedDB para grandes conjuntos de dados
  GAMIFICATION: true,
  AUDIO_PLAYBACK: true,
  SOCIAL_SHARING: true,
  PREMIUM_FEATURES: true,
};

// Configurações de cache
export const CACHE_CONFIG = {
  ttl: parseInt(process.env.REACT_APP_CACHE_TTL || '300000', 10), // 5 minutos por padrão
  prefix: 'fcj', // prefixo para chaves do cache
  cleanInterval: 3600000, // limpar cache expirado a cada 1 hora
};

// Configurações de desenvolvimento
export const DEV_TOOLS = {
  enabled: process.env.REACT_APP_ENABLE_DEVTOOLS === 'true',
  networkMonitoring: process.env.REACT_APP_ENABLE_NETWORK_MONITORING === 'true',
};

// Ambiente atual
export const ENV = {
  isDevelopment: process.env.NODE_ENV === 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isTest: process.env.NODE_ENV === 'test',
  current: process.env.NODE_ENV || 'development',
};

// Versão da aplicação
export const APP_VERSION = process.env.REACT_APP_VERSION || '0.1.0';

// Exporta para uso em outros módulos
export default {
  API_URLS,
  USE_MOCKS,
  ERROR_REPORTING,
  FEATURES,
  CACHE_CONFIG,
  DEV_TOOLS,
  ENV,
  APP_VERSION,
};

// Configuração global do sistema
export const APP_CONFIG = {
  TITLE: 'FaleComJesus',
  DESCRIPTION: 'Sua jornada espiritual personalizada',
  VERSION: '1.0.0',
};

// Limites para usuários Free
export const FREE_LIMITS = {
  DAILY_CHAT_MESSAGES: 5,
  STUDY_DAYS: 10,
}; 