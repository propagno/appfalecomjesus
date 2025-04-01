// Tipagem para as variáveis de ambiente
interface EnvConfig {
  // URLs
  apiUrl: string;
  wsUrl: string;

  // Feature Flags
  enableAnalytics: boolean;
  enableAds: boolean;

  // App Config
  appName: string;
  appVersion: string;
  environment: 'development' | 'staging' | 'production';

  // API Keys (opcional, para serviços externos)
  openaiApiKey?: string;
  googleAnalyticsId?: string;
  stripePublicKey?: string;
}

// Validação das variáveis de ambiente
const validateEnv = (): EnvConfig => {
  const requiredEnvVars = [
    'REACT_APP_API_URL',
    'REACT_APP_WS_URL',
    'REACT_APP_NAME',
    'REACT_APP_VERSION',
    'REACT_APP_ENV',
  ];

  const missingVars = requiredEnvVars.filter(
    (envVar) => !process.env[envVar]
  );

  if (missingVars.length > 0) {
    throw new Error(
      `Missing required environment variables: ${missingVars.join(', ')}`
    );
  }

  // Validação do ambiente
  const env = process.env.REACT_APP_ENV;
  if (!['development', 'staging', 'production'].includes(env || '')) {
    throw new Error(`Invalid environment: ${env}`);
  }

  return {
    // URLs
    apiUrl: process.env.REACT_APP_API_URL || 'http://localhost/api',
    wsUrl: process.env.REACT_APP_WS_URL || 'ws://localhost/ws',

    // Feature Flags
    enableAnalytics: process.env.REACT_APP_ENABLE_ANALYTICS === 'true',
    enableAds: process.env.REACT_APP_ENABLE_ADS === 'true',

    // App Config
    appName: process.env.REACT_APP_NAME || 'FaleComJesus',
    appVersion: process.env.REACT_APP_VERSION || '0.1.0',
    environment: (process.env.REACT_APP_ENV || 'development') as EnvConfig['environment'],

    // API Keys
    openaiApiKey: process.env.REACT_APP_OPENAI_API_KEY,
    googleAnalyticsId: process.env.REACT_APP_GA_ID,
    stripePublicKey: process.env.REACT_APP_STRIPE_PUBLIC_KEY,
  };
};

// Exporta a configuração validada
export const env = validateEnv();

// Funções auxiliares
export const isDevelopment = env.environment === 'development';
export const isStaging = env.environment === 'staging';
export const isProduction = env.environment === 'production';

// Configurações específicas por ambiente
export const getApiConfig = () => {
  if (isDevelopment) {
    return {
      baseURL: env.apiUrl,
      timeout: 30000, // 30 segundos em desenvolvimento
    };
  }

  return {
    baseURL: env.apiUrl,
    timeout: 15000, // 15 segundos em produção
  };
};

// Configurações de cache
export const getCacheConfig = () => ({
  maxAge: isDevelopment ? 5 * 60 * 1000 : 30 * 60 * 1000, // 5 min em dev, 30 min em prod
  staleWhileRevalidate: true,
});

// Configurações de analytics
export const getAnalyticsConfig = () => ({
  enabled: env.enableAnalytics,
  gaId: env.googleAnalyticsId,
  debug: isDevelopment,
});

// Configurações de pagamento
export const getPaymentConfig = () => ({
  stripePublicKey: env.stripePublicKey,
  testMode: !isProduction,
});

// Configurações de IA
export const getAIConfig = () => ({
  apiKey: env.openaiApiKey,
  model: isProduction ? 'gpt-3.5-turbo' : 'gpt-3.5-turbo',
  maxTokens: isProduction ? 1000 : 2000,
  temperature: 0.7,
});

// Configurações de websocket
export const getWebSocketConfig = () => ({
  url: env.wsUrl,
  reconnectInterval: isDevelopment ? 5000 : 30000,
  maxReconnectAttempts: isDevelopment ? 5 : 3,
}); 
