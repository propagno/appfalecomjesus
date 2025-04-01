import { useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import monetizationService from '../api/monetizationService';
import {
  Plan,
  UserSubscription,
  UserLimits,
  AdReward,
  RewardType,
  AdType,
  CheckoutResponse,
  MonetizationState
} from '../types';

/**
 * Hook to manage monetization state and operations
 */
export const useMonetization = () => {
  const queryClient = useQueryClient();

  // Queries to fetch data
  const {
    data: plans,
    isLoading: isLoadingPlans,
    error: plansError
  } = useQuery({
    queryKey: ['monetization-plans'],
    queryFn: monetizationService.getPlans,
    staleTime: 60 * 60 * 1000, // 1 hour
  });

  const {
    data: subscription,
    isLoading: isLoadingSubscription,
    error: subscriptionError
  } = useQuery({
    queryKey: ['monetization-subscription'],
    queryFn: monetizationService.getUserSubscription,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const {
    data: limits,
    isLoading: isLoadingLimits,
    error: limitsError
  } = useQuery({
    queryKey: ['monetization-limits'],
    queryFn: monetizationService.getUserLimits,
    staleTime: 1 * 60 * 1000, // 1 minute
  });

  const {
    data: adRewards,
    isLoading: isLoadingAdRewards,
    error: adRewardsError
  } = useQuery({
    queryKey: ['monetization-ad-rewards'],
    queryFn: monetizationService.getAdRewardsHistory,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Determine the current plan based on subscription
  const currentPlan = plans?.find(plan => 
    plan.id === subscription?.plan_id
  ) || plans?.find(plan => plan.type === 'free') || null;

  // Mutations
  const registerAdRewardMutation = useMutation({
    mutationFn: ({ adType, rewardType }: { adType: AdType; rewardType: RewardType }) => 
      monetizationService.registerAdReward({ ad_type: adType, reward_type: rewardType }),
    onSuccess: (data) => {
      // Invalidate queries to reload the data
      queryClient.invalidateQueries({ queryKey: ['monetization-limits'] });
      queryClient.invalidateQueries({ queryKey: ['monetization-ad-rewards'] });
      
      // Show success message
      toast.success(`Recompensa obtida: +${data.reward.reward_amount} ${
        data.reward.reward_type === 'chat_messages' ? 'mensagens' : 'dias de estudo'
      }`);
    },
    onError: (error) => {
      toast.error('Erro ao registrar recompensa do anúncio');
      console.error('Erro ao registrar recompensa:', error);
    },
  });

  const upgradePlanMutation = useMutation({
    mutationFn: (planId: string) => monetizationService.createCheckout({ 
      plan_id: planId,
      success_url: window.location.origin + '/monetization/success',
      cancel_url: window.location.origin + '/monetization/cancel'
    }),
    onSuccess: (checkoutResponse: CheckoutResponse) => {
      // If there's a redirect URL, open it in a new tab
      if (checkoutResponse.checkout_url) {
        window.open(checkoutResponse.checkout_url, '_blank');
      }
      // Show success message
      toast.success('Redirecionando para o pagamento');
    },
    onError: (error) => {
      toast.error('Erro ao iniciar o processo de upgrade');
      console.error('Erro ao iniciar pagamento:', error);
    },
  });

  const cancelSubscriptionMutation = useMutation({
    mutationFn: (subscriptionId: string) => monetizationService.cancelSubscription(subscriptionId),
    onSuccess: () => {
      // Invalidate subscription query to reload the data
      queryClient.invalidateQueries({ queryKey: ['monetization-subscription'] });
      
      // Show success message
      toast.success('Assinatura cancelada com sucesso');
    },
    onError: (error) => {
      toast.error('Erro ao cancelar assinatura');
      console.error('Erro ao cancelar assinatura:', error);
    },
  });

  // Check if user is on free plan
  const isFreePlan = currentPlan?.type === 'free';

  // Check if user has premium features
  const isPremium = subscription?.status === 'active' && subscription?.plan_type !== 'free';

  // Actions
  const watchAd = useCallback((adType: AdType, rewardType: RewardType) => {
    registerAdRewardMutation.mutate({ adType, rewardType });
  }, [registerAdRewardMutation]);

  // Adicionado para compatibilidade com MonetizationContextType
  const watchAdForReward = useCallback((rewardType: RewardType) => {
    return registerAdRewardMutation.mutateAsync({ adType: AdType.VIDEO, rewardType });
  }, [registerAdRewardMutation]);

  const upgradePlan = useCallback((planId: string): Promise<CheckoutResponse> => {
    return upgradePlanMutation.mutateAsync(planId);
  }, [upgradePlanMutation]);

  const cancelSubscription = useCallback(() => {
    // Só podemos cancelar se tivermos uma assinatura ativa
    if (subscription?.id) {
      return cancelSubscriptionMutation.mutateAsync(subscription.id);
    }
    return Promise.resolve({ success: false, message: 'Nenhuma assinatura ativa' });
  }, [cancelSubscriptionMutation, subscription]);

  // Adicionado para compatibilidade com MonetizationContextType
  const checkRewardAvailability = useCallback((rewardType: RewardType): boolean => {
    // Verificar se há recompensas disponíveis do tipo solicitado
    return Array.isArray(adRewards) && adRewards.some(reward => 
      reward.reward_type === rewardType
    );
  }, [adRewards]);

  // Create state object
  const state: MonetizationState = {
    userSubscription: subscription || null,
    userLimits: limits || null,
    availablePlans: plans || [],
    adRewards: adRewards || [],
    isLoading: isLoadingPlans || isLoadingSubscription || isLoadingLimits || isLoadingAdRewards,
    error: plansError?.message || subscriptionError?.message || limitsError?.message || adRewardsError?.message || null,
  };

  return {
    ...state,
    watchAd,
    watchAdForReward,
    upgradePlan,
    cancelSubscription,
    checkRewardAvailability,
    isFreePlan,
    isPremium,
    isRegisteringAdReward: registerAdRewardMutation.isPending,
    isUpgradingPlan: upgradePlanMutation.isPending,
    isCancelingSubscription: cancelSubscriptionMutation.isPending,
  };
}; 