import React, { useRef, useEffect } from 'react';
import { Message } from '../types';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Volume2 } from 'lucide-react';

interface MessageListProps {
  messages: Message[];
  className?: string;
}

/**
 * Componente para exibir a lista de mensagens do chat
 * Rolagem automática para a última mensagem
 */
export const MessageList: React.FC<MessageListProps> = ({ 
  messages, 
  className = '' 
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Rolar para a última mensagem automaticamente quando novas mensagens chegarem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages.length]);

  // Função para formatar a data da mensagem
  const formatMessageTime = (date: string) => {
    return format(new Date(date), 'HH:mm', { locale: ptBR });
  };

  // Função para ler mensagem em voz alta
  const readMessageAloud = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-BR';
      window.speechSynthesis.speak(utterance);
    } else {
      console.log('API de síntese de voz não suportada pelo navegador');
    }
  };

  return (
    <div className={`flex flex-col space-y-4 p-4 ${className}`}>
      {messages.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>Envie uma mensagem para começar a conversa.</p>
          <p className="mt-2 text-sm">
            Faça perguntas sobre a Bíblia e sobre dúvidas espirituais.
          </p>
        </div>
      ) : (
        messages.map((message, index) => (
          <div 
            key={message.id || index} 
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`relative max-w-3/4 px-4 py-2 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none' 
                  : 'bg-gray-200 text-gray-800 rounded-tl-none'
              }`}
            >
              <div className="text-sm mb-1">
                {message.content}
              </div>
              
              <div className="flex items-center justify-between mt-1">
                <span className="text-xs opacity-70">
                  {formatMessageTime(message.timestamp)}
                </span>
                
                {message.type === 'assistant' && (
                  <button 
                    className="ml-2 p-1 rounded-full hover:bg-gray-300 transition-colors"
                    onClick={() => readMessageAloud(message.content)}
                    title="Ouvir mensagem"
                  >
                    <Volume2 className="h-3 w-3" />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))
      )}
      
      {/* Referência para rolagem automática */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList; 