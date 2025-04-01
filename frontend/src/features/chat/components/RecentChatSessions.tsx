import React from 'react';
import { Link } from 'react-router-dom';
import { useChatContext } from '../contexts/ChatContext';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface RecentChatSessionsProps {
  maxSessions?: number;
  showCreateNew?: boolean;
  className?: string;
}

/**
 * Componente que exibe as conversas recentes do usuário
 */
const RecentChatSessions: React.FC<RecentChatSessionsProps> = ({
  maxSessions = 5,
  showCreateNew = true,
  className = '',
}) => {
  const { chatHistory, createNewSession, isCreatingSession, isHistoryLoading } = useChatContext();
  
  // Filtrar apenas as sessões mais recentes
  const recentSessions = [...(chatHistory || [])]
    .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    .slice(0, maxSessions);
  
  // Lidar com a criação de uma nova sessão
  const handleCreateNew = async () => {
    try {
      const { sessionId } = await createNewSession();
      // Redirecionar para a nova sessão acontecerá automaticamente
    } catch (error) {
      console.error('Erro ao criar nova sessão:', error);
    }
  };

  // Renderizar estado de carregamento
  if (isHistoryLoading) {
    return (
      <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
        <h3 className="text-lg font-medium text-gray-800 mb-3">Conversas recentes</h3>
        <div className="animate-pulse space-y-3">
          {[...Array(3)].map((_, index) => (
            <div key={index} className="h-14 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow p-4 ${className}`}>
      <h3 className="text-lg font-medium text-gray-800 mb-3">Conversas recentes</h3>
      
      {/* Botão para criar nova conversa */}
      {showCreateNew && (
        <button
          onClick={handleCreateNew}
          disabled={isCreatingSession}
          className="w-full mb-4 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md flex items-center justify-center"
        >
          {isCreatingSession ? (
            <span className="inline-block h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
          ) : (
            <svg 
              className="h-5 w-5 mr-2" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 6v6m0 0v6m0-6h6m-6 0H6" 
              />
            </svg>
          )}
          Nova conversa
        </button>
      )}
      
      {/* Lista de sessões recentes */}
      {recentSessions.length > 0 ? (
        <div className="space-y-2">
          {recentSessions.map((session) => (
            <Link
              key={session.id}
              to={`/chat/historico/${session.id}`}
              className="block p-3 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
            >
              <div className="flex justify-between items-center">
                <span className="text-gray-800 font-medium truncate">
                  {session.title || 'Conversa sem título'}
                </span>
                <span className="text-xs text-gray-500">
                  {formatDistanceToNow(new Date(session.updatedAt), { 
                    addSuffix: true,
                    locale: ptBR
                  })}
                </span>
              </div>
              {session.lastMessage && (
                <p className="text-sm text-gray-500 truncate mt-1">
                  {session.lastMessage}
                </p>
              )}
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-6 text-gray-500">
          <p>Nenhuma conversa encontrada</p>
          <p className="text-sm mt-1">Inicie uma nova conversa para começar</p>
        </div>
      )}
    </div>
  );
};

export default RecentChatSessions; 