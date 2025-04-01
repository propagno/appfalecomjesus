import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { useChatQuery } from '../hooks/useChatQuery';
import useStreamingResponse from '../hooks/useStreamingResponse';
import { 
  Message, 
  ChatHistory, 
  MessageLimitInfo, 
  SendMessageRequest,
  WatchAdResult,
  ChatHistoryResponse
} from '../types';

interface ChatProviderProps {
  children: ReactNode;
}

interface ChatContextValue {
  // Estado
  activeSession: ChatHistory | null;
  sessions: ChatHistory[];
  isLoading: boolean;
  isStreaming: boolean;
  streamingText: string;
  messageLimit: MessageLimitInfo | null;
  error: Error | null;
  
  // Ações
  sendMessage: (message: string, sessionId?: string) => Promise<void>;
  createSession: () => Promise<string>;
  selectSession: (sessionId: string) => Promise<void>;
  updateSessionTitle: (sessionId: string, title: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  clearHistory: () => Promise<void>;
  registerAdReward: () => Promise<WatchAdResult>;
}

// Criar o contexto com valor inicial
const ChatContext = createContext<ChatContextValue | null>(null);

/**
 * Provider que gerencia o estado e as ações do chat
 * Implementação do item 10.4.4 - Migração para React Query
 */
export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  // Estado local
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Hooks de React Query para as operações de chat
  const {
    useSessionsQuery,
    useSessionQuery,
    useMessageLimitQuery,
    useSendMessageMutation,
    useCreateSessionMutation,
    useUpdateSessionTitleMutation,
    useDeleteSessionMutation,
    useClearHistoryMutation,
    useRegisterAdRewardMutation,
  } = useChatQuery();

  // Obter as sessões de chat
  const { data: sessionsData } = useSessionsQuery();
  
  // Obter a sessão ativa
  const { 
    data: activeSessionData, 
    isLoading: isSessionLoading 
  } = useSessionQuery(activeSessionId || '');
  
  // Obter o limite de mensagens
  const { 
    data: messageLimitData, 
    isLoading: isLimitLoading 
  } = useMessageLimitQuery();
  
  // Mutações
  const sendMessageMutation = useSendMessageMutation();
  const createSessionMutation = useCreateSessionMutation();
  const updateSessionTitleMutation = useUpdateSessionTitleMutation();
  const deleteSessionMutation = useDeleteSessionMutation();
  const clearHistoryMutation = useClearHistoryMutation();
  const registerAdRewardMutation = useRegisterAdRewardMutation();

  // Hook de streaming
  const { 
    isStreaming, 
    streamedContent, 
    startStreaming, 
    stopStreaming 
  } = useStreamingResponse();

  /**
   * Seleciona uma sessão de chat
   */
  const selectSession = useCallback(async (sessionId: string) => {
    try {
      setActiveSessionId(sessionId);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao selecionar sessão'));
    }
  }, []);

  /**
   * Cria uma nova sessão de chat
   */
  const createSession = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await createSessionMutation.mutateAsync();
      setActiveSessionId(response.sessionId);
      return response.sessionId;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao criar sessão'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [createSessionMutation]);

  /**
   * Envia uma mensagem para o chat IA
   */
  const sendMessage = useCallback(async (message: string, sessionId?: string) => {
    try {
      setIsLoading(true);
      
      // Garantir que existe uma sessão ativa
      const targetSessionId = sessionId || activeSessionId || await createSession();
      
      // Preparar a requisição
      const request: SendMessageRequest = {
        content: message,
        sessionId: targetSessionId
      };
      
      // Enviar a mensagem com streaming
      const messageId = uuidv4();
      startStreaming(targetSessionId, messageId, (completedMessage) => {
        // Quando o streaming completar, atualizar a query para garantir dados consistentes
        sendMessageMutation.mutate(request);
      });
      
    } catch (err) {
      stopStreaming();
      setError(err instanceof Error ? err : new Error('Erro ao enviar mensagem'));
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [activeSessionId, createSession, sendMessageMutation, startStreaming, stopStreaming]);

  /**
   * Atualiza o título de uma sessão
   */
  const updateSessionTitle = useCallback(async (sessionId: string, title: string) => {
    try {
      await updateSessionTitleMutation.mutateAsync({ sessionId, title });
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao atualizar título'));
      throw err;
    }
  }, [updateSessionTitleMutation]);

  /**
   * Exclui uma sessão de chat
   */
  const deleteSession = useCallback(async (sessionId: string) => {
    try {
      await deleteSessionMutation.mutateAsync(sessionId);
      
      // Se a sessão excluída for a ativa, resetar
      if (sessionId === activeSessionId) {
        setActiveSessionId(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao excluir sessão'));
      throw err;
    }
  }, [deleteSessionMutation, activeSessionId]);

  /**
   * Limpa todo o histórico de chat
   */
  const clearHistory = useCallback(async () => {
    try {
      await clearHistoryMutation.mutateAsync();
      setActiveSessionId(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao limpar histórico'));
      throw err;
    }
  }, [clearHistoryMutation]);

  /**
   * Registra recompensa por assistir anúncio
   */
  const registerAdReward = useCallback(async () => {
    try {
      return await registerAdRewardMutation.mutateAsync();
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao registrar recompensa'));
      throw err;
    }
  }, [registerAdRewardMutation]);

  // Extrair a sessão ativa e sessions do data retornado pelas queries
  const activeSession = activeSessionData && 
    (Array.isArray(activeSessionData.sessions) && activeSessionData.sessions.length > 0
      ? activeSessionData.sessions[0]
      : null);
  
  const sessions = sessionsData?.sessions || [];

  // Valor do contexto
  const contextValue: ChatContextValue = {
    // Estado
    activeSession,
    sessions,
    isLoading: isLoading || isSessionLoading || isLimitLoading,
    isStreaming,
    streamingText: streamedContent,
    messageLimit: messageLimitData || null,
    error,
    
    // Ações
    sendMessage,
    createSession,
    selectSession,
    updateSessionTitle,
    deleteSession,
    clearHistory,
    registerAdReward,
  };

  return (
    <ChatContext.Provider value={contextValue}>
      {children}
    </ChatContext.Provider>
  );
};

/**
 * Hook para usar o contexto do chat
 */
export const useChatContext = () => {
  const context = useContext(ChatContext);
  
  if (!context) {
    throw new Error('useChatContext deve ser usado dentro de um ChatProvider');
  }
  
  return context;
};

export default ChatProvider; 