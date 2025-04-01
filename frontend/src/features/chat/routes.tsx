import React from 'react';
import { RouteObject } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import ChatHistoryPage from './pages/ChatHistoryPage';
import { ProtectedRoute } from '../auth';

/**
 * Rotas para a feature de chat
 * Todas as rotas são protegidas e requerem autenticação
 */
const ChatRoutes: RouteObject[] = [
  {
    path: '/chat',
    element: (
      <ProtectedRoute>
        <ChatPage />
      </ProtectedRoute>
    ),
  },
  {
    path: '/chat/historico/:sessionId',
    element: (
      <ProtectedRoute>
        <ChatHistoryPage />
      </ProtectedRoute>
    ),
  },
];

export default ChatRoutes; 