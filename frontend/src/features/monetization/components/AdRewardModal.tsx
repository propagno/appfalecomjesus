import React, { useState } from 'react';
import { AdType, RewardType } from '../types';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import { Button } from '../../../shared/components/ui/Button';

interface AdRewardModalProps {
  isOpen: boolean;
  onClose: () => void;
  rewardType: RewardType;
  onSuccess?: () => void;
}

/**
 * Modal para visualização de anúncios para ganhar recompensas
 * no plano gratuito
 */
const AdRewardModal: React.FC<AdRewardModalProps> = ({
  isOpen,
  onClose,
  rewardType,
  onSuccess
}) => {
  const { registerAdReward } = useMonetizationContext();
  const [loading, setLoading] = useState(false);
  const [adCompleted, setAdCompleted] = useState(false);
  
  // Simula a visualização de um anúncio
  const simulateAdView = () => {
    setLoading(true);
    
    // Simulação de carregamento e visualização do anúncio
    setTimeout(() => {
      setLoading(false);
      setAdCompleted(true);
    }, 3000);
  };
  
  // Registra a recompensa após visualizar o anúncio
  const handleClaimReward = async () => {
    try {
      setLoading(true);
      await registerAdReward(AdType.VIDEO, rewardType);
      
      if (onSuccess) {
        onSuccess();
      }
      
      onClose();
    } catch (error) {
      console.error('Erro ao registrar recompensa:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Reset do estado ao fechar
  const handleClose = () => {
    setAdCompleted(false);
    onClose();
  };
  
  // Determinar texto baseado no tipo de recompensa
  const getRewardText = () => {
    switch (rewardType) {
      case RewardType.CHAT_MESSAGES:
        return '+5 mensagens no chat';
      case RewardType.STUDY_ACCESS:
        return '+1 dia de acesso a estudos';
      case RewardType.PREMIUM_DAYS:
        return '+1 dia de acesso Premium';
      default:
        return 'recompensa';
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
        <div className="p-6">
          <h2 className="text-xl font-semibold mb-4">
            Ganhe {getRewardText()}
          </h2>
          
          {!adCompleted ? (
            <>
              <p className="mb-6 text-gray-700">
                Assista a um anúncio curto para ganhar {getRewardText()} e continuar sua jornada espiritual.
              </p>
              
              <div className="flex justify-center mb-6">
                <div className="w-full h-40 bg-gray-200 rounded flex items-center justify-center">
                  {loading ? (
                    <div className="animate-spin h-8 w-8 border-4 border-indigo-500 rounded-full border-t-transparent"></div>
                  ) : (
                    <button
                      onClick={simulateAdView}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                    >
                      Assistir Anúncio
                    </button>
                  )}
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center justify-center mb-6 p-4 bg-green-50 rounded-lg">
                <div className="flex flex-col items-center">
                  <svg
                    className="w-12 h-12 text-green-500 mb-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p className="text-center text-green-700 font-medium">
                    Anúncio visualizado com sucesso!
                  </p>
                  <p className="text-center text-gray-600 mt-1">
                    Clique abaixo para receber sua recompensa
                  </p>
                </div>
              </div>
            </>
          )}
          
          <div className="flex justify-end space-x-3">
            <Button
              variant="outline"
              onClick={handleClose}
              disabled={loading}
            >
              Cancelar
            </Button>
            
            {adCompleted && (
              <Button
                variant="primary"
                onClick={handleClaimReward}
                loading={loading}
              >
                Receber Recompensa
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdRewardModal; 