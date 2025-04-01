import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ChatScreen from '../components/ChatScreen';
import { useChatContext } from '../contexts/ChatContext';

/**
 * Página que exibe um histórico de chat específico pelo ID
 */
const ChatHistoryPage: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const { activeSessionId, switchSession } = useChatContext();

  // Redirecionar para upgrade
  const handleUpgradeClick = () => {
    navigate('/monetizacao');
  };

  // Carregar o histórico específico quando o componente montar
  useEffect(() => {
    if (sessionId && sessionId !== activeSessionId) {
      switchSession(sessionId);
    }
  }, [sessionId, switchSession, activeSessionId]);

  return (
    <div className="flex flex-col h-screen">
      <main className="flex-1 overflow-hidden">
        <div className="container mx-auto px-4 h-full max-w-4xl">
          <div className="bg-white shadow-sm rounded-lg h-full overflow-hidden">
            <ChatScreen onUpgradeClick={handleUpgradeClick} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChatHistoryPage; 