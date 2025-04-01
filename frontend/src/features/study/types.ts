/**
 * Tipos utilizados no módulo de estudo
 */

// Tipo de plano de estudo
export interface StudyPlan {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: string;
  duration_days: number;
  image_url?: string;
  created_at: string;
}

// Seção do plano de estudo
export interface StudySection {
  id: string;
  study_plan_id: string;
  title: string;
  position: number;
  duration_minutes: number;
}

// Conteúdo de uma seção
export interface SectionContent {
  id: string;
  section_id: string;
  content_type: string;
  content: string;
  position: number;
}

// Progresso do usuário em um plano
export interface UserStudyProgress {
  id: string;
  user_id: string;
  study_plan_id: string;
  current_section_id: string;
  completion_percentage: number;
  started_at: string;
  completed_at?: string;
}

// Reflexão pessoal
export interface Reflection {
  id: string;
  user_id: string;
  study_section_id: string;
  reflection_text: string;
  created_at: string;
}

// Certificado de conclusão
export interface Certificate {
  id: string;
  user_id: string;
  study_plan_id: string;
  completion_date: string;
  certificate_code: string;
  download_count: number;
}

// Filtros para busca de planos
export interface PlanFilters {
  search?: string;
  category?: string;
  difficulty?: string;
  page: number;
  per_page: number;
}

// Preferências do onboarding
export interface OnboardingPreferences {
  objectives: string[];
  bible_experience_level: string;
  content_preferences: string[];
  preferred_time: string;
}

// Resposta da criação de plano personalizado
export interface CreatePersonalizedPlanResponse {
  plan_id: string;
  message: string;
}

// Sugestão de plano gerada pela IA
export interface PlanSuggestion {
  title: string;
  description: string;
  duration_days: number;
  sections: SuggestionSection[];
  justification: string;
}

// Seção sugerida pela IA
export interface SuggestionSection {
  title: string;
  content: string;
  duration_minutes: number;
}

// Contexto do uso de estudo
export interface StudyContextType {
  // Dados
  plans: StudyPlan[];
  userProgress: UserStudyProgress[];
  onboardingSuggestion: PlanSuggestion | null;
  
  // Estado
  isLoading: boolean;
  error: Error | null;
  isOffline: boolean;
  
  // Ações
  startPlan: (planId: string) => Promise<any>;
  updateProgress: (planId: string, sectionId: string, percentage: number) => Promise<any>;
  submitOnboarding: (preferences: OnboardingPreferences) => Promise<any>;
  checkFreePlanLimitations: () => Promise<boolean>;
} 