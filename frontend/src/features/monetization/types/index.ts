/**
 * Enum para os tipos de planos disponíveis
 */
export enum PlanType {
  FREE = "free",
  PREMIUM = "premium",
  PREMIUM_ANNUAL = "premium_annual"
}

/**
 * Enum para os status de assinatura
 */
export enum SubscriptionStatus {
  ACTIVE = "active",
  CANCELED = "canceled",
  TRIAL = "trial",
  EXPIRED = "expired",
  PENDING = "pending"
}

/**
 * Enum para os tipos de pagamento
 */
export enum PaymentGateway {
  STRIPE = "stripe",
  HOTMART = "hotmart",
  PAYPAL = "paypal"
}

/**
 * Enum para os tipos de anúncios
 */
export enum AdType {
  VIDEO = "video",
  BANNER = "banner",
  INTERSTITIAL = "interstitial"
}

/**
 * Enum para os tipos de recompensas
 */
export enum RewardType {
  CHAT_MESSAGES = "chat_messages",
  STUDY_ACCESS = "study_access",
  PREMIUM_DAYS = "premium_days"
}

/**
 * Interface para planos de assinatura
 */
export interface Plan {
  id: string;
  type: PlanType;
  name: string;
  description: string;
  price: number;
  currency: string;
  billing_interval: 'monthly' | 'yearly' | 'one_time';
  features: string[];
  recommended?: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Interface para assinaturas do usuário
 */
export interface UserSubscription {
  id: string;
  user_id: string;
  plan_id: string;
  plan_type: PlanType;
  status: SubscriptionStatus;
  payment_gateway: PaymentGateway;
  start_date: string;
  end_date: string;
  trial_end_date?: string;
  canceled_at?: string;
  created_at: string;
  updated_at: string;
}

/**
 * Interface para recompensas de anúncios
 */
export interface AdReward {
  id: string;
  user_id: string;
  ad_type: AdType;
  reward_type: RewardType;
  reward_amount: number;
  created_at: string;
}

/**
 * Interface para limites do usuário
 */
export interface UserLimits {
  user_id: string;
  is_premium: boolean;
  chat_messages_used: number;
  chat_messages_limit: number;
  studies_used: number;
  studies_limit: number;
  reset_date: string;
}

/**
 * Interface para transações de pagamento
 */
export interface PaymentTransaction {
  id: string;
  user_id: string;
  subscription_id?: string;
  amount: number;
  currency: string;
  payment_gateway: PaymentGateway;
  status: 'completed' | 'pending' | 'failed' | 'refunded';
  transaction_date: string;
  description: string;
}

/**
 * Interface para checkout
 */
export interface CheckoutRequest {
  plan_id: string;
  coupon_code?: string;
  success_url: string;
  cancel_url: string;
}

/**
 * Interface para resposta de checkout
 */
export interface CheckoutResponse {
  checkout_url: string;
  session_id: string;
  expires_at: string;
}

/**
 * Interface para solicitação de recompensa por anúncio
 */
export interface AdRewardRequest {
  ad_type: AdType;
  reward_type: RewardType;
}

/**
 * Interface para resposta de recompensa por anúncio
 */
export interface AdRewardResponse {
  success: boolean;
  reward: AdReward;
  new_limits: UserLimits;
}

/**
 * Interface para cupons de desconto
 */
export interface Coupon {
  id: string;
  code: string;
  discount_percent: number;
  valid_until: string;
  is_valid: boolean;
}

/**
 * Estado global de monetização
 */
export interface MonetizationState {
  userSubscription: UserSubscription | null;
  userLimits: UserLimits | null;
  availablePlans: Plan[];
  adRewards: AdReward[];
  isLoading: boolean;
  error: any;
}

/**
 * Tipos de benefícios dos planos
 */
export type PlanBenefit = 
  | 'unlimited_chat' 
  | 'unlimited_studies' 
  | 'no_ads' 
  | 'premium_content' 
  | 'priority_support'
  | 'limited_chat'
  | 'limited_studies';

/**
 * Tipos de recompensas por anúncios
 */
export type AdRewardType = keyof typeof RewardType;

/**
 * Interface para faturas de pagamento
 */
export interface PaymentInvoice {
  id: string;
  user_id: string;
  subscription_id: string;
  amount: number;
  currency: string;
  status: 'paid' | 'pending' | 'failed';
  payment_method: string;
  created_at: string;
  paid_at: string | null;
}

/**
 * Estado global do contexto de monetização
 */
export interface MonetizationContextType {
  // Estado
  currentPlan: Plan | null;
  userSubscription: UserSubscription | null;
  availablePlans: Plan[];
  adRewards: AdReward[];
  isLoading: boolean;
  isCancelling: boolean; // Indica se um cancelamento está em andamento
  error: string | null;
  
  // Controle de limites
  chatMessagesRemaining: number;
  studiesRemaining: number;
  
  // Checar acesso
  isPremium: boolean;
  hasAccess: (feature: PlanBenefit) => boolean;
  
  // Ações de controle
  fetchUserSubscription: () => Promise<void>;
  fetchAvailablePlans: () => Promise<void>;
  fetchAdRewards: () => Promise<void>;
  
  // Ações para pagamento
  startSubscription: (planId: string) => Promise<string>; // Retorna URL de checkout
  cancelSubscription: () => Promise<void>;
  
  // Ações para recompensa de anúncios (plano Free)
  watchAdForReward: (rewardType: AdRewardType) => Promise<void>;
  useAdReward: (rewardType: AdRewardType) => Promise<boolean>;
  checkRewardAvailability: (rewardType: AdRewardType) => boolean;
  
  // Helpers
  refreshMonetizationData: () => Promise<void>;
  getRemainingTime: () => { days: number; hours: number } | null;
}

/**
 * Valores padrão para limites do plano free
 */
export const DEFAULT_FREE_LIMITS = {
  dailyChatMessages: 5,
  monthlyStudies: 10
}; 