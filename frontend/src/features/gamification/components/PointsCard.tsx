import React from 'react';
import { Card } from '../../../components/ui/card';
import { ProgressBar } from './ProgressBar';
import { UserLevel } from '../types';

interface PointsCardProps {
  points: number;
  level: UserLevel | null;
  levelProgress: number;
  streak: number;
  isLoading?: boolean;
}

const PointsCard: React.FC<PointsCardProps> = ({
  points,
  level,
  levelProgress,
  streak,
  isLoading = false
}) => {
  if (isLoading) {
    return (
      <Card className="p-6 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-12 bg-gray-200 rounded-full w-1/2 mb-6"></div>
        <div className="h-4 bg-gray-200 rounded w-full mb-2.5"></div>
        <div className="h-4 bg-gray-200 rounded w-4/5"></div>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-4">
        <div>
          <h3 className="text-lg font-semibold mb-1">Seus Pontos Espirituais</h3>
          <p className="text-gray-600 text-sm">Continue sua jornada para ganhar mais</p>
        </div>
        <div className="mt-3 md:mt-0">
          <span className="text-3xl font-bold text-primary">{points}</span>
          <span className="text-sm text-gray-600 ml-1">pontos</span>
        </div>
      </div>

      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium">
            Nível {level?.level || 1}: {level?.name || 'Iniciante'}
          </span>
          <span className="text-sm font-medium">
            {levelProgress}%
          </span>
        </div>
        <ProgressBar progress={levelProgress} />
        <p className="text-xs text-gray-500 mt-1">
          {level && level.max_points < Number.MAX_SAFE_INTEGER 
            ? `Próximo nível em: ${level.max_points - points} pontos`
            : 'Você atingiu o nível máximo!'}
        </p>
      </div>

      <div className="flex items-center">
        <div className="bg-blue-100 text-blue-800 p-2 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
        </div>
        <div className="ml-3">
          <p className="font-medium">Sequência de {streak} dias</p>
          <p className="text-sm text-gray-600">Continue estudando para manter sua sequência</p>
        </div>
      </div>
    </Card>
  );
};

export default PointsCard; 