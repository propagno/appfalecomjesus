import React, { useState } from 'react';
import { useGamificationContext } from '../providers/GamificationProvider';
import useGamificationQuery from '../hooks/useGamificationQuery';
import { ActivityType, Level } from '../types';
import { toast } from 'react-toastify';
import PointsCard from '../components/PointsCard';
import AchievementsList from '../components/AchievementsList';
import NewAchievementModal from '../components/NewAchievementModal';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../../components/base/Tabs';
import { Medal, Award, Trophy, BarChart2 } from 'lucide-react';

/**
 * Página principal de gamificação que mostra pontos, conquistas e leaderboard
 */
export const GamificationPage: React.FC = () => {
  const { state, registerActivity, shareAchievement, dismissNewAchievement } = useGamificationContext();
  const [loading, setLoading] = useState<Record<string, boolean>>({});
  
  // Hooks React Query para dados adicionais
  const {
    useLeaderboardQuery,
    useUpcomingAchievementsQuery,
    useAllAchievementsQuery
  } = useGamificationQuery();
  
  // Buscar leaderboard e conquistas próximas
  const { data: leaderboard } = useLeaderboardQuery({ timeframe: 'weekly', limit: 10 });
  const { data: upcomingAchievements } = useUpcomingAchievementsQuery();
  const { data: allAchievements } = useAllAchievementsQuery();

  /**
   * Registra uma atividade e mostra feedback
   */
  const handleRegisterActivity = async (activity: ActivityType, details?: any) => {
    const key = `activity_${activity}`;
    setLoading(prev => ({ ...prev, [key]: true }));
    
    try {
      const result = await registerActivity(activity, details);
      
      toast.success(`🎉 Você ganhou ${result.points_earned} pontos!`);
      
      if (result.achievements_unlocked.length > 0) {
        toast.success(`🏆 ${result.achievements_unlocked.length} conquista(s) desbloqueada(s)!`);
      }
    } catch (error) {
      toast.error('Erro ao registrar atividade');
      console.error(error);
    } finally {
      setLoading(prev => ({ ...prev, [key]: false }));
    }
  };

  /**
   * Compartilha uma conquista
   */
  const handleShareAchievement = async (achievementId: string, network: 'facebook' | 'twitter' | 'whatsapp') => {
    try {
      const shareUrl = await shareAchievement(achievementId, network);
      
      // Simular compartilhamento abrindo URL
      window.open(shareUrl, '_blank');
      
      toast.success('Conquista compartilhada!');
    } catch (error) {
      toast.error('Erro ao compartilhar conquista');
      console.error(error);
    }
  };

  // Contador para pluralização
  const unlockedCount = state.userAchievements.length;

  // Calcular nível atual
  const currentLevel: Level | null = state.userPoints ? {
    level: state.userPoints.level,
    name: 'Nível ' + state.userPoints.level,
    min_points: 0,
    max_points: state.userPoints.next_level_threshold
  } : null;
  
  return (
    <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
      {/* Título da página */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Gamificação</h1>
        <p className="text-gray-600 mt-2">
          Acompanhe seu progresso, conquistas e posição no ranking.
        </p>
      </div>

      {/* Cartão de pontos */}
      <div className="mb-8">
        <PointsCard 
          points={state.userPoints?.total_points || 0} 
          level={currentLevel}
          levelProgress={state.userPoints ? (state.userPoints.total_points / state.userPoints.next_level_threshold) * 100 : 0} 
          streak={0} // TODO: Implementar streak
        />
      </div>

      {/* Tabs para navegação entre seções */}
      <Tabs defaultValue={0}>
        <TabsList>
          <TabsTrigger>
            <Award className="mr-2 h-5 w-5" />
            <span>Conquistas</span>
          </TabsTrigger>
          <TabsTrigger>
            <Trophy className="mr-2 h-5 w-5" />
            <span>Ranking</span>
          </TabsTrigger>
          <TabsTrigger>
            <BarChart2 className="mr-2 h-5 w-5" />
            <span>Atividade</span>
          </TabsTrigger>
        </TabsList>

        {/* Conteúdo da tab Conquistas */}
        <TabsContent value={0}>
          <AchievementsList />
        </TabsContent>

        {/* Conteúdo da tab Ranking */}
        <TabsContent value={1}>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-center">
              <Medal className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-1">Ranking em breve!</h3>
              <p className="text-gray-500">
                Compare seu progresso com outros usuários. Esta funcionalidade estará disponível em breve.
              </p>
            </div>
          </div>
        </TabsContent>

        {/* Conteúdo da tab Atividade */}
        <TabsContent value={2}>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-center">
              <BarChart2 className="h-12 w-12 text-blue-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-1">Histórico de Atividades</h3>
              <p className="text-gray-500">
                Veja seu histórico de pontos e conquistas. Esta funcionalidade estará disponível em breve.
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>

      {/* Modal para novas conquistas */}
      <NewAchievementModal />
    </div>
  );
};

export default GamificationPage; 