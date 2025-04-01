import React, { createContext, useContext, useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import useGamificationQuery, { GamificationQueryKeys } from '../hooks/useGamificationQuery';
import {
  ActivityType,
  // GamificationState, // Remover import se existir
  RewardData,
  RewardResponse,
  UserAchievement,
  UserPoints,
  Level,
  Achievement,
  PointTransaction,
  GamificationNotification
} from '../types';
import { toast } from 'react-toastify';

// Definindo a interface base do estado de gamificação
interface GamificationState {
  userPoints: UserPoints | null;
  userLevel: Level | null;
  achievements: Achievement[]; // Todas as conquistas disponíveis
  userAchievements: UserAchievement[]; // Conquistas do usuário
  unlockedAchievements: UserAchievement[]; // Redundante? Manter por ora.
  pointTransactions: PointTransaction[];
  notifications: GamificationNotification[];
  isLoading: boolean;
  error: Error | null; // Usar tipo Error
}

// Atualizando o tipo GamificationState em memória para incluir novas conquistas e recompensas recentes
interface ExtendedGamificationState extends GamificationState {
  newAchievements: UserAchievement[];
  recentRewards: RewardResponse[];
}

// Valor padrão para o contexto de gamificação, inicializando todas as propriedades
const defaultGamificationState: ExtendedGamificationState = {
  userPoints: null,
  userLevel: null,
  achievements: [],
  userAchievements: [],
  unlockedAchievements: [],
  pointTransactions: [],
  notifications: [],
  newAchievements: [],
  recentRewards: [],
  isLoading: false,
  error: null,
};

// Definição da interface para o contexto
interface GamificationContextProps {
  state: ExtendedGamificationState;
  registerActivity: (activity: ActivityType, details?: any) => Promise<RewardResponse>;
  dismissNewAchievement: (achievementId: string) => void;
  shareAchievement: (achievementId: string, network: 'facebook' | 'twitter' | 'whatsapp') => Promise<string>;
  refreshGamificationData: () => void;
}

// Criação do contexto
const GamificationContext = createContext<GamificationContextProps | undefined>(undefined);

// Props para o provider
interface GamificationProviderProps {
  children: React.ReactNode;
}

/**
 * Provider que gerencia o estado global de gamificação da aplicação
 */
export const GamificationProvider: React.FC<GamificationProviderProps> = ({ children }) => {
  const [state, setState] = useState<ExtendedGamificationState>(defaultGamificationState);
  const queryClient = useQueryClient();

  const {
    useUserPointsQuery,
    useUserAchievementsQuery,
    useRegisterRewardMutation,
    useMarkAchievementAsSeenMutation,
    useShareAchievementMutation,
    refreshGamificationData,
  } = useGamificationQuery();

  // Queries e mutations
  const { data: userPoints, isLoading: isLoadingPoints, error: pointsError } = useUserPointsQuery();
  // Ajuste: A query retorna UserAchievement[], não Achievement[]
  const { data: userAchievementsData, isLoading: isLoadingAchievements, error: achievementsError } = useUserAchievementsQuery();
  const registerRewardMutation = useRegisterRewardMutation();
  const markAchievementAsSeenMutation = useMarkAchievementAsSeenMutation();
  const shareAchievementMutation = useShareAchievementMutation();

  // Atualiza o estado quando os dados mudam
  useEffect(() => {
    // TODO: Buscar todas as achievements disponíveis (state.achievements)
    // TODO: Calcular userLevel a partir de userPoints
    setState(prevState => ({
      ...prevState,
      userPoints: userPoints || null,
      userAchievements: userAchievementsData?.achievements || [], // Atualiza userAchievements
      unlockedAchievements: userAchievementsData?.achievements || [], // Atualiza unlockedAchievements (ou remover se redundante)
      isLoading: isLoadingPoints || isLoadingAchievements,
      error: pointsError || achievementsError || null, // Garantir que seja Error | null
    }));
  }, [userPoints, userAchievementsData, isLoadingPoints, isLoadingAchievements, pointsError, achievementsError]);

  // Observer para novas conquistas
  useEffect(() => {
    const unsubscribe = queryClient.getQueryCache().subscribe(() => {
      // Usar state.userAchievements como base para comparação
      const currentAchievements = queryClient.getQueryData<{ achievements: UserAchievement[] }>([GamificationQueryKeys.ACHIEVEMENTS])?.achievements || [];
      const previousAchievements = state.userAchievements || []; // Comparar com userAchievements do estado

      if (currentAchievements.length > previousAchievements.length) {
        const newOnes = currentAchievements.filter(
          // A comparação deve ser feita em UserAchievement
          current => !previousAchievements.some(prev => prev.id === current.id)
        );

        if (newOnes.length > 0) {
          setState(prev => ({
            ...prev,
            newAchievements: [...prev.newAchievements, ...newOnes]
          }));

          newOnes.forEach(ua => {
            toast.success(`🏆 Nova conquista: ${ua.achievement.name}`, {
              position: "top-right",
              autoClose: 5000,
              closeOnClick: true,
              pauseOnHover: true,
            });
          });
        }
      }
    });

    return () => {
      unsubscribe();
    };
  }, [queryClient, state.userAchievements]); // Depender de state.userAchievements

  /**
   * Registra uma atividade do usuário para ganhar pontos e potencialmente conquistar novos badges
   */
  const registerActivity = async (activityType: ActivityType, details?: any) => {
    const rewardData: RewardData = {
      activity_type: activityType,
      additional_info: details
    };

    try {
      const result = await registerRewardMutation.mutateAsync(rewardData);

      // Atualizar o estado com a recompensa
      setState(prev => ({
        ...prev,
        recentRewards: [result, ...(prev.recentRewards || [])].slice(0, 10), // Usar prev.recentRewards
        userPoints: {
          ...(prev.userPoints || { id: '', user_id: '', total_points: 0, level: 0, next_level_threshold: 0, last_updated: '' }),
          total_points: result.current_points,
          level: result.level
        } as UserPoints
        // TODO: Atualizar userLevel se necessário
      }));

      return result;
    } catch (error) {
      console.error('Erro ao registrar atividade:', error);
      throw error; // Re-throw para tratamento no chamador
    }
  };

  /**
   * Remove uma conquista da lista de novas conquistas
   */
  const dismissNewAchievement = (achievementId: string) => {
    setState(prev => ({
      ...prev,
      newAchievements: prev.newAchievements.filter(ua => ua.achievement_id !== achievementId) // Comparar com achievement_id
    }));

    markAchievementAsSeenMutation.mutate(achievementId);
  };

  /**
   * Compartilha uma conquista nas redes sociais
   */
  const shareAchievement = async (achievementId: string, network: 'facebook' | 'twitter' | 'whatsapp') => {
    try {
      const result = await shareAchievementMutation.mutateAsync({ achievementId, network });

      await registerActivity(ActivityType.SHARE_CONTENT, { achievementId, network });

      return result.shareUrl;
    } catch (error) {
      console.error('Erro ao compartilhar conquista:', error);
      throw error;
    }
  };

  // O valor do contexto
  const contextValue: GamificationContextProps = {
    state,
    registerActivity,
    dismissNewAchievement,
    shareAchievement,
    refreshGamificationData,
  };

  return (
    <GamificationContext.Provider value={contextValue}>
      {children}
    </GamificationContext.Provider>
  );
};

/**
 * Hook para utilizar o contexto de gamificação
 */
export const useGamificationContext = () => {
  const context = useContext(GamificationContext);

  if (context === undefined) {
    throw new Error('useGamificationContext deve ser usado dentro de um GamificationProvider');
  }

  return context;
};

export default GamificationProvider; 