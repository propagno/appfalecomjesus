/**
 * Utilitário para tratamento global de erros
 * Centraliza o registro e tratamento de erros em toda a aplicação
 */

import { ERROR_REPORTING, ENV } from '../constants/config';

/**
 * Interface para erros da API
 */
export interface ApiError {
  status: number;
  message: string;
  code?: string;
  details?: Record<string, any>;
}

/**
 * Tipos de erros do sistema
 */
export enum ErrorType {
  API = 'api_error',
  NETWORK = 'network_error',
  AUTHENTICATION = 'auth_error',
  VALIDATION = 'validation_error',
  UNKNOWN = 'unknown_error',
}

/**
 * Configurações para notificações de erro
 */
export interface ErrorNotificationConfig {
  showNotification: boolean;
  logToConsole: boolean;
  reportToMonitoring: boolean;
}

/**
 * Callback para notificações de erro
 */
export type ErrorNotificationCallback = (error: FormattedError) => void;

/**
 * Erro formatado para exibição e monitoramento
 */
export interface FormattedError {
  type: ErrorType;
  message: string;
  originalError: any;
  timestamp: number;
  details?: Record<string, any>;
  context?: Record<string, any>;
}

/**
 * Interface completa para erros no aplicativo
 */
export interface AppError {
  type: ErrorType;
  message: string;
  code?: string | number;
  status?: number;
  details?: Record<string, any>;
  originalError?: any;
  timestamp: number;
  source?: string;
}

/**
 * Opções para personalizar o comportamento do tratamento de erros
 */
export interface ErrorHandlerOptions {
  silent?: boolean;      // Se true, não exibe notificações
  context?: string;      // Contexto adicional sobre onde o erro ocorreu
  throwError?: boolean;  // Se true, propaga o erro após o tratamento
}

// Definindo tipos para callbacks de erro
type ErrorCallback = (error: AppError) => void;

/**
 * Classe para gerenciar erros da aplicação
 */
export class ErrorHandler {
  private static instance: ErrorHandler;
  private errorCallbacks: ErrorCallback[] = [];
  private notificationCallbacks: ErrorNotificationCallback[] = [];
  private isProduction = process.env.NODE_ENV === 'production';

  /**
   * Obtém instância única do ErrorHandler (Singleton)
   */
  public static getInstance(): ErrorHandler {
    if (!ErrorHandler.instance) {
      ErrorHandler.instance = new ErrorHandler();
    }
    return ErrorHandler.instance;
  }

  /**
   * Adiciona um callback para ser chamado quando ocorrer um erro
   * @param callback Função a ser chamada com o erro
   */
  public registerErrorCallback(callback: ErrorCallback): void {
    this.errorCallbacks.push(callback);
  }

  /**
   * Remove um callback previamente registrado
   * @param callback Callback a ser removido
   */
  public unregisterErrorCallback(callback: ErrorCallback): void {
    this.errorCallbacks = this.errorCallbacks.filter(cb => cb !== callback);
  }

  /**
   * Configura um callback para notificação de erros
   * @param callback Função a ser chamada quando ocorrer um erro
   * @returns Função para remover o callback
   */
  public registerNotificationCallback(callback: ErrorNotificationCallback): () => void {
    this.notificationCallbacks.push(callback);
    return () => {
      this.notificationCallbacks = this.notificationCallbacks.filter((cb) => cb !== callback);
    };
  }

  /**
   * Trata erros da API
   * @param error Erro da API
   * @param context Informações adicionais sobre o contexto do erro
   * @param config Configurações para tratamento do erro
   */
  public handleApiError(
    error: ApiError,
    context?: Record<string, any>,
    config?: Partial<ErrorNotificationConfig>
  ): FormattedError {
    const defaultConfig: ErrorNotificationConfig = {
      showNotification: true,
      logToConsole: ERROR_REPORTING.logToConsole,
      reportToMonitoring: ERROR_REPORTING.enabled,
    };
    
    const mergedConfig = { ...defaultConfig, ...config };
    
    const formattedError: FormattedError = {
      type: ErrorType.API,
      message: error.message || 'Erro na comunicação com o servidor',
      originalError: error,
      timestamp: Date.now(),
      details: {
        status: error.status,
        code: error.code,
        ...error.details,
      },
      context,
    };
    
    // Tratamento do erro
    this.processError(formattedError, mergedConfig);
    
    return formattedError;
  }
  
  /**
   * Trata erros de rede
   */
  public handleNetworkError(
    error: Error,
    context?: Record<string, any>,
    config?: Partial<ErrorNotificationConfig>
  ): FormattedError {
    const defaultConfig: ErrorNotificationConfig = {
      showNotification: true,
      logToConsole: ERROR_REPORTING.logToConsole,
      reportToMonitoring: ERROR_REPORTING.enabled,
    };
    
    const mergedConfig = { ...defaultConfig, ...config };
    
    const formattedError: FormattedError = {
      type: ErrorType.NETWORK,
      message: 'Erro de conexão. Verifique sua internet.',
      originalError: error,
      timestamp: Date.now(),
      context,
    };
    
    this.processError(formattedError, mergedConfig);
    
    return formattedError;
  }
  
