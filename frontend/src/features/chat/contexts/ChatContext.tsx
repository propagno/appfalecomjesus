import React, { createContext, ReactNode, useContext } from 'react';
import useChat from '../hooks/useChat';
import { 
  Message, 
  MessageLimitInfo, 
  ChatHistory,
  WatchAdResult
} from '../types';

// Interface para o valor do contexto de chat
interface ChatContextValue {
  // Estado
  messages: Message[];
  isTyping: boolean;
  activeSessionId?: string;
  messageLimitInfo?: MessageLimitInfo;
  chatHistory: ChatHistory[];
  
  // Estado de carregamento
  isLoading: boolean;
  isLimitLoading: boolean;
  isHistoryLoading: boolean;
  
  // Ações
  sendMessage: (content: string) => Promise<any>;
  watchAd: () => Promise<WatchAdResult>;
  clearHistory: () => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  updateSessionTitle: (sessionId: string, title: string) => Promise<void>;
  createNewSession: () => Promise<{ sessionId: string }>;
  switchSession: (sessionId: string) => void;
  
  // Helpers
  canSendMessage: () => boolean;
  
  // Estado das operações
  isSending: boolean;
  isWatchingAd: boolean;
  isClearing: boolean;
  isDeleting: boolean;
  isUpdatingTitle: boolean;
  isCreatingSession: boolean;
}

// Criar o contexto
const ChatContext = createContext<ChatContextValue | undefined>(undefined);

// Props para o provedor do contexto
interface ChatProviderProps {
  children: ReactNode;
  sessionId?: string;
}

/**
 * Provedor do contexto de chat
 */
export const ChatProvider: React.FC<ChatProviderProps> = ({ 
  children,
  sessionId 
}) => {
  const chat = useChat(sessionId);
  
  return (
    <ChatContext.Provider value={chat}>
      {children}
    </ChatContext.Provider>
  );
};

/**
 * Hook para acessar o contexto de chat
 */
export const useChatContext = () => {
  const context = useContext(ChatContext);
  
  if (context === undefined) {
    throw new Error('useChatContext deve ser usado dentro de um ChatProvider');
  }
  
  return context;
};

export default ChatContext; 