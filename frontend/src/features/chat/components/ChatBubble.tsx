import React, { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Message } from '../types';

interface ChatBubbleProps {
  message: Message;
  onReadAloud?: (text: string) => void;
}

/**
 * Componente que exibe uma mensagem individual no chat
 */
const ChatBubble: React.FC<ChatBubbleProps> = ({ 
  message, 
  onReadAloud 
}) => {
  const [isCopied, setIsCopied] = useState(false);
  
  // Determinar se é uma mensagem do usuário ou da IA
  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';
  
  // Formatar a data relativa (ex: "há 5 minutos")
  const formattedTime = formatDistanceToNow(new Date(message.timestamp), { 
    addSuffix: true,
    locale: ptBR
  });
  
  // Copiar mensagem para a área de transferência
  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
      .then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      });
  };
  
  // Ler mensagem em voz alta
  const handleReadAloud = () => {
    if (onReadAloud) {
      onReadAloud(message.content);
    }
  };
  
  // Estilização condicional baseada no tipo de mensagem
  const bubbleClassName = `
    relative px-4 py-3 rounded-lg max-w-3/4 mb-3
    ${isUser
      ? 'ml-auto bg-blue-600 text-white rounded-tr-none' 
      : isSystem
        ? 'mx-auto bg-gray-100 text-gray-800 italic'
        : 'mr-auto bg-gray-50 text-gray-800 rounded-tl-none border border-gray-200'
    }
    ${message.isLoading ? 'animate-pulse' : ''}
  `;
  
  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : isSystem ? 'items-center' : 'items-start'}`}>
      {/* Mensagem */}
      <div className={bubbleClassName}>
        {message.isLoading ? (
          <div className="flex space-x-2 justify-center items-center h-6">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
          </div>
        ) : (
          <>
            <div className="whitespace-pre-wrap">{message.content}</div>
            
            {/* Botões de ação para mensagens da IA */}
            {!isUser && !isSystem && (
              <div className="flex mt-2 space-x-2 justify-end text-xs text-gray-500">
                <button 
                  onClick={handleCopy} 
                  className="hover:text-gray-700 transition-colors"
                  aria-label="Copiar mensagem"
                >
                  {isCopied ? 'Copiado!' : 'Copiar'}
                </button>
                
                {onReadAloud && (
                  <button 
                    onClick={handleReadAloud} 
                    className="hover:text-gray-700 transition-colors"
                    aria-label="Ouvir mensagem"
                  >
                    Ouvir
                  </button>
                )}
              </div>
            )}
          </>
        )}
      </div>
      
      {/* Timestamp */}
      <span className="text-xs text-gray-500 mt-1 mb-3">
        {formattedTime}
      </span>
    </div>
  );
};

export default ChatBubble; 