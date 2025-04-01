import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { monetizationService } from '../api/monetizationService';
import {
  CheckoutRequest,
  AdRewardRequest,
  Plan,
  UserSubscription,
  UserLimits
} from '../types';

/**
 * Chaves para os queries relacionados à monetização
 */
export enum MonetizationQueryKeys {
  PLANS = 'plans',
  USER_SUBSCRIPTION = 'userSubscription',
  USER_LIMITS = 'userLimits',
  AD_REWARDS = 'adRewards',
  TRANSACTIONS = 'transactions',
}

/**
 * Hook que provê acesso aos dados de monetização via React Query
 */
export const useMonetizationQuery = () => {
  const queryClient = useQueryClient();

  // Query para obter os planos disponíveis
  const usePlansQuery = () =>
    useQuery({
      queryKey: [MonetizationQueryKeys.PLANS],
      queryFn: () => monetizationService.getPlans(),
      staleTime: 1000 * 60 * 60, // 1 hora - planos mudam raramente
    });

  // Query para obter um plano específico
  const usePlanQuery = (planId: string) =>
    useQuery({
      queryKey: [MonetizationQueryKeys.PLANS, planId],
      queryFn: () => monetizationService.getPlan(planId),
      enabled: !!planId,
      staleTime: 1000 * 60 * 60, // 1 hora
    });

  // Query para obter a assinatura do usuário
  const useUserSubscriptionQuery = () =>
    useQuery({
      queryKey: [MonetizationQueryKeys.USER_SUBSCRIPTION],
      queryFn: () => monetizationService.getUserSubscription(),
      staleTime: 1000 * 60 * 15, // 15 minutos
    });

  // Query para obter os limites do usuário
  const useUserLimitsQuery = () =>
    useQuery({
      queryKey: [MonetizationQueryKeys.USER_LIMITS],
      queryFn: () => monetizationService.getUserLimits(),
      staleTime: 1000 * 60 * 5, // 5 minutos - verificar com frequência
    });

  // Query para obter o histórico de recompensas de anúncios
  const useAdRewardsHistoryQuery = () =>
    useQuery({
      queryKey: [MonetizationQueryKeys.AD_REWARDS],
      queryFn: () => monetizationService.getAdRewardsHistory(),
      staleTime: 1000 * 60 * 10, // 10 minutos
    });

  // Query para obter o histórico de transações
  const useTransactionsHistoryQuery = () =>
    useQuery({
      queryKey: [MonetizationQueryKeys.TRANSACTIONS],
      queryFn: () => monetizationService.getTransactionsHistory(),
      staleTime: 1000 * 60 * 15, // 15 minutos
    });

  // Mutation para criar um checkout de assinatura
  const useCreateCheckoutMutation = () =>
    useMutation({
      mutationFn: (checkoutData: CheckoutRequest) =>
        monetizationService.createCheckout(checkoutData),
    });

  // Mutation para cancelar uma assinatura
  const useCancelSubscriptionMutation = () =>
    useMutation({
      mutationFn: (subscriptionId: string) =>
        monetizationService.cancelSubscription(subscriptionId),
      onSuccess: () => {
        // Invalidar cache da assinatura do usuário
        queryClient.invalidateQueries({
          queryKey: [MonetizationQueryKeys.USER_SUBSCRIPTION],
        });
      },
    });

  // Mutation para reativar uma assinatura
  const useReactivateSubscriptionMutation = () =>
    useMutation({
      mutationFn: (subscriptionId: string) =>
        monetizationService.reactivateSubscription(subscriptionId),
      onSuccess: () => {
        // Invalidar cache da assinatura do usuário
        queryClient.invalidateQueries({
          queryKey: [MonetizationQueryKeys.USER_SUBSCRIPTION],
        });
      },
    });

  // Mutation para registrar uma recompensa de anúncio
  const useRegisterAdRewardMutation = () =>
    useMutation({
      mutationFn: (adRewardData: AdRewardRequest) =>
        monetizationService.registerAdReward(adRewardData),
      onSuccess: () => {
        // Invalidar caches relevantes
        queryClient.invalidateQueries({
          queryKey: [MonetizationQueryKeys.USER_LIMITS],
        });
        queryClient.invalidateQueries({
          queryKey: [MonetizationQueryKeys.AD_REWARDS],
        });
      },
    });

  // Mutation para validar um cupom
  const useValidateCouponMutation = () =>
    useMutation({
      mutationFn: ({ code, planId }: { code: string; planId: string }) =>
        monetizationService.validateCoupon(code, planId),
    });

  // Forçar atualização de todos os dados de monetização
  const refreshMonetizationData = () => {
    queryClient.invalidateQueries({
      queryKey: [MonetizationQueryKeys.USER_SUBSCRIPTION],
    });
    queryClient.invalidateQueries({
      queryKey: [MonetizationQueryKeys.USER_LIMITS],
    });
    queryClient.invalidateQueries({
      queryKey: [MonetizationQueryKeys.AD_REWARDS],
    });
    queryClient.invalidateQueries({
      queryKey: [MonetizationQueryKeys.TRANSACTIONS],
    });
  };

  // Verificar se o usuário é premium
  const isPremium = (): boolean => {
    const subscription = queryClient.getQueryData<UserSubscription | null>([
      MonetizationQueryKeys.USER_SUBSCRIPTION,
    ]);
    const limits = queryClient.getQueryData<UserLimits>([
      MonetizationQueryKeys.USER_LIMITS,
    ]);

    // Verificar pelos limites (mais confiável)
    if (limits) {
      return limits.is_premium;
    }

    // Verificar pela assinatura
    if (subscription) {
      return subscription.status === 'active' || subscription.status === 'trial';
    }

    return false;
  };

  return {
    // Queries
    usePlansQuery,
    usePlanQuery,
    useUserSubscriptionQuery,
    useUserLimitsQuery,
    useAdRewardsHistoryQuery,
    useTransactionsHistoryQuery,

    // Mutations
    useCreateCheckoutMutation,
    useCancelSubscriptionMutation,
    useReactivateSubscriptionMutation,
    useRegisterAdRewardMutation,
    useValidateCouponMutation,

    // Helpers
    refreshMonetizationData,
    isPremium,
  };
};

export default useMonetizationQuery; 