import React, { createContext, useContext, ReactNode } from 'react';
import { 
  StudyContextType,
  OnboardingPreferences,
  PlanFilters
} from '../types';
import useToast from '../../../shared/hooks/useToast';
import useStudyQuery from '../hooks/useStudyQuery';

// Contexto de Estudo
const StudyContext = createContext<StudyContextType | null>(null);

// Interface de props do provedor
interface StudyProviderProps {
  children: ReactNode;
}

// Interface temporária para onboarding
interface OnboardingFormData {
  objectives: string[];
  bible_experience_level: string;
  content_preferences: string[];
  preferred_time: string;
}

// Estender a interface do StudyContextType para incluir o método adicional
interface ExtendedStudyContextType extends StudyContextType {
  createPersonalizedPlan: (data: OnboardingFormData) => Promise<any>;
  // Propriedades do StudyPlanDetailPage
  fetchPlanDetails: (planId: string) => Promise<any>;
  // Propriedades do StudyPlansPage
  totalPlans: number;
  filters: PlanFilters;
  handleFilterChange: (newFilters: Partial<PlanFilters>) => void;
  handlePageChange: (page: number) => void;
  fetchPlans: () => Promise<void>;
  // Propriedades adicionais necessárias
  submitOnboarding: (preferences: OnboardingPreferences) => Promise<void>;
  confirmPersonalizedPlan: () => void;
  isMutating: boolean;
}

/**
 * Provedor do contexto de estudo
 * Encapsula a lógica de React Query e oferece uma API limpa 
 * para componentes usarem
 */
export const StudyProvider: React.FC<StudyProviderProps> = ({ children }) => {
  const toast = useToast();
  
  // Obter dados e funcionalidades via React Query
  const studyQuery = useStudyQuery();

  // Adaptador para manter compatibilidade com o código existente
  const createPersonalizedPlan = async (data: OnboardingFormData) => {
    // Convertendo OnboardingFormData para formato adequado se necessário
    return studyQuery.createPersonalizedPlan(data);
  };
  
  // Funções adicionais necessárias para a ExtendedStudyContextType
  const fetchPlanDetails = async (planId: string) => {
    return studyQuery.fetchPlanDetails ? studyQuery.fetchPlanDetails(planId) : null;
  };

  const fetchPlans = async () => {
    return studyQuery.fetchPlans ? studyQuery.fetchPlans() : Promise.resolve();
  };

  // Valor do contexto com tipo extendido
  const contextValue: ExtendedStudyContextType = {
    ...studyQuery as unknown as StudyContextType,
    createPersonalizedPlan,
    fetchPlanDetails,
    totalPlans: (studyQuery as any).totalPlans || 0,
    filters: (studyQuery as any).filters || {},
    handleFilterChange: (studyQuery as any).handleFilterChange || (() => {}),
    handlePageChange: (studyQuery as any).handlePageChange || (() => {}),
    fetchPlans,
    submitOnboarding: async (preferences: OnboardingPreferences) => {
      // Implementation of submitOnboarding
    },
    confirmPersonalizedPlan: () => {
      // Implementation of confirmPersonalizedPlan
    },
    isMutating: false
  };
  
  // Fornecer contexto para toda a árvore de componentes
  return (
    <StudyContext.Provider value={contextValue}>
      {children}
    </StudyContext.Provider>
  );
};

/**
 * Hook para consumir o contexto de estudo
 * @returns Contexto de estudo com todos os dados e funções
 */
export const useStudyContext = (): ExtendedStudyContextType => {
  const context = useContext(StudyContext);
  
  if (!context) {
    throw new Error('useStudyContext deve ser usado dentro de um StudyProvider');
  }
  
  return context as ExtendedStudyContextType;
};

export default StudyContext; 