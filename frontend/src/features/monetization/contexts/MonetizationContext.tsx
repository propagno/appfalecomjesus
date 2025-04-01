import React, { createContext, useContext } from 'react';
import { 
  Plan, 
  UserSubscription, 
  AdReward, 
  PlanBenefit, 
  AdRewardType, 
  PlanType,
  SubscriptionStatus,
  MonetizationContextType,
  RewardType,
  PaymentGateway,
  AdType,
  MonetizationState
} from '../types';
import { MOCK_USER_SUBSCRIPTION, MOCK_AD_REWARDS, DEFAULT_FREE_LIMITS, MOCK_PLANS } from '../types/mocks';

// Valor padrão para o contexto de monetização
export const defaultMonetizationState: MonetizationState = {
  userSubscription: null,
  userLimits: null,
  availablePlans: [],
  adRewards: [],
  isLoading: false,
  error: null,
};

// Interface do contexto de monetização
export interface MonetizationContextProps {
  state: MonetizationState;
  isPremium: boolean;
  hasReachedChatLimit: boolean;
  hasReachedStudyLimit: boolean;
  registerAdReward: (adType: AdType, rewardType: RewardType) => Promise<void>;
  initiateCheckout: (planId: string, couponCode?: string) => Promise<string>;
  cancelSubscription: (subscriptionId: string) => Promise<void>;
  reactivateSubscription: (subscriptionId: string) => Promise<void>;
  refreshMonetizationData: () => void;
}

// Criação do contexto
export const MonetizationContext = createContext<MonetizationContextProps | undefined>(undefined);

/**
 * Hook para utilizar o contexto de monetização
 */
export const useMonetizationContext = () => {
  const context = useContext(MonetizationContext);
  
  if (context === undefined) {
    throw new Error('useMonetizationContext deve ser usado dentro de um MonetizationProvider');
  }
  
  return context;
}; 