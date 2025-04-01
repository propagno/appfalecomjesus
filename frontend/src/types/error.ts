import { ReactNode } from 'react';

export interface ErrorPageProps {
  code: string;
  title: string;
  message: string;
  showRefresh?: boolean;
  showHome?: boolean;
  showHelp?: boolean;
  customActions?: ReactNode;
}

// Interface base para erros da API
export interface ApiError {
  message: string;
  code: string;
  status: number;
  details?: Record<string, any>;
}

// Erro de validação (400)
export interface ValidationError extends ApiError {
  field: string;
  validation: string;
  value?: any;
}

// Erro de autenticação (401)
export interface AuthenticationError extends ApiError {
  token?: string;
  expired?: boolean;
  invalid?: boolean;
}

// Erro de autorização (403)
export interface AuthorizationError extends ApiError {
  requiredRole?: string;
  currentRole?: string;
  resource?: string;
}

// Erro de limite de requisições (429)
export interface RateLimitError extends ApiError {
  limit: number;
  remaining: number;
  resetTime: Date;
}

// Erro de recurso não encontrado (404)
export interface NotFoundError extends ApiError {
  resource: string;
  id?: string | number;
}

// Erro de conflito (409)
export interface ConflictError extends ApiError {
  resource: string;
  conflictingField: string;
  value: any;
}

// Erro de servidor (500)
export interface ServerError extends ApiError {
  stack?: string;
  timestamp: Date;
}

// Erro de rede
export interface NetworkError extends ApiError {
  isOnline: boolean;
  url?: string;
  method?: string;
}

// Erro de timeout
export interface TimeoutError extends ApiError {
  timeout: number;
  url?: string;
  method?: string;
}

// Erro de formato de resposta inválido
export interface InvalidResponseError extends ApiError {
  expectedFormat: string;
  receivedFormat: string;
  data?: any;
}

// Erro de cache
export interface CacheError extends ApiError {
  operation: 'read' | 'write' | 'delete';
  key: string;
  reason: string;
}

// Erro de integração com serviço externo
export interface ExternalServiceError extends ApiError {
  service: string;
  endpoint: string;
  requestId?: string;
  externalError?: any;
}

// Erro de processamento de pagamento
export interface PaymentError extends ApiError {
  transactionId?: string;
  amount?: number;
  currency?: string;
  provider?: string;
  reason?: string;
}

// Erro de processamento de mídia
export interface MediaError extends ApiError {
  type: 'image' | 'video' | 'audio';
  size?: number;
  format?: string;
  operation: 'upload' | 'process' | 'delete';
}

// Erro de processamento de IA
export interface AIError extends ApiError {
  model?: string;
  prompt?: string;
  context?: string;
  maxTokens?: number;
  temperature?: number;
}

// Função auxiliar para verificar o tipo de erro
export function isApiError(error: any): error is ApiError {
  return (
    error &&
    typeof error === 'object' &&
    'message' in error &&
    'code' in error &&
    'status' in error
  );
}

// Função para criar um erro da API
export function createApiError(
  message: string,
  code: string,
  status: number,
  details?: Record<string, any>
): ApiError {
  return {
    message,
    code,
    status,
    details,
  };
}

// Função para mapear erros HTTP para tipos específicos
export function mapHttpError(status: number, data: any): ApiError {
  switch (status) {
    case 400:
      return {
        ...data,
        status,
        code: 'VALIDATION_ERROR',
      } as ValidationError;
    case 401:
      return {
        ...data,
        status,
        code: 'AUTHENTICATION_ERROR',
      } as AuthenticationError;
    case 403:
      return {
        ...data,
        status,
        code: 'AUTHORIZATION_ERROR',
      } as AuthorizationError;
    case 404:
      return {
        ...data,
        status,
        code: 'NOT_FOUND_ERROR',
      } as NotFoundError;
    case 409:
      return {
        ...data,
        status,
        code: 'CONFLICT_ERROR',
      } as ConflictError;
    case 429:
      return {
        ...data,
        status,
        code: 'RATE_LIMIT_ERROR',
      } as RateLimitError;
    case 500:
      return {
        ...data,
        status,
        code: 'SERVER_ERROR',
      } as ServerError;
    default:
      return createApiError(
        'Erro desconhecido',
        'UNKNOWN_ERROR',
        status,
        data
      );
  }
} 
