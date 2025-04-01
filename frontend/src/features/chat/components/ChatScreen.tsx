import React, { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import ChatHistory from './ChatHistory';
import ChatForm from './ChatForm';
import AdRewardPrompt from './AdRewardPrompt';
import { useChatContext } from '../contexts/ChatContext';

interface ChatScreenProps {
  onUpgradeClick?: () => void;
}

/**
 * Tela principal do chat que combina histórico, formulário e prompts
 */
const ChatScreen: React.FC<ChatScreenProps> = ({ onUpgradeClick }) => {
  const { messageLimitInfo, activeSessionId, messages, clearHistory, isLoading } = useChatContext();
  const [isSpeaking, setIsSpeaking] = useState(false);
  
  // Função para ler texto em voz alta usando Web Speech API
  const handleReadAloud = useCallback((text: string) => {
    if (!text || isSpeaking) return;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    utterance.rate = 1.0;
    
    // Eventos para controlar o estado de leitura
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    
    // Cancelar qualquer leitura anterior
    window.speechSynthesis.cancel();
    
    // Iniciar leitura
    window.speechSynthesis.speak(utterance);
  }, [isSpeaking]);
  
  // Função para parar a leitura em voz alta
  const handleStopReading = useCallback(() => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  }, []);
  
  // Determinar se deve mostrar o aviso de limite atingido
  const showLimitWarning = messageLimitInfo && !messageLimitInfo.isPremium && messageLimitInfo.remaining === 0;
  
  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Cabeçalho */}
      <div className="bg-white border-b border-gray-200 p-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Chat com IA</h1>
          <p className="text-sm text-gray-500">
            {activeSessionId ? 'Conversa ativa' : 'Nova conversa'}
          </p>
        </div>
        
        <div className="flex space-x-2">
          {/* Botão para parar leitura */}
          {isSpeaking && (
            <button
              onClick={handleStopReading}
              className="text-red-600 hover:text-red-800 p-2 rounded-full hover:bg-red-50"
              aria-label="Parar leitura"
            >
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
                  d="M5 5h14v14H5z"
                />
              </svg>
            </button>
          )}
          
          {/* Botão para limpar histórico */}
          {messages.length > 0 && (
            <button
              onClick={() => {
                if (window.confirm('Deseja realmente limpar o histórico desta conversa?')) {
                  clearHistory();
                }
              }}
              className="text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-100"
              aria-label="Limpar conversa"
            >
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
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          )}
        </div>
      </div>
      
      {/* Conteúdo principal */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Histórico de chat */}
        <ChatHistory onReadAloud={handleReadAloud} />
        
        {/* Prompt para assistir anúncio (quando limite atingido) */}
        {showLimitWarning && (
          <div className="px-4">
            <AdRewardPrompt onUpgradeClick={onUpgradeClick} />
          </div>
        )}
        
        {/* Rodapé com informações sobre uso (para plano Free) */}
        {messageLimitInfo && !messageLimitInfo.isPremium && messageLimitInfo.remaining > 0 && (
          <div className="bg-gray-50 px-4 py-2 text-xs text-gray-500 border-t border-gray-200">
            <span>
              {messageLimitInfo.remaining} de {messageLimitInfo.limit} mensagens restantes hoje.
              {' '}
              <Link 
                to="/monetizacao" 
                className="text-blue-600 hover:underline"
              >
                Faça upgrade para Premium.
              </Link>
            </span>
          </div>
        )}
        
        {/* Formulário de envio de mensagem */}
        <ChatForm />
      </div>
    </div>
  );
};

export default ChatScreen; 