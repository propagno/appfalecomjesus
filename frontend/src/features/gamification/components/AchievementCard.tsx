import React from 'react';
import { Achievement, UserAchievement } from '../types';
import { cn } from '../../../lib/utils';

// Função local para formatação de data
const formatDate = (date: Date | string): string => {
  if (!date) return '';
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  });
};

interface AchievementCardProps {
  achievement: Achievement;
  userAchievement?: UserAchievement;
  onClick?: () => void;
  className?: string;
}

const AchievementCard: React.FC<AchievementCardProps> = ({
  achievement,
  userAchievement,
  onClick,
  className,
}) => {
  const isUnlocked = !!userAchievement;
  
  // Se a conquista está desbloqueada, use os dados do usuário
  const displayAchievement = userAchievement?.achievement || achievement;
  
  return (
    <div
      className={cn(
        'relative flex flex-col rounded-lg overflow-hidden border shadow-sm',
        isUnlocked ? 'bg-white border-amber-300' : 'bg-gray-100 border-gray-200',
        onClick && 'cursor-pointer hover:shadow-md transition-shadow',
        className
      )}
      onClick={onClick}
    >
      {/* Indicador de Status */}
      {isUnlocked && (
        <div className="absolute top-2 right-2 z-10">
          <div className="bg-amber-500 text-white text-xs px-2 py-1 rounded-full shadow-sm">
            Desbloqueado
          </div>
        </div>
      )}
      
      {/* Imagem/Ícone */}
      <div className={cn(
        'h-32 flex items-center justify-center p-4',
        isUnlocked ? 'bg-amber-50' : 'bg-gray-50'
      )}>
        {displayAchievement.icon_url ? (
          <img
            src={displayAchievement.icon_url}
            alt={displayAchievement.name}
            className={cn(
              'h-20 w-20 object-contain',
              !isUnlocked && 'opacity-40 grayscale'
            )}
          />
        ) : (
          <div className={cn(
            'h-20 w-20 rounded-full flex items-center justify-center bg-amber-100',
            !isUnlocked && 'opacity-40 bg-gray-200'
          )}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
            </svg>
          </div>
        )}
      </div>
      
      {/* Conteúdo */}
      <div className="p-4 flex-1 flex flex-col">
        <h3 className={cn(
          'text-lg font-semibold mb-1',
          isUnlocked ? 'text-amber-800' : 'text-gray-500'
        )}>
          {displayAchievement.name}
        </h3>
        
        <p className={cn(
          'text-sm mb-3 flex-1',
          isUnlocked ? 'text-gray-600' : 'text-gray-400'
        )}>
          {displayAchievement.description}
        </p>
        
        {/* Pontos e Data */}
        <div className="flex justify-between items-center mt-2 text-xs">
          <div className={cn(
            'font-semibold',
            isUnlocked ? 'text-amber-700' : 'text-gray-400'
          )}>
            +{displayAchievement.points_reward} pontos
          </div>
          
          {isUnlocked && userAchievement?.earned_at && (
            <div className="text-gray-500">
              {formatDate(userAchievement.earned_at)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AchievementCard; 