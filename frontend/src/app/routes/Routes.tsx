import React, { lazy, Suspense } from 'react';
import { Navigate, Route, Routes as RouterRoutes, Outlet } from 'react-router-dom';
import LoadingPage from '../../shared/components/LoadingPage';
import ProtectedRoute from '../../features/auth/components/ProtectedRoute';
import LoginPage from '../../features/auth/pages/LoginPage';
import RegisterPage from '../../features/auth/pages/RegisterPage';
import ForgotPasswordPage from '../../features/auth/pages/ForgotPasswordPage';
import ResetPasswordPage from '../../features/auth/pages/ResetPasswordPage';
import HomePage from '../../pages/Home';
import MainLayout from '../../layouts/MainLayout';
import BibleExplorerPage from '../../features/bible/pages/BibleExplorerPage';
import ChatPage from '../../features/chat/pages/ChatPage';
import { StudyPlansPage, OnboardingPage as StudyOnboardingPage } from '../../features/study';
import SettingsPage from '../../pages/Settings';
import NotFoundPage from '../../pages/NotFound';
import { GamificationPage } from '../../features/gamification';
import MonetizationPage from '../../features/monetization/pages/MonetizationPage';

/**
 * Definição das rotas do aplicativo, incluindo rotas públicas e protegidas
 */
const Routes: React.FC = () => {
  return (
    <Suspense fallback={<LoadingPage />}>
      <RouterRoutes>
        {/* Rotas Públicas */}
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        
        {/* Rota de Onboarding - Protegida, mas separada do layout principal */}
        <Route path="/onboarding" element={
          <ProtectedRoute>
            <StudyOnboardingPage />
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
          <Route path="study/onboarding" element={<StudyOnboardingPage />} />
          
          {/* Bíblia */}
          <Route path="bible" element={
            <Suspense fallback={<LoadingPage />}>
              <BibleExplorerPage />
            </Suspense>
          } />
          <Route path="bible/:bookId" element={
            <Suspense fallback={<LoadingPage />}>
              <BibleExplorerPage />
            </Suspense>
          } />
          <Route path="bible/:bookId/:chapterId" element={
            <Suspense fallback={<LoadingPage />}>
              <BibleExplorerPage />
            </Suspense>
          } />
          
          {/* Chat com IA */}
          <Route path="chat" element={
            <Suspense fallback={<LoadingPage />}>
              <ChatPage />
            </Suspense>
          } />
          <Route path="chat/:sessionId" element={
            <Suspense fallback={<LoadingPage />}>
              <ChatPage />
            </Suspense>
          } />
          
          {/* Configurações */}
          <Route path="settings" element={
            <Suspense fallback={<LoadingPage />}>
              <SettingsPage />
            </Suspense>
          } />

          <Route path="gamification" element={<GamificationPage />} />
          
          {/* Monetização */}
          <Route path="monetization" element={<MonetizationPage />} />
        </Route>
        
        {/* Rota de Erro - 404 */}
        <Route path="*" element={
          <Suspense fallback={<LoadingPage />}>
            <NotFoundPage />
          </Suspense>
        } />
      </RouterRoutes>
    </Suspense>
  );
};

export default Routes; 