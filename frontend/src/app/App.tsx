import React, { useEffect, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import ErrorBoundary from '../shared/components/ErrorBoundary';
import { errorHandler, AppError } from '../shared/utils/errorHandler';
import LoadingPage from '../shared/components/LoadingPage';

// Pages
import LoginPage from '../features/auth/pages/LoginPage';
import RegisterPage from '../features/auth/pages/RegisterPage';
import ForgotPasswordPage from '../features/auth/pages/ForgotPasswordPage';
import OnboardingPage from '../features/study/pages/OnboardingPage';
import HomePage from '../pages/Home';
import MainLayout from '../layouts/MainLayout';
import BibleExplorerPage from '../features/bible/pages/BibleExplorerPage';
import ChatPage from '../features/chat/pages/ChatPage';
import { StudyPlansPage } from '../features/study';
import SettingsPage from '../pages/Settings';
import NotFoundPage from '../pages/NotFound';
import { GamificationPage } from '../features/gamification';
import MonetizationPage from '../features/monetization/pages/MonetizationPage';

// Auth component
import ProtectedRoute from '../features/auth/components/ProtectedRoute';

/**
 * Componente raiz da aplicação
 * Configura rotas e tratamento de erros
 */
const App: React.FC = () => {
  // Configurar handler global para erros não capturados
  useEffect(() => {
    const handleUnhandledError = (error: AppError) => {
      console.error('Erro não capturado:', error);
    };
    
    errorHandler.registerErrorCallback(handleUnhandledError);
    
    return () => {
      errorHandler.unregisterErrorCallback(handleUnhandledError);
    };
  }, []);

  return (
    <ErrorBoundary>
      {/* Componente para exibir notificações toast */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 5000,
          style: {
            borderRadius: '8px',
            background: '#333',
            color: '#fff',
          },
        }}
      />
      
      {/* Definição das rotas */}
      <Suspense fallback={<LoadingPage />}>
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          
          {/* Rota de Onboarding - Protegida, mas separada do layout principal */}
          <Route path="/onboarding" element={
            <ProtectedRoute>
              <OnboardingPage />
            </ProtectedRoute>
          } />
          
          {/* Rotas Protegidas */}
          <Route path="/" element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }>
            <Route path="home" element={<HomePage />} />
            <Route path="plans" element={<StudyPlansPage />} />
            
            {/* Bíblia */}
            <Route path="bible" element={<BibleExplorerPage />} />
            <Route path="bible/:bookId" element={<BibleExplorerPage />} />
            <Route path="bible/:bookId/:chapterId" element={<BibleExplorerPage />} />
            
            {/* Chat com IA */}
            <Route path="chat" element={<ChatPage />} />
            <Route path="chat/:sessionId" element={<ChatPage />} />
            
            {/* Configurações */}
            <Route path="settings" element={<SettingsPage />} />
            <Route path="gamification" element={<GamificationPage />} />
            <Route path="monetization" element={<MonetizationPage />} />
          </Route>
          
          {/* Rota de Erro - 404 */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </ErrorBoundary>
  );
};

export default App;
 