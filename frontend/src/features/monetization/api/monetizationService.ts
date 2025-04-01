import { monetizationApi } from '../../../shared/services/api';
import { API_URLS, USE_MOCKS } from '../../../shared/constants/config';
import {
  Plan,
  UserSubscription,
  UserLimits,
  AdReward,
  CheckoutRequest,
  CheckoutResponse,
  AdRewardRequest,
  AdRewardResponse,
  PaymentTransaction,
  Coupon,
  PaymentGateway
} from '../types';
import { MOCK_USER_SUBSCRIPTION, MOCK_AD_REWARDS, MOCK_PLANS, MOCK_USER_LIMITS } from '../types/mocks';

/**
 * Serviço de API para integração com o MS-Monetization
 * Implementação para o item 10.7 - Integração com MS-Monetization
 */
export const monetizationService = {
  /**
   * Obtém os planos disponíveis
   */
  async getPlans(): Promise<Plan[]> {
    if (USE_MOCKS) {
      return MOCK_PLANS;
    }
    const { data } = await monetizationApi.get('/plans');
    return data;
  },

  /**
   * Obtém detalhes de um plano específico
   */
  async getPlan(planId: string): Promise<Plan> {
    if (USE_MOCKS) {
      const plan = MOCK_PLANS.find(p => p.id === planId);
      if (!plan) throw new Error(`Plano não encontrado: ${planId}`);
      return plan;
    }
    const { data } = await monetizationApi.get(`/plans/${planId}`);
    return data;
  },

  /**
   * Obtém a assinatura atual do usuário
   */
  async getUserSubscription(): Promise<UserSubscription | null> {
    if (USE_MOCKS) {
      return MOCK_USER_SUBSCRIPTION;
    }
    try {
      const { data } = await monetizationApi.get('/user/subscription');
      return data;
    } catch (error) {
      if ((error as any).status === 404) {
        return null; // Usuário não tem assinatura
      }
      throw error;
    }
  },

  /**
   * Obtém os limites de uso do usuário
   */
  async getUserLimits(): Promise<UserLimits> {
    if (USE_MOCKS) {
      return MOCK_USER_LIMITS;
    }
    const { data } = await monetizationApi.get('/user/limits');
    return data;
  },

  /**
   * Inicia o processo de checkout para assinar um plano
   */
  async createCheckout(checkoutData: CheckoutRequest): Promise<CheckoutResponse> {
    if (USE_MOCKS) {
      // Simula uma URL de checkout
      return {
        checkout_url: `https://checkout.example.com/${checkoutData.plan_id}`,
        session_id: `sess_${Date.now()}`,
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 horas a partir de agora
      };
    }
    const { data } = await monetizationApi.post('/checkout', checkoutData);
    return data;
  },

  /**
   * Cancela uma assinatura ativa
   */
  async cancelSubscription(subscriptionId: string): Promise<{ success: boolean; message: string }> {
    if (USE_MOCKS) {
      return { success: true, message: 'Assinatura cancelada com sucesso' };
    }
    const { data } = await monetizationApi.post(`/subscriptions/${subscriptionId}/cancel`);
    return data;
  },

  /**
   * Reativa uma assinatura cancelada (se ainda estiver no período)
   */
  async reactivateSubscription(subscriptionId: string): Promise<{ success: boolean; message: string }> {
    if (USE_MOCKS) {
      return { success: true, message: 'Assinatura reativada com sucesso' };
    }
    const { data } = await monetizationApi.post(`/subscriptions/${subscriptionId}/reactivate`);
    return data;
  },

  /**
   * Registra uma recompensa de anúncio assistido
   */
  async registerAdReward(adRewardData: AdRewardRequest): Promise<AdRewardResponse> {
    if (USE_MOCKS) {
      const newReward: AdReward = {
        id: `reward_${Date.now()}`,
        user_id: 'user_mock',
        ad_type: adRewardData.ad_type,
        reward_type: adRewardData.reward_type,
        reward_amount: adRewardData.reward_type === 'chat_messages' ? 5 : 1, // 5 mensagens ou 1 dia de estudo
        created_at: new Date().toISOString()
      };
      
      return {
        success: true,
        reward: newReward,
        new_limits: {
          ...MOCK_USER_LIMITS,
          chat_messages_limit: 
            adRewardData.reward_type === 'chat_messages' 
              ? MOCK_USER_LIMITS.chat_messages_limit + 5 
              : MOCK_USER_LIMITS.chat_messages_limit,
        }
      };
    }
    const { data } = await monetizationApi.post('/ads/reward', adRewardData);
    return data;
  },

  /**
   * Obtém o histórico de recompensas de anúncios do usuário
   */
  async getAdRewardsHistory(): Promise<AdReward[]> {
    if (USE_MOCKS) {
      return MOCK_AD_REWARDS;
    }
    const { data } = await monetizationApi.get('/ads/history');
    return data;
  },

  /**
   * Obtém o histórico de transações do usuário
   */
  async getTransactionsHistory(): Promise<PaymentTransaction[]> {
    if (USE_MOCKS) {
      return [{
        id: 'trans_mock1',
        user_id: 'user_mock',
        subscription_id: 'sub_mock1',
        amount: 19.90,
        currency: 'BRL',
        payment_gateway: PaymentGateway.STRIPE,
        status: 'completed',
        transaction_date: new Date().toISOString(),
        description: 'Assinatura mensal Premium'
      }];
    }
    const { data } = await monetizationApi.get('/transactions');
    return data;
  },

  /**
   * Verifica a validade de um cupom de desconto
   */
  async validateCoupon(code: string, planId: string): Promise<Coupon> {
    if (USE_MOCKS) {
      // Simula um cupom válido para o código "DESCONTO20"
      if (code === 'DESCONTO20') {
        return {
          id: 'coupon_mock1',
          code: 'DESCONTO20',
          discount_percent: 20,
          valid_until: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 dias
          is_valid: true
        };
      }
      throw new Error('Cupom inválido ou expirado');
    }
    const { data } = await monetizationApi.get(`/coupons/validate?code=${code}&plan_id=${planId}`);
    return data;
  },

  /**
   * Obtém o hook de pagamentos para integração com o frontend
   */
  async getPaymentHook(planId: string): Promise<{ hook_script_url: string; hook_data: Record<string, any> }> {
    if (USE_MOCKS) {
      return {
        hook_script_url: 'https://static.example.com/payment-hook.js',
        hook_data: {
          planId,
          merchantId: 'mid_mock',
          apiKey: 'key_mock',
          returnUrl: window.location.origin + '/payment/success'
        }
      };
    }
    const { data } = await monetizationApi.get(`/payment-hook?plan_id=${planId}`);
    return data;
  },

  /**
   * Webhook para confirmar pagamento processado (usado pelo gateway)
   */
  async processWebhook(provider: string, payload: any): Promise<{ success: boolean }> {
    if (USE_MOCKS) {
      return { success: true };
    }
    const { data } = await monetizationApi.post(`/webhook/${provider}`, payload);
    return data;
  }
};

export default monetizationService; 