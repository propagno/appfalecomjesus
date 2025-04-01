/**
 * Hook customizado para gerenciar o cache específico dos estudos bíblicos
 * Implementa o item 10.3.2 da migração - Cache específico para estudos
 */
import { useQueryClient } from '@tanstack/react-query';
import { useCallback } from 'react';
import { StudySection, UserStudyProgress } from '../types';
import { FEATURES } from '../../../shared/constants/config';
import { getFromCache, saveToCache } from '../../../shared/utils/cache';

// Interface para conteúdo de uma seção de estudo
interface StudyContent {
  id: string;
  section_id: string;
  content_type: 'text' | 'audio' | 'verse' | 'reflection';
  content: string;
  position: number;
}

// Prefixos para as chaves de consulta
const QUERY_KEYS = {
  plans: 'study-plans',
  plan: 'study-plan',
  sections: 'study-sections',
  content: 'study-content',
  progress: 'study-progress',
  reflections: 'study-reflections',
  certificates: 'study-certificates',
  currentStudy: 'current-study',
};

const useStudyCache = () => {
  const queryClient = useQueryClient();
  
  /**
   * Invalida o cache de progresso quando há atualizações
   */
  const invalidateProgressCache = useCallback((planId?: string) => {
    if (planId) {
      // Invalidar apenas o progresso do plano específico
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.progress, planId] });
    } else {
      // Invalidar todo o progresso
      queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.progress] });
    }
    
    // Também invalidar estudo atual
    queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.currentStudy] });
  }, [queryClient]);
  
  /**
   * Faz o pré-carregamento (prefetch) de seções subsequentes
   */
  const prefetchNextSections = useCallback(async (
    planId: string, 
    currentSectionPosition: number,
    sections: StudySection[]
  ) => {
    // Identificar a próxima seção
    const nextSection = sections.find(s => s.position === currentSectionPosition + 1);
    
    if (nextSection) {
      // Prefetch da próxima seção
      queryClient.prefetchQuery({
        queryKey: [QUERY_KEYS.content, nextSection.id],
        queryFn: () => getContentForOffline(nextSection.id)
      });
      
      // Se for a penúltima seção, também carrega a última
      if (currentSectionPosition === sections.length - 2) {
        const lastSection = sections.find(s => s.position === currentSectionPosition + 2);
        if (lastSection) {
          queryClient.prefetchQuery({
            queryKey: [QUERY_KEYS.content, lastSection.id],
            queryFn: () => getContentForOffline(lastSection.id)
          });
        }
      }
    }
  }, [queryClient]);
  
  /**
   * Armazena estado de progresso localmente para uso offline
   */
  const saveProgressLocally = useCallback(async (
    planId: string, 
    sectionId: string, 
    percentage: number
  ) => {
    if (FEATURES.offlineMode) {
      try {
        // Recuperar progresso atual do cache
        const cachedProgress = await getFromCache<Record<string, UserStudyProgress>>('offline-progress') || {};
        
        // Atualizar ou adicionar o progresso
        cachedProgress[planId] = {
          ...cachedProgress[planId],
          study_plan_id: planId,
          current_section_id: sectionId,
          completion_percentage: percentage,
          // Campos obrigatórios para o tipo UserStudyProgress
          id: cachedProgress[planId]?.id || `offline-${planId}`,
          user_id: cachedProgress[planId]?.user_id || 'offline-user',
          started_at: cachedProgress[planId]?.started_at || new Date().toISOString(),
        };
        
        // Salvar no cache local
        await saveToCache('offline-progress', cachedProgress, 7 * 24 * 60 * 60 * 1000); // 7 dias
        
        // Marcar que existem mudanças offline para sincronizar
        await saveToCache('has-offline-changes', true, 30 * 24 * 60 * 60 * 1000); // 30 dias
      } catch (error) {
        console.error('Erro ao salvar progresso offline:', error);
      }
    }
  }, []);
  
  /**
   * Recupera conteúdo de uma seção para uso offline
   */
  const getContentForOffline = useCallback(async (sectionId: string): Promise<StudyContent[]> => {
    if (FEATURES.offlineMode) {
      try {
        // Tentar recuperar do cache primeiro
        const cachedContent = await getFromCache<StudyContent[]>(`content-${sectionId}`);
        if (cachedContent) {
          return cachedContent;
        }
      } catch (error) {
        console.error('Erro ao recuperar conteúdo offline:', error);
      }
    }
    
    // Retornar array vazio se não encontrar no cache
    return [];
  }, []);
  
  /**
   * Armazena conteúdo de uma seção para uso offline
   */
  const saveContentForOffline = useCallback(async (sectionId: string, content: StudyContent[]) => {
    if (FEATURES.offlineMode) {
      try {
        // Salvar no cache com TTL longo
        await saveToCache(`content-${sectionId}`, content, 30 * 24 * 60 * 60 * 1000); // 30 dias
      } catch (error) {
        console.error('Erro ao salvar conteúdo offline:', error);
      }
    }
  }, []);
  
  /**
   * Sincroniza os dados offline quando a conexão é restaurada
   */
  const syncOfflineData = useCallback(async () => {
    // Verificar se existem mudanças offline
    const hasOfflineChanges = await getFromCache<boolean>('has-offline-changes');
    
    if (hasOfflineChanges) {
      // Recuperar dados de progresso offline
      const offlineProgress = await getFromCache<Record<string, UserStudyProgress>>('offline-progress') || {};
      
      // Sinalizamos que poderia enviar as atualizações para o servidor aqui
      // mas isso seria implementado no StudyContext que chamaria o studyService
      
      // Limpar flag de mudanças offline
      await saveToCache('has-offline-changes', false);
    }
  }, []);
  
  /**
   * Verifica se está operando em modo offline
   */
  const isOfflineMode = useCallback(async (): Promise<boolean> => {
    return !navigator.onLine && FEATURES.offlineMode;
  }, []);
  
  return {
    // Funções de cache
    invalidateProgressCache,
    prefetchNextSections,
    
    // Funções de offline
    saveProgressLocally,
    getContentForOffline,
    saveContentForOffline,
    syncOfflineData,
    isOfflineMode,
    
    // Constantes
    QUERY_KEYS,
  };
};

export default useStudyCache; 