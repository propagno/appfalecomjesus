import { User } from '../../auth/types';

/**
 * Representa um plano de estudo completo
 */
export interface StudyPlan {
  id: string;
  title: string;
  description: string;
  duration_days: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  category: string;
  image_url?: string;
  created_at: string;
}

/**
 * Representa uma seção/dia de um plano de estudo
 */
export interface StudySection {
  id: string;
  study_plan_id: string;
  title: string;
  position: number;
  duration_minutes: number;
}

/**
 * Representa o conteúdo específico de uma seção de estudo
 */
export interface StudyContent {
  id: string;
  section_id: string;
  content_type: 'text' | 'audio' | 'video';
  content: string;
  position: number;
}

/**
 * Representa o progresso do usuário em um plano de estudo
 */
export interface UserStudyProgress {
  id: string;
  user_id: string;
  study_plan_id: string;
  current_section_id: string;
  completion_percentage: number;
  started_at: string;
  completed_at?: string;
}

/**
 * Representa uma reflexão escrita pelo usuário sobre uma seção de estudo
 */
export interface Reflection {
  id: string;
  user_id: string;
  study_section_id: string;
  reflection_text: string;
  created_at: string;
}

/**
 * Representa um certificado gerado ao concluir um plano de estudo
 */
export interface Certificate {
  id: string;
  user_id: string;
  study_plan_id: string;
  completion_date: string;
  certificate_code: string;
  download_count: number;
}

/**
 * Resposta da API com a lista de planos
 */
export interface StudyPlanListItem {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration_days: number;
  image_url?: string;
}

/**
 * Parâmetros para filtrar planos de estudo
 */
export interface PlanFilters {
  category?: string;
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
  duration?: 'short' | 'medium' | 'long';
  search?: string;
}

/**
 * Resposta do onboarding para iniciar um plano personalizado
 */
export interface OnboardingPreferences {
  objectives: string[];
  bible_experience_level: 'beginner' | 'intermediate' | 'advanced';
  content_preferences: Array<'text' | 'audio' | 'video'>;
  preferred_time: 'morning' | 'afternoon' | 'evening';
}

/**
 * Resposta do onboarding para iniciar um plano personalizado
 */
export interface OnboardingFormData extends OnboardingPreferences {
  user_id: string;
}

/**
 * Formato de um plano sugerido pela IA após o onboarding
 */
export interface PlanSuggestion {
  title: string;
  description: string;
  duration_days: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  category: string;
  sections: Array<{
    title: string;
    content: string;
    duration_minutes: number;
  }>;
}

export interface StudyContextType {
  currentPlan: StudyPlan | null;
  currentSection: StudySection | null;
  userProgress: UserStudyProgress | null;
  loading: boolean;
  error: string | null;
  fetchCurrentStudy: () => Promise<void>;
  markSectionComplete: (sectionId: string) => Promise<void>;
  onboardingSuggestion: PlanSuggestion | null;
  setOnboardingSuggestion: (suggestion: PlanSuggestion | null) => void;
  isPersonalizedPlanCreating: boolean;
  personalizedPlanError: string | null;
}

export interface CreatePersonalizedPlanRequest {
  user_id?: string; // Pode ser opcional se vier do token
  preferences: OnboardingFormData;
}

export interface CreatePersonalizedPlanResponse {
  status: 'success' | 'error';
  plan_id?: string;
  message?: string;
}

export interface StudyPlansResponse {
  plans: StudyPlanListItem[];
  total: number;
  page: number;
  limit: number;
}

export interface CurrentStudyResponse {
  plan: StudyPlan;
  current_section: StudySection;
  progress: UserStudyProgress;
}

export interface CreateReflectionRequest {
  study_section_id: string;
  reflection_text: string;
} 