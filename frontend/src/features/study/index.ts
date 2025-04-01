// Componentes
export { default as PlanCard } from './components/PlanCard';
export { default as OnboardingForm } from './components/OnboardingForm';
export { default as ReflectionForm } from './components/ReflectionForm';

// Páginas
export { default as OnboardingPage } from './pages/OnboardingPage';
export { default as StudyPlansPage } from './pages/StudyPlansPage';

// Contexto e hooks
export { StudyProvider, useStudyContext } from './contexts/StudyContext';
export { default as useStudy } from './hooks/useStudy';

// Serviços de API
export { default as studyService } from './api/studyService';
export type { StudyContent, StudyPlansResponse } from './api/studyService';

// Rotas
export { default as StudyRoutes } from './routes';

// Tipos
export type {
  StudyPlan,
  StudySection,
  UserStudyProgress,
  Reflection,
  Certificate,
  OnboardingPreferences,
  PlanSuggestion,
  PlanFilters as StudyFilters
} from './types'; 