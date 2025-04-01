/**
 * Hook customizado para usar React Query com a feature de estudos
 * Implementação do item 10.3.3 da migração - Integração com serviços reais
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useState, useEffect, useCallback } from 'react';
import { useToast } from '../../../shared/hooks/useToast';
import useStudyCache from './useStudyCache';
import studyService from '../api/studyService';
import {
  StudyPlan,
  StudySection,
  UserStudyProgress,
  PlanFilters,
  OnboardingPreferences,
  Reflection,
  Certificate,
  CreatePersonalizedPlanResponse,
  PlanSuggestion
} from '../types';
import { FEATURES, API_URLS } from '../../../shared/constants/config';
import { useAuthContext } from '../../auth/contexts/AuthContext';
import { api } from '../../../shared/services/api';
import { useLocalStorage } from '../../../shared/hooks/useLocalStorage';
import { QUERY_KEYS } from '../constants';
import { isFreeUserLimitReached } from '../utils/planUtils';
import { useAuth } from '../../auth/hooks/useAuth';
import { PlanType } from '../../monetization/types';

// Define local interfaces for types not exported from types file
interface StudyContent {
  id: string;
  section_id: string;
  content_type: 'text' | 'audio' | 'verse' | 'reflection';
  content: string;
  position: number;
}

const useStudyQuery = () => {
  const toast = useToast();
  const queryClient = useQueryClient();
  const { isAuthenticated, isAuthStatusChecked, user } = useAuthContext();
  const { 
    QUERY_KEYS: studyCacheKeys, 
    invalidateProgressCache, 
    prefetchNextSections,
    saveProgressLocally,
    isOfflineMode
  } = useStudyCache();
  
  const [isOffline, setIsOffline] = useState(!navigator.onLine);
  const [error, setError] = useState<Error | null>(null);
  const [localPlans, setLocalPlans] = useLocalStorage<StudyPlan[]>('study_plans', []);
  const [localProgress, setLocalProgress] = useLocalStorage<UserStudyProgress[]>('study_progress', []);
  const [onboardingSuggestion, setOnboardingSuggestion] = useLocalStorage<PlanSuggestion | null>('onboarding_suggestion', null);
  
  // Estado local
  const [filters, setFilters] = useState<PlanFilters>({
    page: 1,
    per_page: 10,
  });
  
  // Checar status offline na montagem e adicionar listener para mudanças
  useEffect(() => {
    const checkOfflineStatus = async () => {
      const offline = await isOfflineMode();
      setIsOffline(offline);
    };
    
    checkOfflineStatus();
    
    // Adicionar event listeners para monitorar status online/offline
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [isOfflineMode]);

  // Consulta principal para buscar planos de estudo
  const { data: plansData, isLoading: isLoadingPlans } = useQuery({
    queryKey: [QUERY_KEYS.PLANS],
    queryFn: async () => {
      const response = await api.get(`${API_URLS.study}/plans`);
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
    enabled: !isOffline
  });

  // Efeito para lidar com o sucesso do fetch de planos
  useEffect(() => {
    if (plansData?.plans) {
      setLocalPlans(plansData.plans);
    }
  }, [plansData]);

  // Busca progresso do usuário
  const { data: progressData, isLoading: isLoadingProgress } = useQuery({
    queryKey: [QUERY_KEYS.PROGRESS, user?.id],
    queryFn: async () => {
      const response = await api.get(`${API_URLS.study}/progress`);
      return response.data;
    },
    staleTime: 1 * 60 * 1000, // 1 minuto
    enabled: !!user && !isOffline
  });

  // Efeito para lidar com o sucesso do fetch de progresso
  useEffect(() => {
    if (progressData?.progress) {
      setLocalProgress(progressData.progress);
    }
  }, [progressData]);

  // Query para buscar o estudo atual do usuário
  const { 
    data: currentStudy,
    isLoading: isLoadingCurrentStudy
  } = useQuery({
    queryKey: [QUERY_KEYS.CURRENT_STUDY],
    queryFn: () => studyService.getCurrentStudy(),
    staleTime: 60 * 1000, // 1 minuto
    enabled: isAuthStatusChecked && isAuthenticated && !isOffline,
  });

  // Mutação para iniciar um plano
  const startPlanMutation = useMutation({
    mutationFn: async (planId: string) => {
      const response = await api.post(`${API_URLS.study}/plans/${planId}/start`);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PROGRESS] });
      // Adicionar o novo progresso ao cache local
      setLocalProgress((prev) => [...prev, data]);
    },
    onError: (err: Error) => {
      setError(err);
    }
  });

  // Mutação para atualizar progresso
  const updateProgressMutation = useMutation({
    mutationFn: async ({ 
      plan_id, 
      section_id, 
      completion_percentage 
    }: { 
      plan_id: string; 
      section_id: string; 
      completion_percentage: number;
    }) => {
      const response = await api.post(`${API_URLS.study}/progress/update`, {
        plan_id,
        section_id,
        completion_percentage
      });
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PROGRESS] });
      // Atualizar progresso no cache local
      setLocalProgress((prev) => 
        prev.map(p => p.study_plan_id === data.study_plan_id ? data : p)
      );
    },
    onError: (err: Error) => {
      setError(err);
    }
  });

  // Mutação para enviar preferências do onboarding
  const submitOnboardingMutation = useMutation({
    mutationFn: async (preferences: OnboardingPreferences) => {
      const response = await api.post(`${API_URLS.study}/init-plan`, preferences);
      return response.data;
    },
    onSuccess: (data) => {
      if (data?.suggestion) {
        setOnboardingSuggestion(data.suggestion);
      }
    },
    onError: (err: Error) => {
      setError(err);
    }
  });

  // Função para verificar limites do plano Free
  const checkFreePlanLimitations = useCallback(async (): Promise<boolean> => {
    // Verifica localmente se o usuário atingiu o limite
    if (!user || user.subscription.plan_type.toLowerCase() === PlanType.PREMIUM.toLowerCase()) {
      return true; // Premium não tem limitações
    }

    try {
      // Usar dados em cache ou buscar do servidor
      const progress = progressData && 'progress' in progressData ? progressData.progress : localProgress;
      
      // Verificar se o usuário atingiu o limite de dias do plano Free
      const limitReached = isFreeUserLimitReached(progress);
      
      return !limitReached;
    } catch (error) {
      console.error('Erro ao verificar limitações do plano:', error);
      return false; // Em caso de erro, impedir o acesso para garantir
    }
  }, [user, progressData, localProgress]);

  // Função para sincronizar dados offline
  const syncOfflineData = useCallback(async () => {
    if (!isOffline && localProgress.length > 0) {
      // Tentativa de sincronizar progressos não salvos
      try {
        // Aqui você pode implementar lógica para detectar mudanças
        // feitas offline e sincronizá-las
        queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PROGRESS] });
      } catch (error) {
        console.error('Erro ao sincronizar dados offline:', error);
      }
    }
  }, [isOffline, localProgress, queryClient]);

  // Efeito para sincronizar dados quando voltar online
  useEffect(() => {
    if (!isOffline) {
      syncOfflineData();
    }
  }, [isOffline, syncOfflineData]);

  // Handler para mudar filtros
  const handleFilterChange = useCallback((newFilters: Partial<PlanFilters>) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  }, []);
  
  // Handler para mudar página
  const handlePageChange = useCallback((page: number) => {
    setFilters(prev => ({ ...prev, page }));
  }, []);
  
  // Função para buscar detalhes de um plano específico
  const fetchPlanDetails = useCallback(async (planId: string): Promise<StudyPlan | null> => {
    try {
      return await queryClient.fetchQuery({
        queryKey: [QUERY_KEYS.PLAN_DETAILS, planId],
        queryFn: () => studyService.getStudyPlanById(planId),
        staleTime: 5 * 60 * 1000, // 5 minutos
      });
    } catch (error) {
      console.error("Erro ao buscar detalhes do plano:", error);
      toast.error("Erro ao carregar detalhes do plano. Tente novamente.");
      return null;
    }
  }, [queryClient, QUERY_KEYS.PLAN_DETAILS, toast]);
  
  // Função para buscar todos os planos (força um refetch)
  const fetchPlans = useCallback(async (): Promise<void> => {
    try {
      await queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PLANS] });
    } catch (error) {
      console.error("Erro ao buscar planos:", error);
      toast.error("Erro ao atualizar lista de planos. Tente novamente.");
    }
  }, [queryClient, QUERY_KEYS.PLANS, toast]);
  
  // Função para iniciar um plano
  const startPlan = async (planId: string): Promise<void> => {
    if (isOffline) {
      setError(new Error('Não é possível iniciar um plano offline'));
      return;
    }
    return startPlanMutation.mutateAsync(planId);
  };
  
  // Função para atualizar progresso
  const updateProgress = async (
    plan_id: string, 
    section_id: string, 
    completion_percentage: number
  ): Promise<void> => {
    if (isOffline) {
      // Salvar localmente para sincronizar depois
      setLocalProgress((prev) => 
        prev.map(p => p.study_plan_id === plan_id 
          ? { ...p, current_section_id: section_id, completion_percentage } 
          : p
        )
      );
      return;
    }
    
    return updateProgressMutation.mutateAsync({
      plan_id,
      section_id,
      completion_percentage
    });
  };
  
  // Função para obter estudo atual
  const getCurrentStudy = useCallback((): UserStudyProgress | null => {
    return currentStudy || null;
  }, [currentStudy]);
  
  // Função para enviar preferências do onboarding
  const submitOnboarding = async (preferences: OnboardingPreferences): Promise<void> => {
    if (isOffline) {
      setError(new Error('Não é possível enviar preferências offline'));
      return;
    }
    return submitOnboardingMutation.mutateAsync(preferences);
  };
  
  // Função para confirmar plano personalizado
  const confirmPersonalizedPlan = useCallback((): Promise<void> => {
    if (!onboardingSuggestion) {
      toast.error("Não há sugestão de plano para confirmar.");
      return Promise.resolve();
    }
    
    // Implemente a lógica para confirmar o plano personalizado
    toast.error("Função de confirmação de plano personalizado não implementada.");
    return Promise.resolve();
  }, [onboardingSuggestion, toast]);
  
  // Função para criar plano personalizado
  const createPersonalizedPlan = useCallback(async (
    data: OnboardingPreferences
  ): Promise<CreatePersonalizedPlanResponse | null> => {
    try {
      // Primeiro obter a sugestão
      const suggestion = await studyService.submitOnboardingPreferences(data);
      
      // Depois criar o plano com base na sugestão
      const plan = await studyService.createPersonalizedPlan(suggestion);
      
      return {
        plan_id: plan.id,
        message: "Plano personalizado criado com sucesso!"
      };
    } catch (error) {
      console.error("Erro ao criar plano personalizado:", error);
      toast.error("Erro ao criar plano personalizado. Tente novamente.");
      return null;
    }
  }, [toast]);
  
  // Estados combinados para loading e erros
  const isLoading = 
    isLoadingPlans || 
    isLoadingProgress || 
    isLoadingCurrentStudy;
  
  const isMutating = 
    startPlanMutation.isPending || 
    updateProgressMutation.isPending || 
    submitOnboardingMutation.isPending;
  
  return {
    // Dados
    plans: plansData && 'plans' in plansData ? plansData.plans : localPlans,
    totalPlans: plansData && 'total' in plansData ? plansData.total : 0,
    userProgress: progressData && 'progress' in progressData ? progressData.progress : localProgress,
    
    // Estado de carregamento
    isLoading,
    isMutating,
    error,
    
    // Estado de onboarding
    onboardingSuggestion,
    
    // Filtros
    filters,
    handleFilterChange,
    handlePageChange,
    
    // Ações
    fetchPlans,
    fetchPlanDetails,
    startPlan,
    updateProgress,
    getCurrentStudy,
    
    // Ações de onboarding
    submitOnboarding,
    confirmPersonalizedPlan,
    
    // Progresso
    createPersonalizedPlan,
    
    // Status de rede
    isOffline,
    
    // Verificação de plano
    checkFreePlanLimitations,
  };
};

export default useStudyQuery; 