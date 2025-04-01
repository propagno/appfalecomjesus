import { useState, useEffect, useCallback, useRef } from 'react';
import { Message } from '../types';
import { API_URLS } from '../../../shared/constants/config';

/**
 * Hook para gerenciar streaming de respostas da IA
 * Implementação do item 10.4.2 - Streaming de Respostas
 */
export const useStreamingResponse = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamedContent, setStreamedContent] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  
  // Efeito para limpar a conexão quando o componente é desmontado
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);
  
  /**
   * Inicia o streaming de uma resposta da IA
   * @param sessionId ID da sessão de chat
   * @param messageId ID da mensagem que será atualizada com o streaming
   * @param onComplete Callback chamado quando o streaming termina
   */
  const startStreaming = useCallback((
    sessionId: string, 
    messageId: string,
    onComplete?: (message: Message) => void
  ) => {
    // Limpar qualquer streaming anterior
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }
    
    setError(null);
    setIsStreaming(true);
    setIsTyping(true);
    setStreamedContent('');
    
    const url = `${API_URLS.chat}/stream/${sessionId}?messageId=${messageId}`;
    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;
    
    // Buffer para armazenar o conteúdo completo
    let fullContent = '';
    
    // Processar cada chunk de texto recebido
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Se for o token de conclusão, finalizar o streaming
        if (data.done) {
          setIsStreaming(false);
          setIsTyping(false);
          eventSource.close();
          
          // Chamar callback com a mensagem completa
          if (onComplete) {
            onComplete({
              id: messageId,
              content: fullContent,
              type: 'assistant',
              timestamp: new Date().toISOString()
            });
          }
          return;
        }
        
        // Adicionar novo chunk ao conteúdo e atualizar o texto
        if (data.content) {
          fullContent += data.content;
          setStreamedContent(fullContent);
          
          // Simulação de digitação natural
          const typingDelay = Math.min(data.content.length * 10, 300);
          setTimeout(() => setIsTyping(false), typingDelay);
        }
      } catch (err) {
        console.error('Erro ao processar stream:', err);
        setError(err instanceof Error ? err : new Error('Erro desconhecido no streaming'));
        eventSource.close();
        setIsStreaming(false);
        setIsTyping(false);
      }
    };
    
    // Tratar erros de conexão
    eventSource.onerror = (err) => {
      console.error('Erro de conexão SSE:', err);
      setError(new Error('Erro de conexão com o servidor'));
      eventSource.close();
      setIsStreaming(false);
      setIsTyping(false);
      
      // Tentar entregar uma mensagem completa em caso de erro
      if (fullContent && onComplete) {
        onComplete({
          id: messageId,
          content: fullContent + '\n\n_Conexão interrompida. A resposta pode estar incompleta._',
          type: 'assistant',
          timestamp: new Date().toISOString()
        });
      }
    };
    
    return () => {
      eventSource.close();
      setIsStreaming(false);
      setIsTyping(false);
    };
  }, []);
  
  /**
   * Cancela o streaming atual
   */
  const stopStreaming = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setIsStreaming(false);
      setIsTyping(false);
    }
  }, []);
  
  return {
    isStreaming,
    isTyping,
    streamedContent,
    error,
    startStreaming,
    stopStreaming
  };
};

export default useStreamingResponse; 