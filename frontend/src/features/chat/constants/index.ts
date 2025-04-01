/**
 * Constantes usadas no feature de chat
 */

/**
 * Chaves para as queries do React Query no chat
 */
export enum ChatQueryKeys {
  SESSIONS = 'chatSessions',
  SESSION = 'chatSession',
  MESSAGE_LIMIT = 'chatMessageLimit',
}

/**
 * Tipos de mensagens no chat
 */
export enum MessageType {
  USER = 'user',
  ASSISTANT = 'assistant',
} 