import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { v4 as uuidv4 } from 'uuid';
import chatService from '../api/chatService';
import { Message, ChatHistory, SendMessageResponse, SendMessageRequest } from '../types';
import { ChatQueryKeys } from '../constants';

/**
 * Hook que encapsula todas as queries e mutations relacionadas ao chat usando React Query
 * Implementação do item 10.4.3 - Integração com React Query
 */
export const useChatQuery = () => {
  const queryClient = useQueryClient();

  // Query para buscar histórico de sessões de chat
  const useSessionsQuery = (page = 1, limit = 10) => 
    useQuery({
      queryKey: [ChatQueryKeys.SESSIONS, page, limit],
      queryFn: () => chatService.getHistory(page, limit),
    });

  // Query para buscar uma sessão específica
  const useSessionQuery = (sessionId: string) => 
    useQuery({
      queryKey: [ChatQueryKeys.SESSION, sessionId],
      queryFn: () => chatService.getSession(sessionId),
      enabled: !!sessionId,
    });

  // Query para buscar o limite de mensagens do usuário
  const useMessageLimitQuery = () => 
    useQuery({
      queryKey: [ChatQueryKeys.MESSAGE_LIMIT],
      queryFn: chatService.checkMessageLimit,
      refetchInterval: 30000, // Atualiza a cada 30 segundos
    });

  // Mutation para enviar mensagem para a IA
  const useSendMessageMutation = () => 
    useMutation({
      mutationFn: (params: SendMessageRequest) => 
        chatService.sendMessage(params),
      onSuccess: (response: SendMessageResponse, variables) => {
        // Invalidar a query da sessão para refletir as novas mensagens
        if (variables.sessionId) {
          queryClient.invalidateQueries({ 
            queryKey: [ChatQueryKeys.SESSION, variables.sessionId]
          });
        }
        
        // Atualizar o cache de histórico de mensagens
        queryClient.invalidateQueries({
          queryKey: [ChatQueryKeys.SESSIONS]
        });
      },
    });

  // Mutation para criar nova sessão de chat
  const useCreateSessionMutation = () => 
    useMutation({
      mutationFn: chatService.createSession,
      onSuccess: () => {
        // Invalidar a query de sessões para refletir a nova sessão
        queryClient.invalidateQueries({ queryKey: [ChatQueryKeys.SESSIONS] });
      },
    });

  // Mutation para atualizar o título de uma sessão
  const useUpdateSessionTitleMutation = () => 
    useMutation({
      mutationFn: (params: { sessionId: string; title: string }) => 
        chatService.updateSessionTitle(params.sessionId, params.title),
      onSuccess: (_, variables) => {
        // Invalidar queries específicas
        queryClient.invalidateQueries({ queryKey: [ChatQueryKeys.SESSIONS] });
        queryClient.invalidateQueries({ 
          queryKey: [ChatQueryKeys.SESSION, variables.sessionId]
        });
      },
    });

  // Mutation para deletar uma sessão de chat
  const useDeleteSessionMutation = () => 
    useMutation({
      mutationFn: chatService.deleteSession,
      onSuccess: (_, sessionId) => {
        // Invalidar a query de sessões
        queryClient.invalidateQueries({ queryKey: [ChatQueryKeys.SESSIONS] });
        
        // Remover diretamente do cache a sessão deletada
        queryClient.removeQueries({ 
          queryKey: [ChatQueryKeys.SESSION, sessionId]
        });
      },
    });

  // Mutation para limpar todo o histórico de chat
  const useClearHistoryMutation = () => 
    useMutation({
      mutationFn: chatService.deleteHistory,
      onSuccess: () => {
        // Invalidar todas as queries relacionadas ao chat
        queryClient.invalidateQueries({ queryKey: [ChatQueryKeys.SESSIONS] });
        queryClient.invalidateQueries({ 
          queryKey: [ChatQueryKeys.SESSION]
        });
      },
    });

  // Mutation para registrar recompensa por assistir anúncio
  const useRegisterAdRewardMutation = () => 
    useMutation({
      mutationFn: chatService.rewardAdWatched,
      onSuccess: () => {
        // Atualizar o limite de mensagens
        queryClient.invalidateQueries({ 
          queryKey: [ChatQueryKeys.MESSAGE_LIMIT]
        });
      },
    });

  return {
    useSessionsQuery,
    useSessionQuery,
    useMessageLimitQuery,
    useSendMessageMutation,
    useCreateSessionMutation,
    useUpdateSessionTitleMutation,
    useDeleteSessionMutation,
    useClearHistoryMutation,
    useRegisterAdRewardMutation,
  };
};

export default useChatQuery; 