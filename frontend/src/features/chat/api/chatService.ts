import api from '../../../shared/services/api';
import { API_URLS } from '../../../shared/constants/config';
import {
  SendMessageRequest,
  SendMessageResponse,
  ChatHistoryResponse,
  MessageLimitInfo,
  WatchAdResult
} from '../types';

/**
 * Serviço para operações relacionadas ao chat com IA
 * Implementação do item 10.4.1 - Integração com MS-ChatIA
 */
const chatService = {
  /**
   * Envia uma mensagem para o chat IA e obtém a resposta
   * Endpoint: POST /api/chat/message
   */
  sendMessage: async (request: SendMessageRequest): Promise<SendMessageResponse> => {
    const response = await api.chatApi.post<SendMessageResponse>(`/message`, request);
    return response.data;
  },

  /**
   * Obtém o histórico de conversas do usuário
   * Endpoint: GET /api/chat/history
   */
  getHistory: async (page = 1, limit = 10): Promise<ChatHistoryResponse> => {
    const response = await api.chatApi.get<ChatHistoryResponse>(`/history`, {
      params: { page, limit }
    });
    return response.data;
  },

  /**
   * Obtém uma sessão específica de chat pelo ID
   * Endpoint: GET /api/chat/sessions/:id
   */
  getSession: async (sessionId: string): Promise<ChatHistoryResponse> => {
    const response = await api.chatApi.get<ChatHistoryResponse>(`/sessions/${sessionId}`);
    return response.data;
  },

  /**
   * Cria uma nova sessão de chat
   * Endpoint: POST /api/chat/sessions
   */
  createSession: async (): Promise<{ sessionId: string }> => {
    const response = await api.chatApi.post<{ sessionId: string }>(`/sessions`);
    return response.data;
  },

  /**
   * Atualiza o título de uma sessão
   * Endpoint: PUT /api/chat/sessions/:id
   */
  updateSessionTitle: async (sessionId: string, title: string): Promise<void> => {
    await api.chatApi.put(`/sessions/${sessionId}`, { title });
  },

  /**
   * Exclui uma sessão de chat
   * Endpoint: DELETE /api/chat/sessions/:id
   */
  deleteSession: async (sessionId: string): Promise<void> => {
    await api.chatApi.delete(`/sessions/${sessionId}`);
  },

  /**
   * Limpa todo o histórico de chat do usuário
   * Endpoint: DELETE /api/chat/history
   */
  deleteHistory: async (): Promise<void> => {
    await api.chatApi.delete(`/history`);
  },

  /**
   * Verifica o limite de mensagens do usuário (para plano Free)
   * Endpoint: GET /api/chat/limit
   */
  checkMessageLimit: async (): Promise<MessageLimitInfo> => {
    const response = await api.chatApi.get<MessageLimitInfo>(`/limit`);
    return response.data;
  },

  /**
   * Registra uma recompensa por assistir anúncio
   * Endpoint: POST /api/monetization/ad-reward
   */
  rewardAdWatched: async (): Promise<WatchAdResult> => {
    const response = await api.monetizationApi.post<WatchAdResult>(`/ad-reward`, {
      ad_type: 'video',
      reward_type: 'chat_messages',
    });
    return response.data;
  },
  
  /**
   * Inicia uma conexão de streaming para mensagens
   * Endpoint: GET /api/chat/stream/:sessionId
   */
  getMessageStream: (sessionId: string, onMessage: (data: any) => void, onError: (error: any) => void) => {
    const eventSource = new EventSource(`${API_URLS.chat}/stream/${sessionId}`);
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        onError(error);
      }
    };
    
    eventSource.onerror = (error) => {
      onError(error);
      eventSource.close();
    };
    
    return {
      close: () => eventSource.close()
    };
  }
};

export default chatService; 