import { useState, useCallback, useEffect } from 'react';
import { AxiosRequestConfig } from 'axios';
import { ApiError } from '../services/api';
import { CACHE_CONFIG, FEATURES } from '../constants/config';
import { getFromCache, saveToCache } from '../utils/cache';

/**
 * Interface para o hook useApi
 */
export interface UseApiResult<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
  execute: (params?: any) => Promise<T>;
  reset: () => void;
}

/**
 * Hook para fazer requisições à API com estado de loading e erro
 * @param apiMethod - Método da API a ser chamado (ex: authApi.get)
 * @param url - URL da requisição (sem o base URL)
 * @param config - Configurações adicionais do Axios
 * @param immediate - Se true, executa a requisição imediatamente ao montar o componente
 * @param cacheKey - Chave para armazenar em cache (se fornecida, ativa o cache)
 * @param cacheTtl - Tempo de vida do cache em ms (padrão: CACHE_CONFIG.ttl)
 */
export function useApi<T = any, P = any>(
  apiMethod: (url: string, data?: any, config?: AxiosRequestConfig) => Promise<T>,
  url: string,
  config?: AxiosRequestConfig,
  immediate = false,
  cacheKey?: string,
  cacheTtl = CACHE_CONFIG.ttl
): UseApiResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(immediate);
  const [error, setError] = useState<ApiError | null>(null);

  // Função para executar a requisição
  const execute = useCallback(
    async (params?: P): Promise<T> => {
      // Limpa erros anteriores
      setError(null);
      setLoading(true);

      try {
        // Verifica se há dados em cache primeiro
        if (cacheKey && FEATURES.offlineMode) {
          const cachedData = getFromCache<T>(`${CACHE_CONFIG.prefix}:${cacheKey}`);
          if (cachedData) {
            setData(cachedData);
            setLoading(false);
            return cachedData;
          }
        }

        // Se não houver cache, ou estiver expirado, faz a requisição
        const method = url.includes('?') ? url : url + (params ? '?' + new URLSearchParams(params as any).toString() : '');
        const isGetMethod = typeof params !== 'object' || params === null || Object.keys(params).length === 0;
        
        let result: T;
        
        // Determina se é um GET ou outro método (POST, PUT, etc)
        if (isGetMethod) {
          result = await apiMethod(method, config);
        } else {
          result = await apiMethod(url, params, config);
        }

        // Salva o resultado
        setData(result);
        
        // Armazena em cache se necessário
        if (cacheKey && FEATURES.offlineMode) {
          saveToCache(`${CACHE_CONFIG.prefix}:${cacheKey}`, result, cacheTtl);
        }
        
        return result;
      } catch (err) {
        const apiError = err as ApiError;
        setError(apiError);
        throw apiError;
      } finally {
        setLoading(false);
      }
    },
    [apiMethod, url, config, cacheKey, cacheTtl]
  );

  // Reset do estado
  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  // Se immediate, executa a requisição ao montar o componente
  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [execute, immediate]);

  return { data, loading, error, execute, reset };
}

/**
 * Hook para fazer requisições GET
 */
export function useApiGet<T = any, P = any>(
  apiMethod: (url: string, config?: AxiosRequestConfig) => Promise<T>,
  url: string, 
  config?: AxiosRequestConfig,
  immediate = false,
  cacheKey?: string,
  cacheTtl = CACHE_CONFIG.ttl
): UseApiResult<T> {
  return useApi<T, P>(
    (endpoint, _, cfg) => apiMethod(endpoint, cfg),
    url,
    config,
    immediate,
    cacheKey,
    cacheTtl
  );
}

/**
 * Hook para fazer requisições POST
 */
export function useApiPost<T = any, P = any>(
  apiMethod: (url: string, data?: any, config?: AxiosRequestConfig) => Promise<T>,
  url: string,
  config?: AxiosRequestConfig
): UseApiResult<T> {
  return useApi<T, P>(apiMethod, url, config, false);
}

/**
 * Hook para fazer requisições PUT
 */
export function useApiPut<T = any, P = any>(
  apiMethod: (url: string, data?: any, config?: AxiosRequestConfig) => Promise<T>,
  url: string,
  config?: AxiosRequestConfig
): UseApiResult<T> {
  return useApi<T, P>(apiMethod, url, config, false);
}

/**
 * Hook para fazer requisições DELETE
 */
export function useApiDelete<T = any>(
  apiMethod: (url: string, config?: AxiosRequestConfig) => Promise<T>,
  url: string,
  config?: AxiosRequestConfig
): UseApiResult<T> {
  return useApi<T, null>(
    (endpoint, _, cfg) => apiMethod(endpoint, cfg),
    url,
    config,
    false
  );
} 