import { 
  useQuery, 
  useMutation, 
  UseQueryOptions, 
  UseMutationOptions,
  UseQueryResult,
  UseMutationResult,
  QueryKey
} from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { ApiError } from '../services/api';
import { CACHE_CONFIG } from '../constants/config';

/**
 * Hook genérico para fazer consultas usando React Query
 * 
 * @param queryKey - Chave única para identificar a query no cache
 * @param queryFn - Função que faz a requisição à API
 * @param options - Opções adicionais do React Query
 * @returns Resultado da query
 */
export function useApiQuery<TData, TError = ApiError>(
  queryKey: QueryKey,
  queryFn: () => Promise<TData>,
  options?: UseQueryOptions<TData, TError, TData, QueryKey>
): UseQueryResult<TData, TError> {
  return useQuery<TData, TError, TData, QueryKey>({
    queryKey,
    queryFn,
    ...options
  });
}

/**
 * Hook para fazer consultas de entidades específicas usando React Query
 * 
 * @param entityType - Tipo da entidade (ex: 'user', 'study', 'bible')
 * @param entityId - ID da entidade
 * @param fetchFn - Função que faz a requisição à API
 * @param options - Opções adicionais do React Query
 * @returns Resultado da query
 */
export function useEntityQuery<TData, TError = ApiError>(
  entityType: string,
  entityId: string | number | null | undefined,
  fetchFn: () => Promise<TData>,
  options?: UseQueryOptions<TData, TError, TData, [string, string | number | null | undefined]>
): UseQueryResult<TData, TError> {
  return useApiQuery<TData, TError>(
    [entityType, entityId],
    fetchFn,
    {
      // Não executar a query se entityId for nulo ou indefinido
      enabled: entityId !== null && entityId !== undefined && options?.enabled !== false,
      ...options
    }
  );
}

/**
 * Hook para fazer consultas de listas usando React Query
 * 
 * @param entityType - Tipo da entidade (ex: 'users', 'studies', 'bibles')
 * @param params - Parâmetros da consulta (ex: paginação, filtros)
 * @param fetchFn - Função que faz a requisição à API
 * @param options - Opções adicionais do React Query
 * @returns Resultado da query
 */
export function useListQuery<TData, TParams extends Record<string, any>, TError = ApiError>(
  entityType: string,
  params: TParams,
  fetchFn: () => Promise<TData>,
  options?: UseQueryOptions<TData, TError, TData, [string, TParams]>
): UseQueryResult<TData, TError> {
  return useApiQuery<TData, TError>(
    [entityType, params],
    fetchFn,
    {
      // Cache mais curto para listas, pois tendem a mudar mais frequentemente
      staleTime: CACHE_CONFIG.ttl / 2,
      ...options
    }
  );
}

/**
 * Hook para fazer mutações usando React Query
 * 
 * @param mutationFn - Função que faz a mutação na API
 * @param options - Opções adicionais do React Query
 * @returns Resultado da mutação
 */
export function useApiMutation<TData, TVariables, TContext = unknown, TError = ApiError>(
  mutationFn: (variables: TVariables) => Promise<TData>,
  options?: UseMutationOptions<TData, TError, TVariables, TContext>
): UseMutationResult<TData, TError, TVariables, TContext> {
  return useMutation<TData, TError, TVariables, TContext>({
    mutationFn,
    ...options
  });
}

/**
 * Hook para criar uma mutação com confirmação de sucesso
 * 
 * @param mutationFn - Função que faz a mutação na API
 * @param options - Opções adicionais do React Query
 * @returns Resultado da mutação
 */
export function useApiMutationWithToast<TData, TVariables, TContext = unknown, TError = ApiError>(
  mutationFn: (variables: TVariables) => Promise<TData>,
  successMessage: string = 'Operação realizada com sucesso!',
  options?: UseMutationOptions<TData, TError, TVariables, TContext>
): UseMutationResult<TData, TError, TVariables, TContext> {
  // Função para mostrar mensagens de sucesso
  const showSuccessToast = (message: string) => {
    if (window.toast) {
      window.toast.success(message);
    } else {
      console.log('Success:', message);
    }
  };

  return useApiMutation<TData, TVariables, TContext, TError>(
    mutationFn,
    {
      ...options,
      onSuccess: (data, variables, context) => {
        // Mostrar toast de sucesso
        showSuccessToast(successMessage);

        // Executar callback de sucesso personalizado, se fornecido
        if (options?.onSuccess) {
          options.onSuccess(data, variables, context);
        }
      }
    }
  );
}

// Adiciona a declaração do toast global
declare global {
  interface Window {
    toast?: {
      success: (message: string) => void;
      error: (message: string) => void;
      info: (message: string) => void;
      warning: (message: string) => void;
    };
  }
}

export default {
  useApiQuery,
  useEntityQuery,
  useListQuery,
  useApiMutation,
  useApiMutationWithToast
}; 