  /**
   * Trata erros de autenticação
   */
  public handleAuthError(
    error: any,
    context?: Record<string, any>,
    config?: Partial<ErrorNotificationConfig>
  ): FormattedError {
    const defaultConfig: ErrorNotificationConfig = {
      showNotification: true,
      logToConsole: ERROR_REPORTING.logToConsole,
      reportToMonitoring: ERROR_REPORTING.enabled,
    };
    
    const mergedConfig = { ...defaultConfig, ...config };
    
    const formattedError: FormattedError = {
      type: ErrorType.AUTHENTICATION,
      message: 'Erro de autenticação. Por favor, faça login novamente.',
      originalError: error,
      timestamp: Date.now(),
      context,
    };
    
    this.processError(formattedError, mergedConfig);
    
    return formattedError;
  }
  
  /**
   * Trata erros gerais
   */
  public handleError(
    error: any,
    context?: Record<string, any>,
    config?: Partial<ErrorNotificationConfig>
  ): FormattedError {
    const defaultConfig: ErrorNotificationConfig = {
      showNotification: true,
      logToConsole: ERROR_REPORTING.logToConsole,
      reportToMonitoring: ERROR_REPORTING.enabled,
    };
    
    const mergedConfig = { ...defaultConfig, ...config };
    
    const formattedError: FormattedError = {
      type: ErrorType.UNKNOWN,
      message: error.message || 'Ocorreu um erro inesperado',
      originalError: error,
      timestamp: Date.now(),
      context,
    };
    
    this.processError(formattedError, mergedConfig);
    
    return formattedError;
  }
  
  /**
   * Processa um erro formatado
   */
  private processError(
    formattedError: FormattedError,
    config: ErrorNotificationConfig
  ): void {
    // Log no console (em desenvolvimento)
    if (config.logToConsole) {
      console.error('[ErrorHandler]', formattedError);
    }
    
    // Envia para serviço de monitoramento (Sentry)
    if (config.reportToMonitoring && ERROR_REPORTING.enabled) {
      this.reportToMonitoring(formattedError);
    }
    
    // Notifica callbacks registrados (para UI)
    if (config.showNotification) {
      this.notifyCallbacks(formattedError);
    }
  }
  
  /**
   * Envia erro para serviço de monitoramento (Sentry)
   */
  private reportToMonitoring(error: FormattedError): void {
    if (window.Sentry && ERROR_REPORTING.sentryDsn) {
      window.Sentry.withScope((scope) => {
        // Adiciona informações de contexto
        scope.setLevel('error');
        
        // Adiciona tags para facilitar filtragem no Sentry
        scope.setTags({
          error_type: error.type,
          environment: ENV.current,
        });
        
        // Adiciona contexto adicional
        if (error.context) {
          scope.setContext('error_context', error.context);
        }
        
        if (error.details) {
          scope.setContext('error_details', error.details);
        }
        
        // Captura exceção
        window.Sentry.captureException(error.originalError);
      });
    }
  }
  
  /**
   * Notifica todos os callbacks registrados
   */
  private notifyCallbacks(error: FormattedError): void {
    this.notificationCallbacks.forEach((callback) => {
      try {
        callback(error);
      } catch (e) {
        // Previne falhas se um callback lançar exceções
        console.error('Erro ao executar callback de notificação:', e);
      }
    });
  }

  /**
   * Cria um erro de validação formatado
   * @param message Mensagem de erro
   * @param details Detalhes do erro (geralmente campos inválidos)
   */
  public createValidationError(message: string, details?: Record<string, string>): AppError {
    return {
      type: ErrorType.VALIDATION,
      message,
      details,
      timestamp: Date.now(),
      source: 'validation',
    };
  }
}

/**
 * Instância global do ErrorHandler
 */
export const errorHandler = ErrorHandler.getInstance();

/**
 * Configura tratamento global de erros não capturados
 */
export function setupGlobalErrorHandling(): void {
  // Tratamento de erros não capturados
  window.addEventListener('error', (event) => {
    if (ERROR_REPORTING.captureAllErrors) {
      errorHandler.handleError(event.error, {
        source: 'window.onerror',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      });
    }
  });
  
  // Tratamento de promessas rejeitadas não capturadas
  window.addEventListener('unhandledrejection', (event) => {
    if (ERROR_REPORTING.captureAllErrors) {
      errorHandler.handleError(event.reason, {
        source: 'unhandledrejection',
        promise: event.promise,
      });
    }
  });
}

// Interface para Sentry no window
declare global {
  interface Window {
    Sentry?: {
      captureException: (error: any) => void;
      withScope: (callback: (scope: any) => void) => void;
    };
  }
}

export default errorHandler; 