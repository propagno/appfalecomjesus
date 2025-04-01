/**
 * Exportações centralizadas para o feature de chat
 */

// Componentes existentes
export { default as ChatBubble } from './components/ChatBubble';
export { default as ChatScreen } from './components/ChatScreen';
export { default as ChatSidebar } from './components/ChatSidebar';

// Contexto legado (será substituído gradualmente)
export { ChatProvider as LegacyChatProvider, useChatContext as useLegacyChatContext } from './contexts/ChatContext';

// Páginas
export { default as ChatPage } from './pages/ChatPage';

// Serviço de API
export { default as chatService } from './api/chatService';

// Rotas
export * from './routes';

// Tipos
export * from './types';

// Novos Providers com React Query
export { default as ChatProvider } from './providers/ChatProvider';
export { useChatContext } from './providers/ChatProvider';

// Hooks React Query
export { default as useChatQuery } from './hooks/useChatQuery';
export { default as useStreamingResponse } from './hooks/useStreamingResponse';

// Constantes
export { ChatQueryKeys, MessageType } from './constants'; 