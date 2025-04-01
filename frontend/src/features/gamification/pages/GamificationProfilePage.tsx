import React, { useEffect } from 'react';
import { useGamificationContext } from '../providers/GamificationProvider';
import PointsCard from '../components/PointsCard';
import AchievementsList from '../components/AchievementsList';
import PointTransactionList from '../components/PointTransactionList';
import { Container } from '@/components/ui/container';
import { Card } from '../../../components/ui/card';
import { LEVELS } from '../types';

/**
 * Página de perfil de gamificação do usuário
 */
export const GamificationProfilePage: React.FC = () => {
  const { 
    state: { userPoints, achievements, isLoading },
    refreshGamificationData 
  } = useGamificationContext();

  // Encontrar o nível atual com base nos pontos
  const getCurrentLevel = () => {
    if (!userPoints) return LEVELS[0];
    return LEVELS.find(level => 
      level.level === userPoints.level
    ) || LEVELS[0];
  };

  // Calcular progresso para o próximo nível
  const getLevelProgress = () => {
    if (!userPoints) return 0;
    const currentLevel = getCurrentLevel();
    if (currentLevel.max_points === Number.MAX_SAFE_INTEGER) return 100;
    
    const pointsInCurrentLevel = userPoints.total_points - currentLevel.min_points;
    const pointsToNextLevel = currentLevel.max_points - currentLevel.min_points;
    return Math.min(Math.floor((pointsInCurrentLevel / pointsToNextLevel) * 100), 100);
  };

  // Valor padrão para a sequência diária
  const getDailyStreak = () => {
    // Usamos um valor padrão de 0 já que o current_streak não está definido no tipo UserPoints
    return 0;
  };

  useEffect(() => {
    // Carregar dados de gamificação ao montar o componente
    refreshGamificationData();
  }, [refreshGamificationData]);

  return (
    <Container>
      <div className="space-y-8">
        {/* Seção de progresso do usuário */}
        <section>
          <h2 className="text-2xl font-bold mb-4">Meu Progresso</h2>
          <PointsCard 
            points={userPoints?.total_points || 0}
            level={getCurrentLevel()}
            levelProgress={getLevelProgress()}
            streak={getDailyStreak()}
            isLoading={isLoading}
          />
        </section>

        {/* Seção de estatísticas */}
        <section>
          <h2 className="text-2xl font-bold mb-4">Minhas Estatísticas</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-4">
              <div className="text-center">
                <p className="text-gray-500 mb-1">Total de Pontos</p>
                <p className="text-3xl font-bold">{userPoints?.total_points || 0}</p>
              </div>
            </Card>
            <Card className="p-4">
              <div className="text-center">
                <p className="text-gray-500 mb-1">Nível Atual</p>
                <p className="text-3xl font-bold">{userPoints?.level || 1}</p>
              </div>
            </Card>
            <Card className="p-4">
              <div className="text-center">
                <p className="text-gray-500 mb-1">Sequência Atual</p>
                <p className="text-3xl font-bold">{getDailyStreak()} dias</p>
              </div>
            </Card>
          </div>
        </section>

        {/* Seção de conquistas */}
        <section>
          <h2 className="text-2xl font-bold mb-4">Minhas Conquistas</h2>
          <AchievementsList />
        </section>

        {/* Histórico de atividades */}
        <section>
          <h2 className="text-2xl font-bold mb-4">Histórico de Atividades</h2>
          <PointTransactionList 
            transactions={[]} 
            isLoading={isLoading} 
            limit={10} 
          />
        </section>
      </div>
    </Container>
  );
};

export default GamificationProfilePage;