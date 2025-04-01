import React, { useEffect, useState } from 'react';
import useMonetizationQuery from '../hooks/useMonetizationQuery';
import { 
  MonetizationState, 
  AdType,
  RewardType,
  AdRewardRequest,
  PlanType,
  SubscriptionStatus,
  Plan,
  UserSubscription,
  AdReward,
  PlanBenefit,
  AdRewardType,
  PaymentGateway
} from '../types';
import { useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import { MonetizationContext, MonetizationContextProps, defaultMonetizationState } from '../contexts/MonetizationContext';
import { MOCK_USER_SUBSCRIPTION, MOCK_AD_REWARDS, DEFAULT_FREE_LIMITS, MOCK_PLANS } from '../types/mocks';

// Props do Provider
interface MonetizationProviderProps {
  children: React.ReactNode;
}

/**
 * Provider para gerenciar dados de monetização e assinaturas
 * Item 10.7 - Integração com MS-Monetization
 */
export const MonetizationProvider: React.FC<MonetizationProviderProps> = ({ children }) => {
  const [state, setState] = useState<MonetizationState>(defaultMonetizationState);
  const queryClient = useQueryClient();
  
  const {
    // Queries
    usePlansQuery,
    useUserSubscriptionQuery,
    useUserLimitsQuery,
    useAdRewardsHistoryQuery,
    
    // Mutations
    useRegisterAdRewardMutation,
    useCreateCheckoutMutation,
    useCancelSubscriptionMutation,
    useReactivateSubscriptionMutation,
    
    // Helpers
    refreshMonetizationData
  } = useMonetizationQuery();
  
  // Carregar dados
  const { data: plans, isLoading: isLoadingPlans, error: plansError } = usePlansQuery();
  const { data: subscription, isLoading: isLoadingSubscription, error: subscriptionError } = useUserSubscriptionQuery();
  const { data: limits, isLoading: isLoadingLimits, error: limitsError } = useUserLimitsQuery();
  const { data: adRewards, isLoading: isLoadingAdRewards, error: adRewardsError } = useAdRewardsHistoryQuery();
  
  // Mutations
  const registerAdRewardMutation = useRegisterAdRewardMutation();
  const createCheckoutMutation = useCreateCheckoutMutation();
  const cancelSubscriptionMutation = useCancelSubscriptionMutation();
  const reactivateSubscriptionMutation = useReactivateSubscriptionMutation();
  
  // Atualizar estado quando os dados mudarem
  useEffect(() => {
    setState(prevState => ({
      ...prevState,
      userSubscription: subscription || null,
      userLimits: limits || null,
      availablePlans: plans || [],
      adRewards: adRewards || [],
      isLoading: isLoadingPlans || isLoadingSubscription || isLoadingLimits || isLoadingAdRewards,
      error: plansError || subscriptionError || limitsError || adRewardsError,
    }));
  }, [
    plans, subscription, limits, adRewards,
    isLoadingPlans, isLoadingSubscription, isLoadingLimits, isLoadingAdRewards,
    plansError, subscriptionError, limitsError, adRewardsError
  ]);
  
  /**
   * Verifica se o usuário possui assinatura premium
   */
  const isPremium = (): boolean => {
    if (state.userLimits?.is_premium) return true;
    if (state.userSubscription?.status === 'active' || state.userSubscription?.status === 'trial') return true;
    return false;
  };
  
  /**
   * Verifica se o usuário atingiu o limite de mensagens de chat
   */
  const hasReachedChatLimit = (): boolean => {
    if (isPremium()) return false;
    if (!state.userLimits) return false;
    return state.userLimits.chat_messages_used >= state.userLimits.chat_messages_limit;
  };
  
  /**
   * Verifica se o usuário atingiu o limite de estudos
   */
  const hasReachedStudyLimit = (): boolean => {
    if (isPremium()) return false;
    if (!state.userLimits) return false;
    return state.userLimits.studies_used >= state.userLimits.studies_limit;
  };
  
  /**
   * Registra uma recompensa por assistir anúncio
   */
  const registerAdReward = async (adType: AdType, rewardType: RewardType): Promise<void> => {
    try {
      const request: AdRewardRequest = { ad_type: adType, reward_type: rewardType };
      const response = await registerAdRewardMutation.mutateAsync(request);
      
      // Atualizar o estado após receber a recompensa
      if (response.success) {
        setState(prev => ({
          ...prev,
          userLimits: response.new_limits,
          adRewards: [response.reward, ...(prev.adRewards || [])].slice(0, 20)
        }));
        
        // Notificar usuário
        const rewardText = rewardType === RewardType.CHAT_MESSAGES 
          ? `${response.reward.reward_amount} mensagens de chat` 
          : rewardType === RewardType.STUDY_ACCESS
            ? `${response.reward.reward_amount} dias de acesso aos estudos`
            : `${response.reward.reward_amount} dias de Premium`;
        
        toast.success(`Recompensa adicionada: ${rewardText}`, {
          position: "top-right",
          autoClose: 5000,
        });
      }
    } catch (error) {
      console.error('Erro ao registrar recompensa de anúncio:', error);
      toast.error('Não foi possível registrar a recompensa.', {
        position: "top-right",
        autoClose: 5000,
      });
      throw error;
    }
  };
  
  /**
   * Inicia o checkout para assinatura
   */
  const initiateCheckout = async (planId: string, couponCode?: string): Promise<string> => {
    try {
      const request = {
        plan_id: planId,
        coupon_code: couponCode,
        success_url: `${window.location.origin}/checkout/success`,
        cancel_url: `${window.location.origin}/checkout/cancel`
      };
      
      const response = await createCheckoutMutation.mutateAsync(request);
      return response.checkout_url;
    } catch (error) {
      console.error('Erro ao iniciar checkout:', error);
      toast.error('Não foi possível iniciar o processo de assinatura.', {
        position: "top-right",
        autoClose: 5000,
      });
      throw error;
    }
  };
  
  /**
   * Cancela uma assinatura
   */
  const cancelSubscription = async (subscriptionId: string): Promise<void> => {
    try {
      await cancelSubscriptionMutation.mutateAsync(subscriptionId);
      toast.success('Assinatura cancelada com sucesso.', {
        position: "top-right",
        autoClose: 5000,
      });
    } catch (error) {
      console.error('Erro ao cancelar assinatura:', error);
      toast.error('Não foi possível cancelar a assinatura.', {
        position: "top-right",
        autoClose: 5000,
      });
      throw error;
    }
  };
  
  /**
   * Reativa uma assinatura
   */
  const reactivateSubscription = async (subscriptionId: string): Promise<void> => {
    try {
      await reactivateSubscriptionMutation.mutateAsync(subscriptionId);
      toast.success('Assinatura reativada com sucesso.', {
        position: "top-right",
        autoClose: 5000,
      });
    } catch (error) {
      console.error('Erro ao reativar assinatura:', error);
      toast.error('Não foi possível reativar a assinatura.', {
        position: "top-right",
        autoClose: 5000,
      });
      throw error;
    }
  };
  
  // Valor do contexto
  const contextValue: MonetizationContextProps = {
    state,
    isPremium: isPremium(),
    hasReachedChatLimit: hasReachedChatLimit(),
    hasReachedStudyLimit: hasReachedStudyLimit(),
    registerAdReward,
    initiateCheckout,
    cancelSubscription,
    reactivateSubscription,
    refreshMonetizationData,
  };
  
  return (
    <MonetizationContext.Provider value={contextValue}>
      {children}
    </MonetizationContext.Provider>
  );
};

export default MonetizationProvider; 