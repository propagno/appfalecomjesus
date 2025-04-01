import React, { useState } from 'react';
import { useMonetization } from '../hooks/useMonetization';
import { RewardType } from '../types';

interface AdRewardCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  rewardType: RewardType;
  buttonText: string;
}

/**
 * Componente que exibe um card para assistir anúncios e receber recompensas
 */
const AdRewardCard: React.FC<AdRewardCardProps> = ({
  title,
  description,
  icon,
  rewardType,
  buttonText
}) => {
  const { watchAdForReward, isPremium, checkRewardAvailability } = useMonetization();
  const [isLoading, setIsLoading] = useState(false);
  const [lastReward, setLastReward] = useState<string | null>(null);

  const handleWatchAd = async () => {
    if (isPremium) {
      alert('Usuários premium não precisam assistir anúncios para receber recompensas.');
      return;
    }

    try {
      setIsLoading(true);
      await watchAdForReward(rewardType);
      setLastReward(new Date().toLocaleString());
    } catch (error) {
      console.error('Erro ao assistir anúncio:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isPremium) {
    return null; // Não mostrar para usuários premium
  }

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
      <div className="p-5">
        <div className="flex items-center mb-4">
          <div className="bg-primary-light p-3 rounded-full mr-4 text-primary">
            {icon || (
              <svg className="w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            )}
          </div>
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        
        <p className="text-gray-600 mb-6">{description}</p>
        
        <button
          onClick={handleWatchAd}
          disabled={isLoading}
          className="w-full py-2 px-4 bg-primary text-white rounded-lg font-medium 
                    hover:bg-primary-dark transition-colors flex justify-center items-center"
        >
          {isLoading ? (
            <>
              <span className="animate-spin h-5 w-5 mr-2 border-t-2 border-b-2 border-white rounded-full"></span>
              Carregando anúncio...
            </>
          ) : (
            buttonText
          )}
        </button>
        
        {lastReward && (
          <p className="text-xs text-gray-500 mt-3 text-center">
            Última recompensa: {lastReward}
          </p>
        )}
        
        {checkRewardAvailability(rewardType) && (
          <p className="text-xs text-green-600 mt-2 text-center font-medium">
            Você já tem recompensas disponíveis para usar!
          </p>
        )}
      </div>
    </div>
  );
};

export default AdRewardCard; 