import React from 'react';
import { RouteObject } from 'react-router-dom';
import { ProtectedRoute } from '../auth';
import OnboardingPage from './pages/OnboardingPage';
import StudyPlansPage from './pages/StudyPlansPage';
import StudyPlanDetailPage from './pages/StudyPlanDetailPage';
import { StudyProvider } from './contexts/StudyContext';

/**
 * Wrapper que fornece o contexto de estudo para as rotas
 */
const StudyProviderWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <StudyProvider>
    {children}
  </StudyProvider>
);

/**
 * Configuração de rotas para a feature de estudo
 */
const StudyRoutes: RouteObject[] = [
  {
    path: '/estudo',
    element: (
      <ProtectedRoute>
        <StudyProviderWrapper>
          <StudyPlansPage />
        </StudyProviderWrapper>
      </ProtectedRoute>
    ),
  },
  {
    path: '/estudo/planos',
    element: (
      <ProtectedRoute>
        <StudyProviderWrapper>
          <StudyPlansPage />
        </StudyProviderWrapper>
      </ProtectedRoute>
    ),
  },
  {
    path: '/estudo/planos/:planId',
    element: (
      <ProtectedRoute>
        <StudyProviderWrapper>
          <StudyPlanDetailPage />
        </StudyProviderWrapper>
      </ProtectedRoute>
    ),
  },
  {
    path: '/estudo/onboarding',
    element: (
      <ProtectedRoute>
        <StudyProviderWrapper>
          <OnboardingPage />
        </StudyProviderWrapper>
      </ProtectedRoute>
    ),
  },
];

export default StudyRoutes; 