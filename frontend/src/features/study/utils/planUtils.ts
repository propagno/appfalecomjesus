/**
 * Utilitários para cálculos e verificações relacionados aos planos de estudo
 */
import { UserStudyProgress } from '../types';
import { FREE_PLAN_LIMITS } from '../constants';

/**
 * Verifica se um usuário no plano Free atingiu o limite de dias de estudos
 * @param progress Array com o progresso do usuário
 * @returns true se o limite foi atingido, false caso contrário
 */
export const isFreeUserLimitReached = (progress: UserStudyProgress[]): boolean => {
  if (!progress || progress.length === 0) {
    return false;
  }

  // Conta quantos dias de estudo o usuário já utilizou
  const activePlans = new Set(progress.map(p => p.study_plan_id));
  
  // Verifica se excedeu o número máximo de planos ativos
  if (activePlans.size >= FREE_PLAN_LIMITS.MAX_STUDY_PLANS) {
    return true;
  }
  
  // Verifica o total de dias estudados entre todos os planos
  const totalDaysStudied = progress.reduce((total, p) => {
    // Se o progresso está acima de 0%, considera um dia utilizado
    return p.completion_percentage > 0 ? total + 1 : total;
  }, 0);
  
  return totalDaysStudied >= FREE_PLAN_LIMITS.MAX_STUDY_DAYS;
};

/**
 * Calcula a porcentagem geral de conclusão de todos os planos de estudo
 * @param progress Array com o progresso do usuário
 * @returns Porcentagem geral (0-100)
 */
export const calculateOverallProgress = (progress: UserStudyProgress[]): number => {
  if (!progress || progress.length === 0) {
    return 0;
  }
  
  const totalProgress = progress.reduce((sum, p) => sum + p.completion_percentage, 0);
  return Math.round(totalProgress / progress.length);
};

/**
 * Verifica se um plano específico já foi iniciado pelo usuário
 * @param progress Array com o progresso do usuário
 * @param planId ID do plano a verificar
 * @returns true se o plano foi iniciado, false caso contrário
 */
export const isPlanStarted = (progress: UserStudyProgress[], planId: string): boolean => {
  if (!progress || progress.length === 0) {
    return false;
  }
  
  return progress.some(p => p.study_plan_id === planId);
};

/**
 * Verifica se um plano específico foi concluído pelo usuário
 * @param progress Array com o progresso do usuário
 * @param planId ID do plano a verificar
 * @returns true se o plano foi concluído (100%), false caso contrário
 */
export const isPlanCompleted = (progress: UserStudyProgress[], planId: string): boolean => {
  if (!progress || progress.length === 0) {
    return false;
  }
  
  const planProgress = progress.find(p => p.study_plan_id === planId);
  return planProgress ? planProgress.completion_percentage === 100 : false;
};

/**
 * Retorna o ID da seção atual de um plano específico
 * @param progress Array com o progresso do usuário
 * @param planId ID do plano
 * @returns ID da seção atual ou null se o plano não foi iniciado
 */
export const getCurrentSectionId = (progress: UserStudyProgress[], planId: string): string | null => {
  if (!progress || progress.length === 0) {
    return null;
  }
  
  const planProgress = progress.find(p => p.study_plan_id === planId);
  return planProgress ? planProgress.current_section_id : null;
};

/**
 * Formata a porcentagem para exibição
 * @param percentage Número representando a porcentagem
 * @returns String formatada (ex: "85%")
 */
export const formatPercentage = (percentage: number): string => {
  return `${Math.round(percentage)}%`;
}; 