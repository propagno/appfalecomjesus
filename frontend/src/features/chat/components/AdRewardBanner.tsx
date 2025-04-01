import React from 'react';
import { VideoIcon, Gift } from 'lucide-react';

interface AdRewardBannerProps {
  isVisible: boolean;
  onWatchAd: () => void;
  reward: number;
  isLoading?: boolean;
}

/**
 * Componente que exibe um banner para assistir anúncios e ganhar mais mensagens (plano gratuito)
 */
export const AdRewardBanner: React.FC<AdRewardBannerProps> = ({
  isVisible,
  onWatchAd,
  reward,
  isLoading = false,
}) => {
  if (!isVisible) return null;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 my-4 animate-fadeIn">
      <div className="flex flex-col md:flex-row items-center justify-between">
        <div className="flex items-center mb-3 md:mb-0">
          <Gift className="text-blue-500 mr-3" size={24} />
          <div>
            <h3 className="font-semibold text-blue-700">Limite de mensagens atingido</h3>
            <p className="text-sm text-blue-600">
              Assista a um anúncio para receber mais {reward} mensagens.
            </p>
          </div>
        </div>
        
        <button
          onClick={onWatchAd}
          disabled={isLoading}
          className={`flex items-center px-4 py-2 rounded-lg text-white transition-colors ${
            isLoading 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          <VideoIcon size={16} className="mr-2" />
          {isLoading ? 'Carregando...' : 'Assistir anúncio'}
        </button>
      </div>
      
      <div className="text-xs text-blue-500 mt-2 text-center md:text-right">
        Ou <a href="/planos" className="underline font-medium">faça upgrade</a> para mensagens ilimitadas.
      </div>
    </div>
  );
};

export default AdRewardBanner; 