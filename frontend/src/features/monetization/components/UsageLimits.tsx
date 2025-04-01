import React, { useState } from 'react';
import { MessageCircle, Calendar, AlertCircle } from 'lucide-react';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import AdRewardModal from './AdRewardModal';
import { AdRewardType, RewardType } from '../types';

/**
 * Component that displays the user's current usage limits and remaining quota
 */
export const UsageLimits: React.FC = () => {
  const { state, isPremium, hasReachedChatLimit, hasReachedStudyLimit } = useMonetizationContext();
  const { userLimits } = state;
  const isFreePlan = !isPremium;
  
  const [adModalOpen, setAdModalOpen] = useState(false);
  const [rewardType, setRewardType] = useState<RewardType>(RewardType.CHAT_MESSAGES);

  // Handle opening the ad modal
  const handleWatchAd = (type: RewardType) => {
    setRewardType(type);
    setAdModalOpen(true);
  };

  if (!userLimits) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-12 bg-gray-200 rounded mb-6"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-12 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {/* Header */}
        <div className="bg-blue-600 text-white p-4">
          <h3 className="font-semibold text-lg">Limites de Uso</h3>
          <p className="text-sm text-blue-100">
            {isPremium 
              ? 'Aproveite seu acesso ilimitado!' 
              : 'Veja seus limites restantes no plano gratuito'}
          </p>
        </div>
        
        {/* Chat limits */}
        <div className="p-4 border-b border-gray-100">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <MessageCircle className="h-5 w-5 text-blue-500 mr-2" />
              <span className="text-gray-700 font-medium">Chat IA</span>
            </div>
            {isFreePlan && (
              <button
                onClick={() => handleWatchAd(RewardType.CHAT_MESSAGES)}
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
              >
                + Ganhar mensagens
              </button>
            )}
          </div>
          
          {isPremium ? (
            <div className="text-green-600 font-medium">Mensagens ilimitadas</div>
          ) : (
            <>
              <div className="h-2 bg-gray-200 rounded-full mb-2">
                <div
                  className="h-full bg-blue-500 rounded-full"
                  style={{
                    width: `${((userLimits.chat_messages_limit - userLimits.chat_messages_used) / userLimits.chat_messages_limit) * 100}%`,
                  }}
                ></div>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">
                  {userLimits.chat_messages_limit - userLimits.chat_messages_used} de {userLimits.chat_messages_limit} mensagens restantes
                </span>
                <span className="text-gray-500">Reseta em: {new Date(userLimits.reset_date).toLocaleDateString()}</span>
              </div>
            </>
          )}
        </div>
        
        {/* Study days limits */}
        <div className="p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 text-blue-500 mr-2" />
              <span className="text-gray-700 font-medium">Estudos</span>
            </div>
            {isFreePlan && (
              <button
                onClick={() => handleWatchAd(RewardType.STUDY_ACCESS)}
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
              >
                + Ganhar dias
              </button>
            )}
          </div>
          
          {isPremium ? (
            <div className="text-green-600 font-medium">Estudos ilimitados</div>
          ) : (
            <>
              <div className="h-2 bg-gray-200 rounded-full mb-2">
                <div
                  className="h-full bg-blue-500 rounded-full"
                  style={{
                    width: `${((userLimits.studies_limit - userLimits.studies_used) / userLimits.studies_limit) * 100}%`,
                  }}
                ></div>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">
                  {userLimits.studies_limit - userLimits.studies_used} de {userLimits.studies_limit} dias restantes
                </span>
                <span className="text-gray-500">Reseta em: {new Date(userLimits.reset_date).toLocaleDateString()}</span>
              </div>
            </>
          )}
        </div>
        
        {/* Upgrade prompt for free users */}
        {isFreePlan && (
          <div className="p-4 bg-gray-50 border-t border-gray-100 flex items-start">
            <AlertCircle className="h-5 w-5 text-blue-500 mr-2 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-gray-600">
              Faça upgrade para o plano Premium para obter acesso ilimitado a todas as funcionalidades do aplicativo.
            </p>
          </div>
        )}
      </div>
      
      {/* Ad reward modal */}
      <AdRewardModal
        isOpen={adModalOpen}
        onClose={() => setAdModalOpen(false)}
        rewardType={rewardType}
        onSuccess={() => {}} // Adicionar função de sucesso se necessário
      />
    </>
  );
};

export default UsageLimits; 