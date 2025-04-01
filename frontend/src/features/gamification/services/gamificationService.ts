import { api } from '../../../lib/axios';
import {
  UserPoints,
  Achievement,
  UserAchievement,
  PointTransaction,
  GamificationNotification,
  PointActionType
} from '../types';

const ENDPOINTS = {
  USER_POINTS: '/gamification/user-points',
  ACHIEVEMENTS: '/gamification/achievements',
  USER_ACHIEVEMENTS: '/gamification/user-achievements',
  POINT_TRANSACTIONS: '/gamification/point-transactions',
  NOTIFICATIONS: '/gamification/notifications',
  AWARD_POINTS: '/gamification/award-points',
};

/**
 * Serviço para interação com a API de gamificação
 */
export const gamificationService = {
  /**
   * Obtém os pontos do usuário atual
   */
  getUserPoints: async (): Promise<UserPoints> => {
    const response = await api.get<UserPoints>(ENDPOINTS.USER_POINTS);
    return response.data;
  },
  
  /**
   * Obtém todas as conquistas disponíveis
   */
  getAchievements: async (): Promise<Achievement[]> => {
    const response = await api.get<Achievement[]>(ENDPOINTS.ACHIEVEMENTS);
    return response.data;
  },
  
  /**
   * Obtém as conquistas desbloqueadas pelo usuário
   */
  getUserAchievements: async (): Promise<UserAchievement[]> => {
    const response = await api.get<UserAchievement[]>(ENDPOINTS.USER_ACHIEVEMENTS);
    return response.data;
  },
  
  /**
   * Obtém o histórico de transações de pontos do usuário
   */
  getPointTransactions: async (limit?: number): Promise<PointTransaction[]> => {
    const response = await api.get<PointTransaction[]>(
      ENDPOINTS.POINT_TRANSACTIONS,
      { params: { limit } }
    );
    return response.data;
  },
  
  /**
   * Obtém notificações de gamificação não lidas
   */
  getNotifications: async (): Promise<GamificationNotification[]> => {
    const response = await api.get<GamificationNotification[]>(ENDPOINTS.NOTIFICATIONS);
    return response.data;
  },
  
  /**
   * Marca uma notificação como lida
   */
  markNotificationAsRead: async (notificationId: string): Promise<void> => {
    await api.patch(`${ENDPOINTS.NOTIFICATIONS}/${notificationId}/read`);
  },
  
  /**
   * Marca todas as notificações como lidas
   */
  markAllNotificationsAsRead: async (): Promise<void> => {
    await api.patch(`${ENDPOINTS.NOTIFICATIONS}/read-all`);
  },
  
  /**
   * Remove uma notificação
   */
  dismissNotification: async (notificationId: string): Promise<void> => {
    await api.delete(`${ENDPOINTS.NOTIFICATIONS}/${notificationId}`);
  },
  
  /**
   * Registra uma ação que concede pontos ao usuário
   */
  awardPoints: async (
    action: PointActionType,
    customDescription?: string
  ): Promise<{
    pointsAwarded: number;
    newAchievements: UserAchievement[];
    levelUp: boolean;
    newLevel?: { level: number; name: string };
  }> => {
    const response = await api.post(ENDPOINTS.AWARD_POINTS, {
      action,
      customDescription
    });
    return response.data;
  },

  // Mock para desenvolvimento sem backend
  getMockUserPoints: (): UserPoints => ({
    id: 'mock-points-id',
    user_id: 'mock-user-id',
    total_points: 345,
    level: 3,
    next_level_threshold: 600,
    last_updated: new Date().toISOString()
  }),

  getMockAchievements: (): Achievement[] => [
    {
      id: '1',
      code: 'first_login',
      name: 'Primeiro Login',
      description: 'Bem-vindo à jornada espiritual!',
      category: 'engagement',
      icon_url: '/images/achievements/first-login.png',
      points_reward: 10,
      difficulty: 'easy',
      requirements: 'Faça login pela primeira vez'
    },
    {
      id: '2',
      code: 'first_study',
      name: 'Estudante Dedicado',
      description: 'Completou seu primeiro estudo diário.',
      category: 'study',
      icon_url: '/images/achievements/first-study.png',
      points_reward: 20,
      difficulty: 'easy',
      requirements: 'Complete seu primeiro estudo'
    },
    {
      id: '3',
      code: 'weekly_streak',
      name: 'Constância Semanal',
      description: 'Logou por 7 dias consecutivos.',
      category: 'engagement',
      icon_url: '/images/achievements/week-streak.png',
      points_reward: 30,
      difficulty: 'medium',
      requirements: 'Faça login por 7 dias consecutivos'
    }
  ],

  getMockUserAchievements: (): UserAchievement[] => [
    {
      id: 'ua_1',
      user_id: 'mock-user-id',
      achievement_id: '1',
      achievement: {
        id: '1',
        code: 'first_login',
        name: 'Primeiro Login',
        description: 'Bem-vindo à jornada espiritual!',
        category: 'engagement',
        icon_url: '/images/achievements/first-login.png',
        points_reward: 10,
        difficulty: 'easy',
        requirements: 'Faça login pela primeira vez'
      },
      earned_at: new Date('2023-05-10').toISOString(),
      seen: false
    },
    {
      id: 'ua_2',
      user_id: 'mock-user-id',
      achievement_id: '2',
      achievement: {
        id: '2',
        code: 'first_study',
        name: 'Estudante Dedicado',
        description: 'Completou seu primeiro estudo diário.',
        category: 'study',
        icon_url: '/images/achievements/first-study.png',
        points_reward: 20,
        difficulty: 'easy',
        requirements: 'Complete seu primeiro estudo'
      },
      earned_at: new Date('2023-05-12').toISOString(),
      seen: false
    }
  ],

  getMockPointTransactions: (): PointTransaction[] => [
    {
      id: 'pt1',
      user_id: 'mock-user-id',
      action: 'daily_login',
      amount: 5,
      description: 'Login diário',
      created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 'pt2',
      user_id: 'mock-user-id',
      action: 'study_started',
      amount: 10,
      description: 'Iniciou o estudo "Fundamentos da Fé"',
      created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 'pt3',
      user_id: 'mock-user-id',
      action: 'achievement_unlocked',
      amount: 20,
      description: 'Conquistou: Estudante Dedicado',
      created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 'pt4',
      user_id: 'mock-user-id',
      action: 'daily_devotional',
      amount: 5,
      description: 'Leu o devocional do dia',
      created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString()
    }
  ],

  getMockNotifications: (): GamificationNotification[] => [
    {
      id: 'n1',
      user_id: 'mock-user-id',
      type: 'achievement_unlocked',
      title: 'Nova Conquista!',
      message: 'Você desbloqueou a conquista "Estudante Dedicado"',
      image_url: '/images/achievements/first-study.png',
      is_read: false,
      created_at: new Date().toISOString(),
      data: {
        achievement_id: '2'
      }
    },
    {
      id: 'n2',
      user_id: 'mock-user-id',
      type: 'streak_milestone',
      title: 'Sequência de 5 dias!',
      message: 'Você está usando o app há 5 dias seguidos!',
      is_read: false,
      created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      data: {
        streak: 5,
        points: 25
      }
    }
  ]
}; 