import React, { useState } from 'react';
import { Card } from '../../../components/ui/card';
import { UserAchievement, Achievement } from '../types';
import { useGamification } from '../contexts/GamificationContext';

export interface AchievementGridProps {
  achievements: UserAchievement[];
  isLoading?: boolean;
  className?: string;
}

const AchievementGrid: React.FC<AchievementGridProps> = ({
  achievements,
  isLoading = false,
  className = ''
}) => {
  const { achievements: allAchievements } = useGamification();
  const [filter, setFilter] = useState<string>('all');
  
  // Renderiza o ícone da conquista
  const renderIcon = (achievement: Achievement) => (
    <div className="bg-blue-100 p-2 rounded-full">
      <img 
        src={achievement.icon_url || '/icons/achievement-default.svg'} 
        alt={achievement.name}
        className="w-10 h-10"
      />
    </div>
  );
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="p-4 animate-pulse">
            <div className="flex items-center mb-3">
              <div className="w-12 h-12 rounded-full bg-gray-200"></div>
              <div className="ml-3 w-3/4">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
            <div className="h-10 bg-gray-200 rounded w-full"></div>
          </Card>
        ))}
      </div>
    );
  }
  
  if (achievements.length === 0) {
    return (
      <Card className="p-6 text-center">
        <p className="text-gray-600">
          Você ainda não desbloqueou nenhuma conquista. Continue sua jornada espiritual para ganhar conquistas!
        </p>
      </Card>
    );
  }

  // Filtrar conquistas por categoria
  const filteredAchievements = filter === 'all' 
    ? achievements 
    : achievements.filter(a => a.achievement.category === filter);

  // Obter categorias únicas para o filtro
  const uniqueCategories = Array.from(
    new Set(achievements.map(a => a.achievement.category))
  );
  const categories = ['all', ...uniqueCategories];

  const getAchievementDetails = (userAchievement: UserAchievement): Achievement | undefined => {
    return allAchievements.find(a => a.id === userAchievement.achievement_id);
  };

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="flex flex-wrap gap-2 mb-4">
        {categories.map(category => (
          <button
            key={category}
            onClick={() => setFilter(category)}
            className={`px-3 py-1 text-sm rounded-full ${
              filter === category 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {category === 'all' ? 'Todas' : category.charAt(0).toUpperCase() + category.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredAchievements.map((userAchievement) => {
          const achievement = getAchievementDetails(userAchievement);
          if (!achievement) return null;
          
          return (
            <Card key={userAchievement.id} className="p-4 flex flex-col">
              <div className="flex items-center">
                {renderIcon(achievement)}
                <div className="ml-3">
                  <h4 className="font-medium">{achievement.name}</h4>
                  {userAchievement && (
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(userAchievement.earned_at).toLocaleDateString()}
                    </div>
                  )}
                </div>
              </div>
              <div className="mt-2 flex justify-between items-center">
                <div className="bg-amber-50 text-amber-800 text-xs px-2 py-1 rounded">
                  {achievement.category}
                </div>
                {userAchievement && (
                  <div className="text-green-600 text-xs font-medium">
                    +{achievement.points_reward} pontos
                  </div>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default AchievementGrid; 