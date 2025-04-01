import React from 'react';
import { MessageSquare, X, Clock, ChevronRight } from 'lucide-react';
import { format, isAfter } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { ChatHistory } from '../types';

interface ChatSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  chatHistory: ChatHistory[];
  activeSessionId: string | null;
  onSelectSession: (sessionId: string) => void;
  isLoading?: boolean;
}

/**
 * Componente que mostra o histórico de conversas na barra lateral
 */
export const ChatSidebar: React.FC<ChatSidebarProps> = ({
  isOpen,
  onClose,
  chatHistory,
  activeSessionId,
  onSelectSession,
  isLoading = false,
}) => {
  // Formatar a data para exibição
  const formatDate = (date: Date) => {
    // Se for hoje, mostrar apenas a hora
    const today = new Date();
    if (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    ) {
      return format(date, "'Hoje,' HH:mm", { locale: ptBR });
    }
    // Se for ontem
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    if (
      date.getDate() === yesterday.getDate() &&
      date.getMonth() === yesterday.getMonth() &&
      date.getFullYear() === yesterday.getFullYear()
    ) {
      return format(date, "'Ontem,' HH:mm", { locale: ptBR });
    }
    // Se for nos últimos 7 dias, mostrar o dia da semana
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    if (isAfter(date, sevenDaysAgo)) {
      return format(date, "EEEE', ' HH:mm", { locale: ptBR });
    }
    // Caso contrário, mostrar a data completa
    return format(date, "dd 'de' MMMM', ' HH:mm", { locale: ptBR });
  };

  // Obter a prévia da última mensagem de uma sessão
  const getLastMessagePreview = (session: ChatHistory) => {
    if (!session.messages || session.messages.length === 0) {
      return 'Nenhuma mensagem';
    }
    
    const lastMessage = session.messages[session.messages.length - 1];
    const preview = lastMessage.content.slice(0, 30);
    return preview.length < lastMessage.content.length 
      ? `${preview}...` 
      : preview;
  };

  return (
    <div
      className={`fixed inset-y-0 left-0 z-20 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:w-72 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="flex flex-col h-full">
        {/* Cabeçalho do sidebar */}
        <div className="flex justify-between items-center p-4 border-b border-gray-200">
          <h2 className="font-semibold text-lg">Histórico</h2>
          <button
            onClick={onClose}
            className="p-1 rounded-full hover:bg-gray-200 lg:hidden"
            title="Fechar"
          >
            <X size={20} />
          </button>
        </div>

        {/* Conteúdo do histórico */}
        <div className="flex-1 overflow-y-auto p-2">
          {isLoading ? (
            // Estado de carregamento
            <div className="flex flex-col items-center justify-center h-32 text-gray-500">
              <Clock className="animate-spin mb-2" />
              <p>Carregando histórico...</p>
            </div>
          ) : chatHistory.length === 0 ? (
            // Estado vazio
            <div className="flex flex-col items-center justify-center h-32 text-gray-500 p-4">
              <MessageSquare className="mb-2" />
              <p className="text-center">Nenhuma conversa iniciada.</p>
              <p className="text-center text-sm mt-1">
                Suas conversas aparecerão aqui.
              </p>
            </div>
          ) : (
            // Lista de conversas
            <div className="space-y-1">
              {chatHistory.map((session) => (
                <button
                  key={session.id}
                  onClick={() => onSelectSession(session.id)}
                  className={`w-full text-left p-3 rounded-lg transition-colors flex justify-between items-center ${
                    activeSessionId === session.id
                      ? 'bg-blue-50 text-blue-700'
                      : 'hover:bg-gray-100'
                  }`}
                >
                  <div className="flex-1 overflow-hidden">
                    <div className="font-medium truncate">{session.title || 'Nova conversa'}</div>
                    <div className="text-xs text-gray-500 truncate">
                      {getLastMessagePreview(session)}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {formatDate(new Date(session.updatedAt))}
                    </div>
                  </div>
                  <ChevronRight
                    size={16}
                    className={`text-gray-400 ${
                      activeSessionId === session.id ? 'opacity-100' : 'opacity-0'
                    }`}
                  />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Rodapé com info */}
        <div className="p-3 text-xs text-center text-gray-500 border-t border-gray-200">
          © 2023 FaleComJesus - Conversas em Cristo
        </div>
      </div>
    </div>
  );
};

export default ChatSidebar; 