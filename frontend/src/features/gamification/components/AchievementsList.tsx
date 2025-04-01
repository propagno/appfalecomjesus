import React, { useState } from 'react';
import { useGamificationContext } from '../providers/GamificationProvider';
import { useEffect } from 'react';
import AchievementCard from './AchievementCard';
import { Search, Filter, Trophy } from 'lucide-react';

/**
 * Componente que lista as conquistas do usuário
 */
export const AchievementsList: React.FC = () => {
  const { state } = useGamificationContext();
  const { achievements } = state;
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Filtrar conquistas por categoria e termo de busca
  const filteredAchievements = achievements.filter(achievement => {
    // Filtrar por categoria
    const categoryMatch = filter === 'all' || achievement.category === filter;
    
    // Filtrar por termo de busca
    const searchMatch = searchTerm === '' || 
      achievement.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
      achievement.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    return categoryMatch && searchMatch;
  });

  // Obter lista de categorias únicas a partir das conquistas
  const categorySet = new Set(achievements.map(a => a.category));
  const categories = ['all', ...Array.from(categorySet)];

  // Calcular estatísticas
  const achievementStats = {
    total: achievements.length,
    available: 0, // Não há availableBadges no novo formato
    unlocked: achievements.length,
    completion: 0 // Não é possível calcular sem availableBadges
  };

  if (state.isLoading) {
    return (
      <div className="space-y-4">
        <div className="animate-pulse bg-white p-4 rounded-lg h-12"></div>
        <div className="animate-pulse bg-white p-6 rounded-lg h-40 mb-4"></div>
        <div className="animate-pulse bg-white p-6 rounded-lg h-40 mb-4"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Estatísticas */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{achievementStats.total}</div>
            <div className="text-sm text-gray-500">Total</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{achievementStats.unlocked}</div>
            <div className="text-sm text-gray-500">Desbloqueados</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{achievementStats.available}</div>
            <div className="text-sm text-gray-500">Disponíveis</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">{achievementStats.completion}%</div>
            <div className="text-sm text-gray-500">Completado</div>
          </div>
        </div>
      </div>
      
      {/* Filtros e busca */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Buscar conquistas..."
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <Filter className="h-5 w-5 text-gray-500" />
            <select
              className="border border-gray-300 rounded-md py-2 pl-2 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="all">Todas categorias</option>
              {categories.filter(c => c !== 'all').map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
        </div>
      </div>
      
      {/* Lista de conquistas */}
      {filteredAchievements.length > 0 ? (
        <div className="space-y-4">
          {filteredAchievements.map(achievement => (
            <AchievementCard
              key={achievement.id}
              achievement={achievement}
            />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <Trophy className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-1">Nenhuma conquista encontrada</h3>
          <p className="text-gray-500">
            {searchTerm || filter !== 'all'
              ? 'Tente ajustar seus filtros para ver mais resultados.'
              : 'Continue usando o aplicativo para desbloquear conquistas!'}
          </p>
        </div>
      )}
    </div>
  );
};

export default AchievementsList; 