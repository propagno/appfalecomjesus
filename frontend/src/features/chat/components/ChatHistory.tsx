import React, { useRef, useEffect } from 'react';
import { useChatContext } from '../contexts/ChatContext';
import ChatBubble from './ChatBubble';

interface ChatHistoryProps {
  onReadAloud?: (text: string) => void;
}

/**
 * Componente que exibe o histórico de mensagens do chat
 */
const ChatHistory: React.FC<ChatHistoryProps> = ({ onReadAloud }) => {
  const { messages, isLoading } = useChatContext();
  const endOfMessagesRef = useRef<HTMLDivElement>(null);
  
  // Rolagem automática para a última mensagem
  useEffect(() => {
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);
  
  // Se não há mensagens, exibe um placeholder
  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex flex-col h-full justify-center items-center p-4 text-center">
        <div className="mb-4 text-gray-500">
          <svg
            className="mx-auto h-12 w-12"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900">Inicie uma conversa</h3>
        <p className="mt-1 text-sm text-gray-500">
          Envie uma mensagem para começar a conversar com a IA.
        </p>
      </div>
    );
  }
  
  return (
    <div className="flex-1 p-4 overflow-y-auto">
      {messages.map((message) => (
        <ChatBubble
          key={message.id}
          message={message}
          onReadAloud={onReadAloud}
        />
      ))}
      
      {/* Elemento invisível para rolagem automática */}
      <div ref={endOfMessagesRef} />
    </div>
  );
};

export default ChatHistory; 