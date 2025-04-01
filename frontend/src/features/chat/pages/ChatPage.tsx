import React, { useState, useRef, useEffect } from 'react';
import { useChatContext } from '../providers/ChatProvider';
import { MessageType } from '../constants';

/**
 * Página de demonstração do chat usando a nova implementação com React Query
 * Implementação do item 10.4.5 - Componente demo
 */
const ChatPage: React.FC = () => {
  const {
    activeSession,
    sessions,
    isLoading,
    isStreaming,
    streamingText,
    messageLimit,
    error,
    sendMessage,
    createSession,
    selectSession,
    updateSessionTitle,
    deleteSession,
    clearHistory,
    registerAdReward,
  } = useChatContext();

  const [inputMessage, setInputMessage] = useState('');
  const [sessionTitle, setSessionTitle] = useState('');
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Rolar para o final quando as mensagens mudarem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeSession?.messages, streamingText]);

  // Lidar com o envio de mensagem
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;
    
    try {
      await sendMessage(inputMessage);
      setInputMessage('');
    } catch (err) {
      console.error('Erro ao enviar mensagem:', err);
    }
  };

  // Criar uma nova sessão
  const handleCreateSession = async () => {
    try {
      await createSession();
    } catch (err) {
      console.error('Erro ao criar sessão:', err);
    }
  };

  // Atualizar o título da sessão
  const handleUpdateTitle = async () => {
    if (!activeSession || !sessionTitle.trim()) return;
    
    try {
      await updateSessionTitle(activeSession.id, sessionTitle);
      setIsEditingTitle(false);
    } catch (err) {
      console.error('Erro ao atualizar título:', err);
    }
  };

  // Iniciar edição de título
  const startEditingTitle = () => {
    if (activeSession) {
      setSessionTitle(activeSession.title || 'Nova Conversa');
      setIsEditingTitle(true);
    }
  };

  // Registrar recompensa por anúncio
  const handleWatchAd = async () => {
    try {
      const result = await registerAdReward();
      if (result.success) {
        alert(`Você ganhou ${result.reward?.value} mensagens adicionais!`);
      }
    } catch (err) {
      console.error('Erro ao registrar recompensa:', err);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar com histórico de sessões */}
      <div className="w-64 bg-white border-r p-4">
        <h2 className="text-lg font-semibold mb-4">Conversas</h2>
        
        <button 
          onClick={handleCreateSession}
          className="w-full mb-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Nova Conversa
        </button>
        
        <div className="space-y-2">
          {sessions.map(session => (
            <div 
              key={session.id} 
              className={`p-2 rounded cursor-pointer flex justify-between items-center ${
                activeSession?.id === session.id ? 'bg-blue-100' : 'hover:bg-gray-100'
              }`}
              onClick={() => selectSession(session.id)}
            >
              <span className="truncate">{session.title || 'Nova Conversa'}</span>
              <button 
                onClick={(e) => { 
                  e.stopPropagation(); 
                  deleteSession(session.id); 
                }}
                className="text-red-500 hover:text-red-700"
              >
                ×
              </button>
            </div>
          ))}
        </div>
        
        {sessions.length > 0 && (
          <button 
            onClick={() => clearHistory()}
            className="mt-4 text-sm text-red-500 hover:text-red-700"
          >
            Limpar Histórico
          </button>
        )}
      </div>
      
      {/* Área principal de chat */}
      <div className="flex-1 flex flex-col">
        {/* Cabeçalho */}
        <div className="bg-white p-4 shadow">
          {activeSession ? (
            isEditingTitle ? (
              <div className="flex">
                <input
                  type="text"
                  value={sessionTitle}
                  onChange={(e) => setSessionTitle(e.target.value)}
                  className="flex-1 border rounded px-2 py-1"
                />
                <button 
                  onClick={handleUpdateTitle}
                  className="ml-2 px-3 bg-blue-600 text-white rounded"
                >
                  Salvar
                </button>
              </div>
            ) : (
              <div className="flex justify-between items-center">
                <h1 className="text-xl font-semibold" onClick={startEditingTitle}>
                  {activeSession.title || 'Nova Conversa'}
                </h1>
                <div>
                  {messageLimit && !messageLimit.isPremium && (
                    <div className="text-sm text-gray-600">
                      Mensagens restantes: {messageLimit.remaining}/{messageLimit.limit}
                    </div>
                  )}
                </div>
              </div>
            )
          ) : (
            <h1 className="text-xl font-semibold">
              Selecione ou inicie uma conversa
            </h1>
          )}
        </div>
        
        {/* Mensagens */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {activeSession?.messages.map(message => (
            <div 
              key={message.id}
              className={`p-3 rounded max-w-3xl ${
                message.type === MessageType.USER 
                  ? 'bg-blue-100 ml-auto' 
                  : 'bg-white shadow'
              }`}
            >
              {message.content}
            </div>
          ))}
          
          {/* Mensagem em streaming */}
          {isStreaming && (
            <div className="p-3 rounded max-w-3xl bg-white shadow">
              {streamingText || 'Pensando...'}
            </div>
          )}
          
          {/* Elemento para rolar para o fim */}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Área de entrada */}
        <div className="bg-white p-4 border-t">
          {messageLimit && messageLimit.remaining === 0 && !messageLimit.isPremium && (
            <div className="mb-4 p-3 bg-yellow-100 rounded text-center">
              <p>Você atingiu o limite de mensagens para hoje.</p>
              <button 
                onClick={handleWatchAd}
                className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Assista um anúncio para ganhar mais mensagens
              </button>
            </div>
          )}
          
          <form onSubmit={handleSendMessage} className="flex">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              disabled={isLoading || (messageLimit?.remaining === 0 && !messageLimit.isPremium)}
              placeholder="Digite sua mensagem..."
              className="flex-1 border rounded-l px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim() || (messageLimit?.remaining === 0 && !messageLimit.isPremium)}
              className="bg-blue-600 text-white px-6 py-2 rounded-r hover:bg-blue-700 disabled:bg-gray-400"
            >
              Enviar
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatPage; 