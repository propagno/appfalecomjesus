import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import studyService from '../api/studyService';
import {
  StudyPlan,
  StudySection,
  UserStudyProgress,
  Reflection,
  Certificate,
  PlanFilters,
  OnboardingPreferences,
  PlanSuggestion
} from '../types';

// Define StudyContent locally since it's not exported from types
interface StudyContent {
  id: string;
  section_id: string;
  content_type: 'text' | 'audio' | 'verse' | 'reflection';
  content: string;
  position: number;
}

// Chaves de query para cache
export const STUDY_QUERY_KEYS = {
  plans: 'plans',
  plan: 'plan',
  sections: 'sections',
  content: 'content',
  progress: 'progress',
  currentStudy: 'currentStudy',
  reflections: 'reflections'
};

/**
 * Hook para gerenciar a lógica e estado da feature de estudo
 */
function useStudy(initialPlanId?: string) {
  const queryClient = useQueryClient();
  const [currentPlanId, setCurrentPlanId] = useState<string | undefined>(initialPlanId);
  const [currentSectionId, setCurrentSectionId] = useState<string | undefined>();
  const [filters, setFilters] = useState<PlanFilters>({
    page: 1,
    per_page: 10
  });
  const [onboardingSuggestion, setOnboardingSuggestion] = useState<PlanSuggestion | null>(null);

  // Consultas (Queries)
  
  // Buscar todos os planos de estudo com filtros
  const plansQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.plans, filters],
    queryFn: () => studyService.getStudyPlans(filters),
    enabled: !!filters
  });

  // Buscar detalhes de um plano específico
  const planDetailQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.plan, currentPlanId],
    queryFn: () => studyService.getStudyPlanById(currentPlanId!),
    enabled: !!currentPlanId
  });

  // Buscar seções de um plano
  const sectionsQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.sections, currentPlanId],
    queryFn: () => studyService.getStudySections(currentPlanId!),
    enabled: !!currentPlanId
  });

  // Buscar conteúdo de uma seção
  const sectionContentQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.content, currentSectionId],
    queryFn: () => studyService.getSectionContent(currentSectionId!),
    enabled: !!currentSectionId
  });

  // Buscar progresso do usuário em todos os planos
  const userProgressQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.progress],
    queryFn: () => studyService.getUserProgress()
  });

  // Buscar progresso específico do plano atual
  const planProgressQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.progress, currentPlanId],
    queryFn: () => studyService.getUserPlanProgress(currentPlanId!),
    enabled: !!currentPlanId
  });

  // Buscar reflexões do usuário
  const reflectionsQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.reflections],
    queryFn: () => studyService.getUserReflections()
  });

  // Buscar certificados do usuário
  const certificatesQuery = useQuery({
    queryKey: [STUDY_QUERY_KEYS.progress],
    queryFn: () => studyService.getUserCertificates()
  });

  // Mutações (Mutations)
  
  // Iniciar um novo plano de estudo
  const startPlanMutation = useMutation({
    mutationFn: (planId: string) => studyService.startStudyPlan(planId),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.progress] });
      setCurrentPlanId(data.study_plan_id);
      // Buscar a primeira seção para mostrar ao usuário
      if (sectionsQuery.data && sectionsQuery.data.length > 0) {
        const firstSection = sectionsQuery.data.find(section => section.position === 1);
        if (firstSection) {
          setCurrentSectionId(firstSection.id);
        }
      }
    }
  });

  // Atualizar progresso em um plano
  const updateProgressMutation = useMutation({
    mutationFn: (data: { planId: string, sectionId: string, completionPercentage: number }) => 
      studyService.updateProgress(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.progress] });
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.progress, currentPlanId] });
    }
  });

  // Salvar uma reflexão
  const saveReflectionMutation = useMutation({
    mutationFn: (data: { sectionId: string, reflectionText: string }) => 
      studyService.saveReflection(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.reflections] });
    }
  });

  // Gerar certificado
  const generateCertificateMutation = useMutation({
    mutationFn: (planId: string) => studyService.generateCertificate(planId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.progress] });
    }
  });

  // Enviar preferências de onboarding
  const submitOnboardingMutation = useMutation({
    mutationFn: (preferences: OnboardingPreferences) => 
      studyService.submitOnboardingPreferences(preferences),
    onSuccess: (data) => {
      setOnboardingSuggestion(data);
    }
  });

  // Criar plano personalizado
  const createPersonalizedPlanMutation = useMutation({
    mutationFn: (suggestion: PlanSuggestion) => 
      studyService.createPersonalizedPlan(suggestion),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: [STUDY_QUERY_KEYS.plans] });
      setCurrentPlanId(data.id);
      // Iniciar o plano automaticamente
      startPlanMutation.mutate(data.id);
    }
  });

  // Actions e Handlers
  
  // Manipular filtros de planos
  const handleFilterChange = useCallback((newFilters: Partial<PlanFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  }, []);

  // Mudar de página na listagem de planos
  const handlePageChange = useCallback((page: number) => {
    setFilters(prev => ({ ...prev, page }));
  }, []);

  // Selecionar um plano
  const selectPlan = useCallback((planId: string) => {
    setCurrentPlanId(planId);
  }, []);

  // Selecionar uma seção
  const selectSection = useCallback((sectionId: string) => {
    setCurrentSectionId(sectionId);
  }, []);

  // Iniciar um plano
  const startPlan = useCallback((planId: string) => {
    startPlanMutation.mutate(planId);
  }, [startPlanMutation]);

  // Marcar seção como concluída
  const completeSection = useCallback((sectionId: string, completionPercentage: number) => {
    if (!currentPlanId) return;
    
    updateProgressMutation.mutate({
      planId: currentPlanId,
      sectionId,
      completionPercentage
    });
  }, [currentPlanId, updateProgressMutation]);

  // Salvar uma reflexão do usuário
  const saveReflection = useCallback((reflectionText: string) => {
    if (!currentSectionId) return;
    
    saveReflectionMutation.mutate({
      sectionId: currentSectionId,
      reflectionText
    });
  }, [currentSectionId, saveReflectionMutation]);

  // Enviar preferências de onboarding
  const submitOnboarding = useCallback((preferences: OnboardingPreferences) => {
    submitOnboardingMutation.mutate(preferences);
  }, [submitOnboardingMutation]);

  // Confirmar e criar plano personalizado
  const confirmPersonalizedPlan = useCallback(() => {
    if (!onboardingSuggestion) return;
    
    createPersonalizedPlanMutation.mutate(onboardingSuggestion);
  }, [onboardingSuggestion, createPersonalizedPlanMutation]);

  // Gerar certificado para plano concluído
  const generateCertificate = useCallback((planId: string) => {
    generateCertificateMutation.mutate(planId);
  }, [generateCertificateMutation]);

  // Estados de loading e erro combinados
  const isLoading = 
    plansQuery.isLoading || 
    planDetailQuery.isLoading || 
    sectionsQuery.isLoading || 
    sectionContentQuery.isLoading || 
    userProgressQuery.isLoading;

  const isMutating = 
    startPlanMutation.isPending || 
    updateProgressMutation.isPending || 
    saveReflectionMutation.isPending || 
    submitOnboardingMutation.isPending || 
    createPersonalizedPlanMutation.isPending ||
    generateCertificateMutation.isPending;

  // Retornar objetos e funções necessárias
  return {
    // Dados
    plans: plansQuery.data?.plans || [],
    totalPlans: plansQuery.data?.total || 0,
    currentPlan: planDetailQuery.data,
    sections: sectionsQuery.data || [],
    sectionContent: sectionContentQuery.data || [],
    userProgress: userProgressQuery.data || [],
    currentPlanProgress: planProgressQuery.data,
    reflections: reflectionsQuery.data || [],
    certificates: certificatesQuery.data || [],
    onboardingSuggestion,
    filters,
    
    // Estados
    isLoading,
    isMutating,
    
    // Ações
    handleFilterChange,
    handlePageChange,
    selectPlan,
    selectSection,
    startPlan,
    completeSection,
    saveReflection,
    submitOnboarding,
    confirmPersonalizedPlan,
    generateCertificate
  };
}

export default useStudy; 