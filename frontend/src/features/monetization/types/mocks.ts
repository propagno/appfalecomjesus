import { 
  AdReward, 
  RewardType, 
  AdType, 
  UserSubscription, 
  SubscriptionStatus, 
  PaymentGateway, 
  PlanType, 
  Plan,
  UserLimits
} from './index';

/**
 * Mock de assinatura do usuário para desenvolvimento
 */
export const MOCK_USER_SUBSCRIPTION: UserSubscription = {
  id: 'sub_123456',
  user_id: 'user_123',
  plan_id: 'plan_free',
  plan_type: PlanType.FREE,
  status: SubscriptionStatus.ACTIVE,
  payment_gateway: PaymentGateway.STRIPE,
  start_date: new Date('2023-01-01').toISOString(),
  end_date: new Date('2099-01-01').toISOString(),
  created_at: new Date('2023-01-01').toISOString(),
  updated_at: new Date('2023-01-01').toISOString()
};

/**
 * Mock de recompensas de anúncios para desenvolvimento
 */
export const MOCK_AD_REWARDS: AdReward[] = [
  {
    id: 'reward_1',
    user_id: 'user_123',
    ad_type: AdType.VIDEO,
    reward_type: RewardType.CHAT_MESSAGES,
    reward_amount: 5,
    created_at: new Date('2023-05-15T10:30:00').toISOString()
  },
  {
    id: 'reward_2',
    user_id: 'user_123',
    ad_type: AdType.VIDEO,
    reward_type: RewardType.STUDY_ACCESS,
    reward_amount: 1,
    created_at: new Date('2023-05-14T15:45:00').toISOString()
  }
];

/**
 * Mock de planos disponíveis para desenvolvimento
 */
export const MOCK_PLANS: Plan[] = [
  {
    id: 'plan_free',
    type: PlanType.FREE,
    name: 'Plano Gratuito',
    description: 'Acesso básico à plataforma com recursos limitados.',
    price: 0,
    currency: 'BRL',
    billing_interval: 'monthly',
    features: ['5 mensagens diárias no chat IA', '10 dias de estudo por mês'],
    created_at: new Date('2023-01-01').toISOString(),
    updated_at: new Date('2023-01-01').toISOString()
  },
  {
    id: 'plan_premium_monthly',
    type: PlanType.PREMIUM,
    name: 'Plano Premium Mensal',
    description: 'Acesso completo à plataforma com chat IA ilimitado.',
    price: 19.90,
    currency: 'BRL',
    billing_interval: 'monthly',
    features: [
      'Chat IA ilimitado', 
      'Estudos ilimitados', 
      'Sem anúncios', 
      'Conteúdos exclusivos',
      'Suporte prioritário'
    ],
    recommended: true,
    created_at: new Date('2023-01-01').toISOString(),
    updated_at: new Date('2023-01-01').toISOString()
  },
  {
    id: 'plan_premium_annual',
    type: PlanType.PREMIUM_ANNUAL,
    name: 'Plano Premium Anual',
    description: 'Acesso completo à plataforma com desconto de 20%.',
    price: 191.90,
    currency: 'BRL',
    billing_interval: 'yearly',
    features: [
      'Chat IA ilimitado', 
      'Estudos ilimitados', 
      'Sem anúncios', 
      'Conteúdos exclusivos',
      'Suporte prioritário',
      'Desconto de 20% em relação ao plano mensal'
    ],
    created_at: new Date('2023-01-01').toISOString(),
    updated_at: new Date('2023-01-01').toISOString()
  }
];

/**
 * Mock de limites do usuário para desenvolvimento
 */
export const MOCK_USER_LIMITS: UserLimits = {
  user_id: 'user_123',
  is_premium: false,
  chat_messages_used: 2,
  chat_messages_limit: 5,
  studies_used: 3,
  studies_limit: 10,
  reset_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // Amanhã
};

/**
 * Valores padrão para limites de uso no plano gratuito
 */
export const DEFAULT_FREE_LIMITS = {
  dailyChatMessages: 5,
  monthlyStudies: 10
}; 