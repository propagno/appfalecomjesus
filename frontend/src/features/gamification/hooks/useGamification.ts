import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { gamificationService } from '../services/gamificationService';
import { UserPoints, UserAchievement, Level, PointActionType, Achievement } from '../types';
import { LEVELS } from '../types';

interface AwardPointsResponse {
  pointsAwarded: number;
  newAchievements: UserAchievement[];
  levelUp: boolean;
  newLevel?: { level: number; name: string };
}

export function useGamification() {
  const queryClient = useQueryClient();

  // Busca os pontos do usuário
  const {
    data: userPoints,
    isLoading: isLoadingPoints,
    error: pointsError
  } = useQuery({
    queryKey: ['user-points'],
    queryFn: () => gamificationService.getUserPoints(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });

  // Busca as conquistas do usuário
  const {
    data: achievements,
    isLoading: isLoadingAchievements,
    error: achievementsError
  } = useQuery<Achievement[]>({
    queryKey: ['user-achievements'],
    queryFn: () => gamificationService.getAchievements(),
    staleTime: 15 * 60 * 1000, // 15 minutos
  });

  // Mutation para registrar atividade
  const { mutate: registerActivity, isPending: isRegisteringActivity } = useMutation<
    AwardPointsResponse,
    Error,
    { action: PointActionType; description?: string }
  >({
    mutationFn: (payload) =>
      gamificationService.awardPoints(payload.action, payload.description),
    onSuccess: (response) => {
      // Invalida as queries para recarregar os dados
      queryClient.invalidateQueries({ queryKey: ['user-points'] });
      queryClient.invalidateQueries({ queryKey: ['user-achievements'] });

      // Se houve level up, mostra notificação
      if (response.levelUp && response.newLevel) {
        // TODO: Mostrar notificação de level up
      }

      // Se ganhou pontos, mostra notificação
      if (response.pointsAwarded > 0) {
        // TODO: Mostrar notificação de pontos
      }

      // Se desbloqueou conquistas, mostra notificação
      if (response.newAchievements?.length > 0) {
        // TODO: Mostrar notificação de conquistas
      }
    }
  });

  // Mutation para resgatar recompensa de anúncio
  const { mutate: redeemAdReward, isPending: isRedeemingAdReward } = useMutation<
    AwardPointsResponse,
    Error,
    void
  >({
    mutationFn: () => gamificationService.awardPoints('watched_ad', 'Assistiu a um anúncio'),
    onSuccess: (response) => {
      // Invalida as queries para recarregar os dados
      queryClient.invalidateQueries({ queryKey: ['user-points'] });
      
      // Se ganhou pontos, mostra notificação
      if (response.pointsAwarded > 0) {
        // TODO: Mostrar notificação de pontos
      }
    }
  });

  // Calcula o nível atual do usuário
  const getCurrentLevel = (): Level | null => {
    if (!userPoints) return null;
    return LEVELS.find(
      level =>
        userPoints.total_points >= level.min_points &&
        userPoints.total_points <= level.max_points
    ) || null;
  };

  // Calcula o progresso para o próximo nível
  const getNextLevelProgress = (): number => {
    if (!userPoints) return 0;
    const currentLevel = getCurrentLevel();
    if (!currentLevel) return 0;
    
    const pointsInLevel = userPoints.total_points - currentLevel.min_points;
    const levelRange = currentLevel.max_points - currentLevel.min_points;
    return Math.min((pointsInLevel / levelRange) * 100, 100);
  };

  return {
    userPoints,
    achievements,
    isLoading: isLoadingPoints || isLoadingAchievements,
    error: pointsError || achievementsError,
    registerActivity,
    redeemAdReward,
    getCurrentLevel,
    getNextLevelProgress,
    isRegisteringActivity,
    isRedeemingAdReward
  };
} 