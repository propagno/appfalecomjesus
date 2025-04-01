import React from 'react';
import { Book, MoreVertical, Plus, XCircle } from 'lucide-react';
import { ChatHistory } from '../types';

interface ChatHeaderProps {
  activeSession: ChatHistory | null;
  remainingMessages?: number | null;
  isPremium?: boolean;
  onCreateNewSession: () => void;
  onDeleteSession: (sessionId: string) => void;
  onToggleSidebar?: () => void;
}

/**
 * Componente para o cabeçalho da tela de chat
 * Exibe o título da sessão, mensagens restantes e ações
 */
export const ChatHeader: React.FC<ChatHeaderProps> = ({
  activeSession,
  remainingMessages,
  isPremium = false,
  onCreateNewSession,
  onDeleteSession,
  onToggleSidebar,
}) => {
  const [showMenu, setShowMenu] = React.useState(false);

  // Abrir/fechar menu de ações
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  // Deletar sessão atual e confirmar
  const handleDeleteSession = () => {
    if (activeSession && window.confirm('Tem certeza que deseja excluir esta conversa?')) {
      onDeleteSession(activeSession.id);
      setShowMenu(false);
    }
  };

  return (
    <div className="bg-white border-b border-gray-200 p-3 flex items-center justify-between">
      <div className="flex items-center gap-2">
        {/* Botão para mostrar/ocultar sidebar em telas pequenas */}
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-full hover:bg-gray-200 lg:hidden"
            title="Ver histórico de conversas"
          >
            <Book size={20} />
          </button>
        )}
        
        {/* Título da sessão */}
        <h2 className="font-medium truncate max-w-[200px] md:max-w-[300px]">
          {activeSession?.title || 'Nova conversa'}
        </h2>
      </div>

      <div className="flex items-center gap-3">
        {/* Contador de mensagens restantes (apenas no plano free) */}
        {!isPremium && remainingMessages !== null && remainingMessages !== undefined && (
          <div className="text-sm">
            <span className="font-semibold text-blue-600">{remainingMessages}</span>
            <span className="text-gray-500 ml-1">
              {remainingMessages === 1 ? 'mensagem restante' : 'mensagens restantes'}
            </span>
          </div>
        )}

        {/* Botão nova conversa */}
        <button
          onClick={onCreateNewSession}
          className="p-2 rounded-full hover:bg-gray-200"
          title="Nova conversa"
        >
          <Plus size={20} />
        </button>

        {/* Menu de ações */}
        <div className="relative">
          <button
            onClick={toggleMenu}
            className="p-2 rounded-full hover:bg-gray-200"
            title="Mais opções"
          >
            <MoreVertical size={20} />
          </button>

          {/* Dropdown menu */}
          {showMenu && (
            <div className="absolute right-0 top-10 bg-white shadow-md rounded-md border border-gray-200 w-48 z-10">
              <div className="py-1">
                {/* Opção para deletar conversa */}
                {activeSession && (
                  <button
                    onClick={handleDeleteSession}
                    className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600 flex items-center gap-2"
                  >
                    <XCircle size={16} />
                    <span>Excluir conversa</span>
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatHeader; 