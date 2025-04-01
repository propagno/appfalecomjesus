import React, { useState } from 'react';
import { useGamification } from '../contexts/GamificationContext';
import { GamificationNotification as NotificationType } from '../types';
import NotificationBadge from './NotificationBadge';

// Função local para formatação de data e hora
const formatDateTime = (date: Date | string): string => {
  if (!date) return '';
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

interface GamificationNotificationsProps {
  maxNotifications?: number;
}

const GamificationNotifications: React.FC<GamificationNotificationsProps> = ({
  maxNotifications = 5,
}) => {
  const {
    notifications,
    markNotificationAsRead,
    markAllNotificationsAsRead,
    dismissNotification,
    hasNewNotifications,
    getUnreadNotificationsCount,
  } = useGamification();

  const [isOpen, setIsOpen] = useState(false);

  // Exibir apenas as notificações mais recentes
  const displayNotifications = notifications
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, maxNotifications);

  // Renderizar o ícone da notificação com base no tipo
  const renderNotificationIcon = (notification: NotificationType) => {
    switch (notification.type) {
      case 'achievement_unlocked':
        return (
          <div className="bg-amber-100 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-amber-600" viewBox="0 0 20 20" fill="currentColor">
              <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
            </svg>
          </div>
        );
      case 'level_up':
        return (
          <div className="bg-green-100 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-green-600" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
            </svg>
          </div>
        );
      case 'streak_milestone':
        return (
          <div className="bg-blue-100 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clipRule="evenodd" />
            </svg>
          </div>
        );
      case 'points_milestone':
        return (
          <div className="bg-purple-100 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-purple-600" viewBox="0 0 20 20" fill="currentColor">
              <path d="M6 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm-4 2a2 2 0 1 1-4 0 2 2 0 0 1 4 0z" />
            </svg>
          </div>
        );
      default:
        return (
          <div className="bg-gray-100 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
        );
    }
  };

  // Manipular clique na notificação
  const handleNotificationClick = (notification: NotificationType) => {
    if (!notification.is_read) {
      markNotificationAsRead(notification.id);
    }
    
    // Aqui podemos implementar navegação ou ações específicas
    // baseadas no tipo e dados da notificação
    console.log('Notificação clicada:', notification);
  };

  return (
    <div className="relative">
      {/* Botão de notificação com badge */}
      <button
        className="rounded-full p-2 hover:bg-gray-100 relative"
        onClick={() => setIsOpen(!isOpen)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        
        {/* Badge para notificações não lidas */}
        <NotificationBadge 
          count={getUnreadNotificationsCount()} 
          className="absolute top-0 right-0 transform translate-x-1/3 -translate-y-1/3"
        />
      </button>
      
      {/* Dropdown de notificações */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border overflow-hidden z-50">
          {/* Cabeçalho */}
          <div className="bg-blue-50 border-b border-blue-100 p-3 flex justify-between items-center">
            <h3 className="font-medium text-blue-900">Notificações</h3>
            {hasNewNotifications() && (
              <button
                className="text-xs text-blue-600 hover:text-blue-800"
                onClick={() => {
                  markAllNotificationsAsRead();
                  // Manter o dropdown aberto
                }}
              >
                Marcar todas como lidas
              </button>
            )}
          </div>
          
          {/* Lista de notificações */}
          {displayNotifications.length > 0 ? (
            <div className="max-h-96 overflow-y-auto divide-y divide-gray-100">
              {displayNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-3 flex gap-3 hover:bg-gray-50 cursor-pointer relative ${
                    !notification.is_read ? 'bg-blue-50' : ''
                  }`}
                  onClick={() => handleNotificationClick(notification)}
                >
                  {/* Ícone */}
                  <div className="flex-shrink-0">
                    {renderNotificationIcon(notification)}
                  </div>
                  
                  {/* Conteúdo */}
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-gray-900">
                      {notification.title}
                    </h4>
                    <p className="text-xs text-gray-600 mt-1">
                      {notification.message}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {formatDateTime(notification.created_at)}
                    </p>
                  </div>
                  
                  {/* Botão de dispensar */}
                  <button
                    className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
                    onClick={(e) => {
                      e.stopPropagation();
                      dismissNotification(notification.id);
                    }}
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 text-center text-gray-500 text-sm">
              Nenhuma notificação disponível.
            </div>
          )}
          
          {/* Rodapé */}
          <div className="border-t border-gray-100 p-2 text-center">
            <button 
              className="text-xs text-blue-600 hover:text-blue-800 font-medium"
              onClick={() => setIsOpen(false)}
            >
              Fechar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default GamificationNotifications; 