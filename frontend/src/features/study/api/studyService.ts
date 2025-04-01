import { API_URLS } from '../../../shared/constants/config';
import { createApiClient } from '../../../shared/services/api';
import {
  StudyPlan,
  StudySection,
  UserStudyProgress,
  Reflection,
  Certificate,
  PlanFilters as StudyFilters,
  OnboardingPreferences,
  PlanSuggestion
} from '../types';

// Interface para resposta de listagem de planos
export interface StudyPlansResponse {
  plans: StudyPlan[];
  total: number;
  page: number;
  per_page: number;
}

// Interface para conteúdo de uma seção de estudo
export interface StudyContent {
  id: string;
  section_id: string;
  content_type: 'text' | 'audio' | 'verse' | 'reflection';
  content: string;
  position: number;
}

// Criar cliente específico para o microsserviço de estudos
const studyApi = createApiClient({ baseURL: API_URLS.study });

/**
 * Serviço para interação com o microsserviço MS-Study
 */
const studyService = {
  /**
   * Busca todos os planos de estudo disponíveis
   */
  getStudyPlans: async (filters?: StudyFilters): Promise<StudyPlansResponse> => {
    const params = new URLSearchParams();
    
    if (filters) {
      if (filters.category) params.append('category', filters.category);
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.search) params.append('search', filters.search);
      if (filters.page) params.append('page', filters.page.toString());
      if (filters.per_page) params.append('per_page', filters.per_page.toString());
    }
    
    const response = await studyApi.get<StudyPlansResponse>(`/plans?${params.toString()}`);
    return response.data;
  },

  /**
   * Busca os detalhes de um plano de estudo específico
   */
  getStudyPlanById: async (planId: string): Promise<StudyPlan> => {
    const response = await studyApi.get<StudyPlan>(`/plans/${planId}`);
    return response.data;
  },

  /**
   * Busca as seções de um plano de estudo
   */
  getStudySections: async (planId: string): Promise<StudySection[]> => {
    const response = await studyApi.get<{ sections: StudySection[] }>(`/plans/${planId}/sections`);
    return response.data.sections;
  },

  /**
   * Busca o conteúdo de uma seção específica
   */
  getSectionContent: async (sectionId: string): Promise<StudyContent[]> => {
    const response = await studyApi.get<{ content: StudyContent[] }>(`/sections/${sectionId}/content`);
    return response.data.content;
  },

  /**
   * Busca o progresso do usuário em todos os planos
   */
  getUserProgress: async (): Promise<UserStudyProgress[]> => {
    const response = await studyApi.get<{ progress: UserStudyProgress[] }>(`/progress`);
    return response.data.progress;
  },

  /**
   * Busca o progresso do usuário em um plano específico
   */
  getUserPlanProgress: async (planId: string): Promise<UserStudyProgress> => {
    const response = await studyApi.get<UserStudyProgress>(`/progress/${planId}`);
    return response.data;
  },

  /**
   * Atualiza o progresso do usuário em um plano
   */
  updateProgress: async (data: { 
    planId: string, 
    sectionId: string, 
    completionPercentage: number 
  }): Promise<UserStudyProgress> => {
    const { planId, sectionId, completionPercentage } = data;
    const response = await studyApi.post<UserStudyProgress>(`/progress/update`, {
      plan_id: planId,
      section_id: sectionId,
      completion_percentage: completionPercentage
    });
    return response.data;
  },

  /**
   * Inicia um novo plano de estudo para o usuário
   */
  startStudyPlan: async (planId: string): Promise<UserStudyProgress> => {
    const response = await studyApi.post<UserStudyProgress>(`/plans/${planId}/start`);
    return response.data;
  },

  /**
   * Salva uma reflexão do usuário sobre uma seção de estudo
   */
  saveReflection: async (data: { 
    sectionId: string, 
    reflectionText: string 
  }): Promise<Reflection> => {
    const { sectionId, reflectionText } = data;
    const response = await studyApi.post<Reflection>(`/reflections`, {
      section_id: sectionId,
      reflection_text: reflectionText
    });
    return response.data;
  },

  /**
   * Busca as reflexões do usuário
   */
  getUserReflections: async (): Promise<Reflection[]> => {
    const response = await studyApi.get<{ reflections: Reflection[] }>(`/reflections`);
    return response.data.reflections;
  },

  /**
   * Busca os certificados do usuário
   */
  getUserCertificates: async (): Promise<Certificate[]> => {
    const response = await studyApi.get<{ certificates: Certificate[] }>(`/certificates`);
    return response.data.certificates;
  },

  /**
   * Gera um certificado para um plano concluído
   */
  generateCertificate: async (planId: string): Promise<Certificate> => {
    const response = await studyApi.post<Certificate>(`/certificates/generate`, {
      plan_id: planId
    });
    return response.data;
  },

  /**
   * Envia as preferências do onboarding para gerar um plano personalizado
   */
  submitOnboardingPreferences: async (
    preferences: OnboardingPreferences
  ): Promise<PlanSuggestion> => {
    const response = await studyApi.post<{ suggestion: PlanSuggestion }>(`/init-plan`, preferences);
    return response.data.suggestion;
  },

  /**
   * Cria um plano personalizado com base na sugestão da IA
   */
  createPersonalizedPlan: async (
    suggestion: PlanSuggestion
  ): Promise<StudyPlan> => {
    const response = await studyApi.post<{ plan: StudyPlan }>(`/plans/create-personalized`, {
      suggestion
    });
    return response.data.plan;
  },

  /**
   * Busca o estudo atual recomendado para o usuário
   */
  getCurrentStudy: async (): Promise<UserStudyProgress | null> => {
    const response = await studyApi.get<{ progress: UserStudyProgress | null }>(`/current`);
    return response.data.progress;
  },

  /**
   * Marca um plano como completo
   */
  completePlan: async (planId: string): Promise<UserStudyProgress> => {
    const response = await studyApi.post<UserStudyProgress>(`/plans/${planId}/complete`);
    return response.data;
  }
};

export default studyService; 