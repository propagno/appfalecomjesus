import React, { useState, useRef, useEffect } from 'react';
import { useChatContext } from '../contexts/ChatContext';

/**
 * Componente de formulário para enviar mensagens no chat
 */
const ChatForm: React.FC = () => {
  const { 
    sendMessage, 
    isSending,
    canSendMessage,
    messageLimitInfo
  } = useChatContext();
  
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  // Ajustar altura do textarea automaticamente
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  };
  
  // Resetar altura quando a mensagem for enviada
  useEffect(() => {
    if (!message && textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }, [message]);
  
  // Lidar com mudanças no textarea
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    adjustTextareaHeight();
  };
  
  // Lidar com envio do formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim() || isSending) return;
    
    // Verificar se pode enviar mensagem (limite não atingido)
    if (!canSendMessage()) {
      return;
    }
    
    try {
      await sendMessage(message.trim());
      setMessage('');
      
      // Reset da altura do textarea
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
    }
  };
  
  // Lidar com tecla Enter (enviar) e Shift+Enter (nova linha)
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };
  
  // Determinar se deve mostrar aviso de limite
  const showLimitWarning = messageLimitInfo && !messageLimitInfo.isPremium && messageLimitInfo.remaining <= 1;
  
  return (
    <form 
      onSubmit={handleSubmit} 
      className="border-t border-gray-200 bg-white p-4 sticky bottom-0"
    >
      {/* Aviso de limite de mensagens */}
      {showLimitWarning && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-3 py-2 rounded-md mb-2 text-sm">
          {messageLimitInfo.remaining === 0
            ? 'Você atingiu o limite diário de mensagens. Assista a um anúncio para continuar.'
            : `Você tem apenas ${messageLimitInfo.remaining} mensagem restante hoje.`
          }
        </div>
      )}
      
      <div className="flex items-end space-x-2">
        <div className="flex-grow relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder="Digite uma mensagem..."
            className="w-full border border-gray-300 rounded-lg py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[40px] max-h-[150px] pr-10"
            rows={1}
            disabled={isSending || !canSendMessage()}
          />
          
          {/* Contador de caracteres (opcional) */}
          {message.length > 0 && (
            <div className="absolute bottom-2 right-2 text-xs text-gray-400">
              {message.length}
            </div>
          )}
        </div>
        
        <button
          type="submit"
          disabled={!message.trim() || isSending || !canSendMessage()}
          className="bg-blue-600 text-white rounded-full p-2 h-10 w-10 flex items-center justify-center focus:outline-none hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Enviar mensagem"
        >
          {isSending ? (
            <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" />
          ) : (
            <svg 
              className="w-5 h-5" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" 
              />
            </svg>
          )}
        </button>
      </div>
    </form>
  );
};

export default ChatForm; 