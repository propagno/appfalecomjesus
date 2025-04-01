import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosRequestHeaders } from 'axios';
import { ENV, API_URLS, APP_VERSION, ERROR_REPORTING } from '../constants/config';

// Configurações globais para todas as instâncias Axios
axios.defaults.withCredentials = true; // Permite envio de cookies
axios.defaults.timeout = 30000; // 30 segundos timeout

// Tipo para erros de API personalizado
export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  details?: any;
  originalError?: Error;
}

// Interface para opções de criação do cliente
export interface ApiClientOptions {
  baseURL: string;
  withAuth?: boolean;
  enableRetry?: boolean;
  maxRetries?: number;
}

/**
 * Cria um cliente API configurado com interceptors para autenticação, 
 * retry, e tratamento de erros
 */
export const createApiClient = (options: ApiClientOptions): AxiosInstance => {
  const { baseURL, withAuth = true, enableRetry = true, maxRetries = 3 } = options;

  // Criar instância do Axios com configurações básicas
  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });

  // Interceptador de requisição - adiciona token JWT se necessário
  if (withAuth) {
    api.interceptors.request.use(
      (config) => {
        // JWT já está sendo enviado automaticamente via cookies httpOnly
        // Não é necessário adicionar no header, mas podemos adicionar outras infos
        if (!config.headers) {
          config.headers = {} as AxiosRequestHeaders;
        }
        config.headers['X-App-Version'] = APP_VERSION;
        
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  // Interceptador de resposta - trata erros e refresh token
  api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      // Criar uma versão estilizada do erro para logs e tratamento
      const apiError: ApiError = {
        message: error.message || 'Erro desconhecido',
        status: error.response?.status,
        details: error.response?.data,
        originalError: error,
      };

      // Log de erro em produção/staging
      if (!ENV.isDevelopment) {
        console.error('API Error:', {
          url: error.config?.url,
          method: error.config?.method,
          status: error.response?.status,
          message: apiError.message,
          details: error.response?.data,
        });

        // Aqui poderia integrar com um serviço de monitoramento como Sentry
        if (window.Sentry && ERROR_REPORTING.enabled) {
          // Usar métodos do Sentry sem depender de tipos específicos
          window.Sentry.captureException(error);
        }
      }

      // Tratamento específico para erro 401 (Unauthorized)
      if (error.response?.status === 401) {
        // Verificar se não estamos já na página de login ou tentando fazer refresh
        const isRefreshEndpoint = error.config?.url?.includes('/refresh');
        const isLoginEndpoint = error.config?.url?.includes('/login');
        
        if (!isRefreshEndpoint && !isLoginEndpoint) {
          try {
            // Tenta fazer refresh do token
            const refreshResponse = await axios.post(`${API_URLS.auth}/refresh`, {}, {
              withCredentials: true,
            });
            
            // Se sucesso no refresh, tenta a requisição original novamente
            if (refreshResponse.status === 200 && error.config) {
              return api(error.config);
            }
          } catch (refreshError) {
            // Se falhar o refresh, força o logout
            // Isso acontecerá quando o refresh token expirar ou for inválido
            localStorage.removeItem('user');
            window.location.href = '/login?session_expired=true';
            return Promise.reject(apiError);
          }
        } else {
          // Estamos na página de login ou tentando fazer refresh, e ainda temos 401
          // Neste caso, a sessão definitivamente expirou
          localStorage.removeItem('user');
          window.location.href = '/login?session_expired=true';
        }
      }

      // Implementação de retry automático para erros de rede ou 5xx
      if (enableRetry && error.config && shouldRetry(error, maxRetries)) {
        // Garantir que headers existe
        if (!error.config.headers) {
          error.config.headers = {} as AxiosRequestHeaders;
        }
        
        const retryCount = (error.config.headers['x-retry-count'] as number) || 0;
        
        if (retryCount < maxRetries) {
          // Incrementar contador de retries
          error.config.headers['x-retry-count'] = retryCount + 1;
          
          // Atraso exponencial: 1s, 2s, 4s, etc.
          const delay = Math.pow(2, retryCount) * 1000;
          
          // Esperar e tentar novamente
          return new Promise(resolve => {
            setTimeout(() => {
              console.log(`Tentativa ${retryCount + 1} para ${error.config?.url}`);
              resolve(api(error.config!));
            }, delay);
          });
        }
      }

      return Promise.reject(apiError);
    }
  );

  return api;
};

/**
 * Determina se uma requisição deve ser repetida com base no tipo de erro
 */
function shouldRetry(error: AxiosError, maxRetries: number): boolean {
  // Não tenta novamente se já atingimos o máximo de tentativas
  if (!error.config?.headers) return false;
  
  const retryCount = (error.config.headers['x-retry-count'] as number) || 0;
  if (retryCount >= maxRetries) return false;
  
  // Erros de rede (sem resposta do servidor)
  if (!error.response) return true;
  
  // Erros 5xx (servidor)
  const status = error.response.status;
  return status >= 500 && status < 600;
}

// Instâncias pré-configuradas para cada microsserviço
export const authApi = createApiClient({ baseURL: API_URLS.auth });
export const studyApi = createApiClient({ baseURL: API_URLS.study });
export const chatApi = createApiClient({ baseURL: API_URLS.chat });
export const bibleApi = createApiClient({ baseURL: API_URLS.bible });
export const gamificationApi = createApiClient({ baseURL: API_URLS.gamification });
export const monetizationApi = createApiClient({ baseURL: API_URLS.monetization });
export const adminApi = createApiClient({ baseURL: API_URLS.admin });

// Adicionar uma instância api padrão para compatibilidade
export const api = authApi;

export default {
  authApi,
  studyApi,
  chatApi,
  bibleApi,
  gamificationApi,
  monetizationApi,
  adminApi,
  api,
  createApiClient
}; 