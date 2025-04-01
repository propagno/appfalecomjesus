import { gamificationApi } from '../../../shared/services/api';
import { API_URLS } from '../../../shared/constants/apiUrls';
import { 
  UserPoints, 
  UserAchievement, 
  Achievement, 
  ActivityType,
  RewardData,
  RewardResponse,
  LeaderboardItem,
  UserAchievementsResponse,
  LeaderboardResponse
} from '../types';

/**
 * Serviço de API para integração com o microsserviço de Gamificação
 */
export const gamificationService = {
  /**
   * Obter os pontos do usuário atual
   */
  async getUserPoints(): Promise<UserPoints> {
    const { data } = await gamificationApi.get('/user-points');
    return data;
  },

  /**
   * Obter as conquistas do usuário
   * @param filter filtro opcional por categoria ou status
   */
  async getUserAchievements(
    filter?: { category?: string; status?: 'unlocked' | 'locked' | 'all' }
  ): Promise<UserAchievementsResponse> {
    const { data } = await gamificationApi.get('/user-achievements', { params: filter });
    return data;
  },

  /**
   * Obter detalhes de uma conquista específica
   * @param achievementId ID da conquista
   */
  async getAchievement(achievementId: string): Promise<Achievement> {
    const { data } = await gamificationApi.get(`/achievements/${achievementId}`);
    return data;
  },

  /**
   * Marcar uma conquista como visualizada pelo usuário
   * @param achievementId ID da conquista
   */
  async markAchievementAsSeen(achievementId: string): Promise<void> {
    await gamificationApi.post(`/user-achievements/${achievementId}/seen`);
  },

  /**
   * Registrar atividade do usuário para obter recompensa (pontos)
   * @param activityData dados da atividade realizada
   */
  async registerReward(activityData: RewardData): Promise<RewardResponse> {
    const { data } = await gamificationApi.post('/reward', activityData);
    return data;
  },

  /**
   * Obter o ranking de líderes
   * @param params parâmetros opcionais de paginação e filtro
   */
  async getLeaderboard(
    params?: { page?: number; limit?: number; timeframe?: 'weekly' | 'monthly' | 'alltime' }
  ): Promise<LeaderboardResponse> {
    const { data } = await gamificationApi.get('/leaderboard', { params });
    return data;
  },

  /**
   * Compartilhar uma conquista nas redes sociais
   * @param achievementId ID da conquista
   * @param network rede social para compartilhamento
   */
  async shareAchievement(
    achievementId: string,
    network: 'facebook' | 'twitter' | 'whatsapp'
  ): Promise<{ shareUrl: string }> {
    const { data } = await gamificationApi.post(`/achievements/${achievementId}/share`, { network });
    return data;
  },

  /**
   * Obter um resumo da gamificação do usuário
   */
  async getGamificationSummary(): Promise<{
    points: UserPoints;
    recentAchievements: UserAchievement[];
    level: number;
    rank: number;
  }> {
    const { data } = await gamificationApi.get('/summary');
    return data;
  },

  /**
   * Obter as próximas conquistas que o usuário está perto de desbloquear
   */
  async getUpcomingAchievements(): Promise<{
    achievements: Achievement[];
    progress: Record<string, number>;
  }> {
    const { data } = await gamificationApi.get('/upcoming-achievements');
    return data;
  },

  /**
   * Obter todas as conquistas disponíveis no sistema
   */
  async getAllAchievements(): Promise<Achievement[]> {
    const { data } = await gamificationApi.get('/achievements');
    return data;
  }
};

export default gamificationService; 