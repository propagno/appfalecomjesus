import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { gamificationService } from '../api/gamificationService';
import { 
  Achievement,
  RewardData,
  UserAchievement
} from '../types';

/**
 * Chaves para os queries relacionados à gamificação
 */
export enum GamificationQueryKeys {
  POINTS = 'userPoints',
  ACHIEVEMENTS = 'userAchievements',
  LEADERBOARD = 'leaderboard',
  SUMMARY = 'gamificationSummary',
  UPCOMING = 'upcomingAchievements',
  ALL_ACHIEVEMENTS = 'allAchievements',
}

/**
 * Hook que provê acesso aos dados de gamificação via React Query
 */
export const useGamificationQuery = () => {
  const queryClient = useQueryClient();
  
  // Query para obter os pontos do usuário
  const useUserPointsQuery = () => 
    useQuery({
      queryKey: [GamificationQueryKeys.POINTS],
      queryFn: () => gamificationService.getUserPoints(),
      staleTime: 1000 * 60 * 5, // 5 minutos
    });
  
  // Query para obter as conquistas do usuário
  const useUserAchievementsQuery = (
    filter?: { category?: string; status?: 'unlocked' | 'locked' | 'all' }
  ) => 
    useQuery({
      queryKey: [GamificationQueryKeys.ACHIEVEMENTS, filter],
      queryFn: () => gamificationService.getUserAchievements(filter),
      staleTime: 1000 * 60 * 5, // 5 minutos
    });
  
  // Query para obter uma conquista específica
  const useAchievementQuery = (achievementId: string) => 
    useQuery({
      queryKey: [GamificationQueryKeys.ACHIEVEMENTS, achievementId],
      queryFn: () => gamificationService.getAchievement(achievementId),
      enabled: !!achievementId,
    });
  
  // Mutation para marcar uma conquista como vista
  const useMarkAchievementAsSeenMutation = () => 
    useMutation({
      mutationFn: (achievementId: string) => 
        gamificationService.markAchievementAsSeen(achievementId),
      onSuccess: () => {
        // Invalidar o cache de conquistas do usuário
        queryClient.invalidateQueries({
          queryKey: [GamificationQueryKeys.ACHIEVEMENTS],
        });
      },
    });
  
  // Mutation para registrar uma recompensa
  const useRegisterRewardMutation = () => 
    useMutation({
      mutationFn: (rewardData: RewardData) => 
        gamificationService.registerReward(rewardData),
      onSuccess: () => {
        // Invalidar caches relevantes
        queryClient.invalidateQueries({
          queryKey: [GamificationQueryKeys.POINTS],
        });
        queryClient.invalidateQueries({
          queryKey: [GamificationQueryKeys.ACHIEVEMENTS],
        });
        queryClient.invalidateQueries({
          queryKey: [GamificationQueryKeys.SUMMARY],
        });
      },
    });
  
  // Query para obter o leaderboard
  const useLeaderboardQuery = (
    params?: { page?: number; limit?: number; timeframe?: 'weekly' | 'monthly' | 'alltime' }
  ) => 
    useQuery({
      queryKey: [GamificationQueryKeys.LEADERBOARD, params],
      queryFn: () => gamificationService.getLeaderboard(params),
      staleTime: 1000 * 60 * 5, // 5 minutos
    });
  
  // Mutation para compartilhar uma conquista
  const useShareAchievementMutation = () => 
    useMutation({
      mutationFn: ({ 
        achievementId, 
        network 
      }: { 
        achievementId: string; 
        network: 'facebook' | 'twitter' | 'whatsapp' 
      }) => 
        gamificationService.shareAchievement(achievementId, network),
    });
  
  // Query para obter o resumo de gamificação
  const useGamificationSummaryQuery = () => 
    useQuery({
      queryKey: [GamificationQueryKeys.SUMMARY],
      queryFn: () => gamificationService.getGamificationSummary(),
      staleTime: 1000 * 60 * 5, // 5 minutos
    });
  
  // Query para obter as próximas conquistas
  const useUpcomingAchievementsQuery = () => 
    useQuery({
      queryKey: [GamificationQueryKeys.UPCOMING],
      queryFn: () => gamificationService.getUpcomingAchievements(),
      staleTime: 1000 * 60 * 10, // 10 minutos
    });
  
  // Query para obter todas as conquistas
  const useAllAchievementsQuery = () => 
    useQuery({
      queryKey: [GamificationQueryKeys.ALL_ACHIEVEMENTS],
      queryFn: () => gamificationService.getAllAchievements(),
      staleTime: 1000 * 60 * 30, // 30 minutos - este dado muda raramente
    });

  // Forçar atualização de todos os dados de gamificação
  const refreshGamificationData = () => {
    queryClient.invalidateQueries({
      queryKey: [GamificationQueryKeys.POINTS],
    });
    queryClient.invalidateQueries({
      queryKey: [GamificationQueryKeys.ACHIEVEMENTS],
    });
    queryClient.invalidateQueries({
      queryKey: [GamificationQueryKeys.SUMMARY],
    });
    queryClient.invalidateQueries({
      queryKey: [GamificationQueryKeys.UPCOMING],
    });
    queryClient.invalidateQueries({
      queryKey: [GamificationQueryKeys.LEADERBOARD],
    });
  };

  return {
    useUserPointsQuery,
    useUserAchievementsQuery,
    useAchievementQuery,
    useMarkAchievementAsSeenMutation,
    useRegisterRewardMutation,
    useLeaderboardQuery,
    useShareAchievementMutation,
    useGamificationSummaryQuery,
    useUpcomingAchievementsQuery,
    useAllAchievementsQuery,
    refreshGamificationData,
  };
};

export default useGamificationQuery; 