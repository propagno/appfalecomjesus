import React, { useState } from 'react';
import { useChatContext } from '../contexts/ChatContext';

interface AdRewardPromptProps {
  onUpgradeClick?: () => void;
}

/**
 * Componente para exibir opções quando o usuário atinge o limite de mensagens
 */
const AdRewardPrompt: React.FC<AdRewardPromptProps> = ({ onUpgradeClick }) => {
  const { messageLimitInfo, watchAd, isWatchingAd } = useChatContext();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [rewardAmount, setRewardAmount] = useState(0);
  
  // Verificar se é necessário mostrar este componente
  if (!messageLimitInfo || messageLimitInfo.isPremium || messageLimitInfo.remaining > 0) {
    return null;
  }
  
  // Função para lidar com o clique no botão de assistir anúncio
  const handleWatchAd = async () => {
    if (isWatchingAd) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Normalmente, aqui seria exibido o anúncio real com SDK próprio
      // Nesta implementação, apenas fazemos a chamada de API
      const result = await watchAd();
      
      if (result.success && result.reward) {
        setSuccess(true);
        setRewardAmount(result.reward.value);
        
        // Reset após 5 segundos
        setTimeout(() => {
          setSuccess(false);
          setRewardAmount(0);
        }, 5000);
      } else {
        setError(result.error || 'Não foi possível obter a recompensa. Tente novamente.');
      }
    } catch (err) {
      setError('Ocorreu um erro ao processar sua solicitação. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 my-4">
      <div className="flex flex-col items-center text-center">
        <div className="text-blue-600 mb-2">
          <svg 
            className="h-12 w-12 mx-auto" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={1.5} 
              d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" 
            />
          </svg>
        </div>
        
        <h3 className="text-lg font-medium text-gray-900 mb-1">
          Limite de mensagens atingido
        </h3>
        
        <p className="text-sm text-gray-600 mb-4">
          Você atingiu seu limite diário de mensagens gratuitas.
        </p>
        
        {error && (
          <div className="text-red-600 text-sm mb-4 p-2 bg-red-50 rounded w-full">
            {error}
          </div>
        )}
        
        {success ? (
          <div className="bg-green-100 text-green-800 p-3 rounded-lg mb-4 w-full">
            <p className="font-medium">Parabéns!</p>
            <p>Você ganhou mais {rewardAmount} mensagens.</p>
          </div>
        ) : (
          <div className="space-y-3 w-full">
            <button
              onClick={handleWatchAd}
              disabled={isLoading}
              className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 flex justify-center items-center"
            >
              {isLoading ? (
                <>
                  <span className="animate-spin h-5 w-5 mr-2 border-2 border-white border-t-transparent rounded-full" />
                  Processando...
                </>
              ) : (
                'Assistir anúncio para ganhar 5 mensagens'
              )}
            </button>
            
            {onUpgradeClick && (
              <button
                onClick={onUpgradeClick}
                className="w-full py-2 px-4 bg-white border border-blue-600 text-blue-600 hover:bg-blue-50 rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Fazer upgrade para Premium
              </button>
            )}
          </div>
        )}
        
        <p className="text-xs text-gray-500 mt-4">
          Seu limite será renovado automaticamente em {messageLimitInfo.resetDate}
        </p>
      </div>
    </div>
  );
};

export default AdRewardPrompt; 