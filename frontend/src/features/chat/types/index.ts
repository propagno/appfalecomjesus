/**
 * Tipo de mensagem no chat
 */
export type MessageType = 'user' | 'assistant' | 'system';

/**
 * Interface para uma mensagem individual no chat
 */
export interface Message {
  id: string;
  content: string;
  type: MessageType;
  timestamp: string;
  isLoading?: boolean;
}

/**
 * Interface para histórico de mensagens
 */
export interface ChatHistory {
  id: string;
  sessionId?: string;
  title?: string;
  messages: Message[];
  lastMessage?: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Configurações do chat
 */
export interface ChatSettings {
  voiceEnabled: boolean;
  autoRead: boolean;
  fontSize: 'small' | 'medium' | 'large';
}

/**
 * Estado global do chat
 */
export interface ChatState {
  activeSession: ChatHistory | null;
  allSessions: ChatHistory[];
  messages: Message[];
  isLoading: boolean;
  isTyping: boolean;
  error: ChatError | null;
  settings: ChatSettings;
  messageLimit: MessageLimitInfo;
}

/**
 * Informações sobre o limite de mensagens para o plano Free
 */
export interface MessageLimitInfo {
  limit: number;
  used: number;
  remaining: number;
  resetDate: string;
  isPremium: boolean;
}

/**
 * Estrutura para envio de mensagem
 */
export interface SendMessageRequest {
  content: string;
  sessionId?: string;
}

/**
 * Estrutura para resposta da API de envio de mensagem
 */
export interface SendMessageResponse {
  message: Message;
  session: {
    id: string;
    title: string;
    messagesCount: number;
  };
  messageLimit: MessageLimitInfo;
}

/**
 * Estrutura de resposta do histórico de chat
 */
export interface ChatHistoryResponse {
  sessions: ChatHistory[];
}

/**
 * Estrutura de erro específico de chat
 */
export interface ChatError {
  code: string;
  message: string;
  details?: string;
}

/**
 * Interface para recompensa por assistir anúncios
 */
export interface AdReward {
  type: 'chat_messages';
  value: number;
  grantedAt: string;
  expiresAt: string;
}

/**
 * Resultado da tentativa de assistir anúncio
 */
export interface WatchAdResult {
  success: boolean;
  reward?: AdReward;
  error?: string;
} 