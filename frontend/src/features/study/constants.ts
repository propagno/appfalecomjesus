/**
 * Constantes utilizadas no módulo de estudos
 */

// Chaves para usar no React Query
export const QUERY_KEYS = {
  PLANS: 'study-plans',
  PLAN_DETAILS: 'study-plan-details',
  SECTIONS: 'study-sections',
  SECTION_CONTENT: 'study-section-content',
  PROGRESS: 'study-user-progress',
  CURRENT_STUDY: 'study-current',
  REFLECTIONS: 'study-reflections',
  CERTIFICATES: 'study-certificates',
  SUGGESTIONS: 'study-suggestions'
};

// Tempos de stale para diferentes tipos de dados
export const STALE_TIMES = {
  PLANS: 5 * 60 * 1000, // 5 minutos
  PROGRESS: 1 * 60 * 1000, // 1 minuto
  CONTENT: 10 * 60 * 1000, // 10 minutos
  REFLECTIONS: 2 * 60 * 1000 // 2 minutos
};

// Tempos de cache para diferentes tipos de dados
export const CACHE_TIMES = {
  PLANS: 60 * 60 * 1000, // 1 hora
  PROGRESS: 30 * 60 * 1000, // 30 minutos
  CONTENT: 24 * 60 * 60 * 1000, // 24 horas
  REFLECTIONS: 60 * 60 * 1000 // 1 hora
};

// Limites do plano Free
export const FREE_PLAN_LIMITS = {
  MAX_STUDY_DAYS: 10, // Máximo de 10 dias no plano Free por mês
  MAX_STUDY_PLANS: 2 // Máximo de 2 planos ativos no plano Free
};

// Status do progresso
export enum ProgressStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}

// Tipos de conteúdo
export enum ContentType {
  TEXT = 'text',
  AUDIO = 'audio',
  VIDEO = 'video',
  INTERACTIVE = 'interactive'
}

// Níveis de dificuldade
export enum DifficultyLevel {
  BEGINNER = 'iniciante',
  INTERMEDIATE = 'intermediário',
  ADVANCED = 'avançado'
}

// Tempos preferenciais
export enum PreferredTime {
  MORNING = 'manhã',
  AFTERNOON = 'tarde',
  EVENING = 'noite',
  ANY = 'qualquer'
}

export default {
  QUERY_KEYS,
  STALE_TIMES,
  CACHE_TIMES,
  FREE_PLAN_LIMITS,
  ProgressStatus,
  ContentType,
  DifficultyLevel,
  PreferredTime
}; 