import { useState, useCallback, useEffect } from 'react';
import { nanoid } from 'nanoid';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthContext } from '../../../features/auth/contexts/AuthContext';
import chatService from '../api/chatService';
import {
  Message,
  MessageType,
  SendMessageRequest,
  MessageLimitInfo,
  ChatHistory,
  ChatHistoryResponse,
  WatchAdResult
} from '../types';
import { toast } from 'react-toastify';

/**
 * Hook para gerenciar o estado e operações do chat
 */
export const useChat = (sessionId?: string) => {
  const queryClient = useQueryClient();
  const { user } = useAuthContext();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [activeSessionId, setActiveSessionId] = useState<string | undefined>(sessionId);

  // Buscar limite de mensagens
  const {
    data: messageLimitInfo,
    isLoading: isLimitLoading,
    refetch: refetchLimit
  } = useQuery({
    queryKey: ['chatLimit'],
    queryFn: chatService.checkMessageLimit,
    enabled: !!user
  });

  // Buscar histórico de mensagens da sessão atual (se houver)
  const {
    data: sessionData,
    isLoading: isSessionLoading
  } = useQuery({
    queryKey: ['chatSession', activeSessionId],
    queryFn: () => chatService.getSession(activeSessionId!),
    enabled: !!activeSessionId && !!user
  });

  // Buscar histórico de sessões
  const {
    data: chatHistory,
    isLoading: isHistoryLoading
  } = useQuery({
    queryKey: ['chatHistory'],
    queryFn: () => chatService.getHistory(),
    enabled: !!user
  });

  // Efeito para atualizar mensagens quando a sessão mudar
  useEffect(() => {
    if (sessionData) {
      const typedData = sessionData as ChatHistoryResponse;
      if (typedData.sessions && typedData.sessions.length > 0) {
        setMessages(typedData.sessions[0].messages || []);
      }
    }
  }, [sessionData]);

  // Enviar mensagem
  const sendMessageMutation = useMutation({
    mutationFn: chatService.sendMessage,
    onMutate: async (variables) => {
      // Otimisticamente atualizar a UI
      const userMessage: Message = {
        id: nanoid(),
        content: variables.content,
        type: 'user',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, userMessage]);
      
      // Adicionar mensagem de carregamento
      const loadingMessage: Message = {
        id: nanoid(),
        content: '',
        type: 'assistant',
        timestamp: new Date().toISOString(),
        isLoading: true
      };

      setMessages(prev => [...prev, loadingMessage]);
      setIsTyping(true);

      return { userMessage, loadingMessage };
    },
    onSuccess: (response, variables, context) => {
      // Remover mensagem de carregamento e adicionar resposta real
      if (context) {
        setMessages(prev => 
          prev.filter(msg => msg.id !== context.loadingMessage.id)
            .concat([response.message])
        );
      }
      
      // Atualizar limite de mensagens
      if (response.messageLimit) {
        queryClient.setQueryData(['chatLimit'], response.messageLimit);
      }

      // Atualizar ID da sessão se for nova
      if (response.session && !activeSessionId) {
        setActiveSessionId(response.session.id);
      }

      // Invalidar consultas para recarregar histórico
      queryClient.invalidateQueries({ queryKey: ['chatHistory'] });
      if (activeSessionId) {
        queryClient.invalidateQueries({ queryKey: ['chatSession', activeSessionId] });
      }
    },
    onError: (error, variables, context) => {
      // Remover mensagem de carregamento em caso de erro
      if (context) {
        setMessages(prev => 
          prev.filter(msg => msg.id !== context.loadingMessage.id)
            .concat([{
              id: nanoid(),
              content: 'Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.',
              type: 'system',
              timestamp: new Date().toISOString()
            }])
        );
      }
    },
    onSettled: () => {
      setIsTyping(false);
    }
  });

  // Registrar anúncio assistido
  const watchAdMutation = useMutation({
    mutationFn: chatService.rewardAdWatched,
    onSuccess: () => {
      // Atualizar limite de mensagens
      refetchLimit();
    }
  });

  // Limpar histórico
  const clearHistoryMutation = useMutation({
    mutationFn: chatService.deleteHistory,
    onSuccess: () => {
      setMessages([]);
      setActiveSessionId(undefined);
      queryClient.invalidateQueries({ queryKey: ['chatHistory'] });
    }
  });

  // Excluir sessão específica
  const deleteSessionMutation = useMutation({
    mutationFn: chatService.deleteSession,
    onSuccess: (_, variables) => {
      if (variables === activeSessionId) {
        setMessages([]);
        setActiveSessionId(undefined);
      }
      queryClient.invalidateQueries({ queryKey: ['chatHistory'] });
    }
  });

  // Atualizar título da sessão
  const updateSessionTitleMutation = useMutation({
    mutationFn: ({ sessionId, title }: { sessionId: string; title: string }) => 
      chatService.updateSessionTitle(sessionId, title),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['chatHistory'] });
      if (variables.sessionId === activeSessionId) {
        queryClient.invalidateQueries({ queryKey: ['chatSession', activeSessionId] });
      }
    }
  });

  // Criar nova sessão
  const createSessionMutation = useMutation({
    mutationFn: chatService.createSession,
    onSuccess: (response) => {
      setActiveSessionId(response.sessionId);
      setMessages([]);
    }
  });

  // Funções auxiliares
  const sendMessage = useCallback((content: string) => {
    if (!content.trim()) return;
    
    const request: SendMessageRequest = {
      content,
      sessionId: activeSessionId
    };
    
    return sendMessageMutation.mutateAsync(request);
  }, [activeSessionId, sendMessageMutation]);

  const watchAd = useCallback(async (): Promise<WatchAdResult> => {
    return watchAdMutation.mutateAsync();
  }, [watchAdMutation]);

  const clearHistory = useCallback(() => {
    return clearHistoryMutation.mutateAsync();
  }, [clearHistoryMutation]);

  const deleteSession = useCallback((sessionId: string) => {
    return deleteSessionMutation.mutateAsync(sessionId);
  }, [deleteSessionMutation]);

  const updateSessionTitle = useCallback((sessionId: string, title: string) => {
    return updateSessionTitleMutation.mutateAsync({ sessionId, title });
  }, [updateSessionTitleMutation]);

  const createNewSession = useCallback(() => {
    return createSessionMutation.mutateAsync();
  }, [createSessionMutation]);

  const switchSession = useCallback((sessionId: string) => {
    setActiveSessionId(sessionId);
  }, []);

  // Verificar se o usuário ainda tem mensagens disponíveis (plano Free)
  const canSendMessage = useCallback(() => {
    if (!messageLimitInfo) return true;
    if (messageLimitInfo.isPremium) return true;
    return messageLimitInfo.remaining > 0;
  }, [messageLimitInfo]);

  // Retornar o estado e funções
  return {
    // Estado
    messages,
    isTyping,
    activeSessionId,
    messageLimitInfo,
    chatHistory: chatHistory?.sessions || [],
    
    // Estado de carregamento
    isLoading: isSessionLoading || sendMessageMutation.isPending,
    isLimitLoading,
    isHistoryLoading,
    
    // Ações
    sendMessage,
    watchAd,
    clearHistory,
    deleteSession,
    updateSessionTitle,
    createNewSession,
    switchSession,
    
    // Helpers
    canSendMessage,
    
    // Estado das operações
    isSending: sendMessageMutation.isPending,
    isWatchingAd: watchAdMutation.isPending,
    isClearing: clearHistoryMutation.isPending,
    isDeleting: deleteSessionMutation.isPending,
    isUpdatingTitle: updateSessionTitleMutation.isPending,
    isCreatingSession: createSessionMutation.isPending
  };
};

export default useChat; 