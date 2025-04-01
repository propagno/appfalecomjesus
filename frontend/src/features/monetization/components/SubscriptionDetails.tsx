import React from 'react';
import { Card } from '../../../components/ui/card';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import { formatDate } from '../utils/formatDate';

/**
 * Componente que exibe os detalhes da assinatura atual do usuário
 */
const SubscriptionDetails: React.FC = () => {
  const {
    state: { userSubscription, availablePlans, isLoading },
    isPremium,
    cancelSubscription
  } = useMonetizationContext();

  // Encontrar o plano atual nas opções disponíveis
  const currentPlan = userSubscription 
    ? availablePlans.find(p => p.type === userSubscription.plan_type) 
    : null;

  const handleCancelSubscription = () => {
    if (userSubscription && window.confirm('Tem certeza que deseja cancelar sua assinatura?')) {
      cancelSubscription(userSubscription.id);
    }
  };

  if (isLoading) {
    return (
      <Card className="p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded mb-4 w-1/2"></div>
        <div className="h-4 bg-gray-200 rounded mb-4 w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded mb-4 w-2/3"></div>
      </Card>
    );
  }

  if (!userSubscription || !currentPlan) {
    return (
      <Card className="p-6">
        <h3 className="text-lg font-medium mb-2">Sem assinatura ativa</h3>
        <p className="text-gray-500 text-sm">
          Você está usando a versão gratuita. Assine um plano premium para desbloquear recursos adicionais.
        </p>
      </Card>
    );
  }

  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium mb-4">Detalhes da Assinatura</h3>
      
      <div className="mb-4">
        <div className="flex items-center mb-2">
          <div className="w-1/3 text-gray-500 text-sm">Plano:</div>
          <div className="w-2/3 font-medium">{currentPlan.name}</div>
        </div>
        
        <div className="flex items-center mb-2">
          <div className="w-1/3 text-gray-500 text-sm">Status:</div>
          <div className="w-2/3">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              userSubscription.status === 'active' ? 'bg-green-100 text-green-800' : 
              userSubscription.status === 'canceled' ? 'bg-red-100 text-red-800' : 
              'bg-yellow-100 text-yellow-800'
            }`}>
              {userSubscription.status === 'active' ? 'Ativo' : 
               userSubscription.status === 'canceled' ? 'Cancelado' : 
               userSubscription.status === 'trial' ? 'Período de teste' : 
               'Pendente'}
            </span>
          </div>
        </div>
        
        <div className="flex items-center mb-2">
          <div className="w-1/3 text-gray-500 text-sm">Início:</div>
          <div className="w-2/3">{formatDate(userSubscription.start_date)}</div>
        </div>
        
        <div className="flex items-center">
          <div className="w-1/3 text-gray-500 text-sm">Validade:</div>
          <div className="w-2/3">{formatDate(userSubscription.end_date)}</div>
        </div>
      </div>
      
      {/* Preço */}
      <div className="mb-6 p-3 bg-gray-50 rounded-md">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Valor</span>
          <span className="font-medium">
            {currentPlan.price > 0 
              ? `R$ ${currentPlan.price.toFixed(2)}/${currentPlan.billing_interval === 'monthly' ? 'mês' : 'ano'}`
              : 'Grátis'}
          </span>
        </div>
      </div>
      
      {/* Botões de ação */}
      {userSubscription.status === 'active' && currentPlan.price > 0 && (
        <div className="text-right">
          <button
            onClick={handleCancelSubscription}
            className="text-sm text-red-600 hover:text-red-800 font-medium"
          >
            Cancelar assinatura
          </button>
          <p className="text-xs text-gray-500 mt-1">
            O acesso continuará disponível até o final do período pago.
          </p>
        </div>
      )}
    </Card>
  );
};

export default SubscriptionDetails; 