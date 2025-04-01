import React from 'react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { CreditCard, Calendar, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { useMonetizationContext } from '../contexts/MonetizationContext';

/**
 * Component that displays the user's current subscription details
 */
export const SubscriptionInfo: React.FC = () => {
  const { state, cancelSubscription } = useMonetizationContext();
  const { userSubscription, availablePlans } = state;
  const currentPlan = availablePlans.find(plan => plan.id === userSubscription?.plan_id);
  const isCancelingSubscription = false; // Placeholder until we have a proper state for this

  if (!userSubscription || !currentPlan) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3 mx-auto mb-4"></div>
        </div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), "dd 'de' MMMM 'de' yyyy", { locale: ptBR });
    } catch (e) {
      return 'Data indisponível';
    }
  };

  const handleCancelSubscription = async () => {
    if (window.confirm('Tem certeza que deseja cancelar sua assinatura? Você perderá acesso aos recursos premium quando o período atual terminar.')) {
      try {
        if (userSubscription.id) {
          await cancelSubscription(userSubscription.id);
        }
      } catch (error) {
        console.error('Erro ao cancelar assinatura:', error);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {/* Card header */}
      <div className={`p-4 ${
        userSubscription.plan_type === 'free' 
          ? 'bg-gray-100' 
          : 'bg-blue-600 text-white'
      }`}>
        <div className="flex justify-between items-center">
          <h3 className={`font-semibold text-lg ${
            userSubscription.plan_type === 'free' ? 'text-gray-800' : 'text-white'
          }`}>
            {currentPlan.name}
          </h3>
          
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            userSubscription.status === 'active' 
              ? 'bg-green-100 text-green-800' 
              : userSubscription.status === 'canceled' 
                ? 'bg-orange-100 text-orange-800'
                : 'bg-red-100 text-red-800'
          }`}>
            {userSubscription.status === 'active' 
              ? 'Ativo' 
              : userSubscription.status === 'canceled' 
                ? 'Cancelado'
                : userSubscription.status === 'expired'
                  ? 'Expirado'
                  : 'Pendente'
            }
          </div>
        </div>
      </div>
      
      {/* Card body */}
      <div className="p-4">
        <ul>
          {/* Start date */}
          <li className="flex justify-between items-center py-2 border-b border-gray-100">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 text-gray-500 mr-3" />
              <span className="text-gray-600">Data de início</span>
            </div>
            <span className="text-gray-800 font-medium">{formatDate(userSubscription.start_date)}</span>
          </li>
          
          {/* End date */}
          <li className="flex justify-between items-center py-2 border-b border-gray-100">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 text-gray-500 mr-3" />
              <span className="text-gray-600">Validade</span>
            </div>
            <span className="text-gray-800 font-medium">{formatDate(userSubscription.end_date)}</span>
          </li>
          
          {/* Payment gateway */}
          {userSubscription.payment_gateway && (
            <li className="flex justify-between items-center py-2 border-b border-gray-100">
              <div className="flex items-center">
                <CreditCard className="h-5 w-5 text-gray-500 mr-3" />
                <span className="text-gray-600">Forma de pagamento</span>
              </div>
              <span className="text-gray-800 font-medium">{userSubscription.payment_gateway}</span>
            </li>
          )}
          
          {/* We don't have auto_renew in UserSubscription, so let's comment out this block for now */}
          {/* 
          <li className="flex justify-between items-center py-2 border-b border-gray-100">
            <div className="flex items-center">
              {userSubscription.auto_renew ? (
                <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              ) : (
                <XCircle className="h-5 w-5 text-red-500 mr-3" />
              )}
              <span className="text-gray-600">Renovação automática</span>
            </div>
            <span className={`font-medium ${
              userSubscription.auto_renew ? 'text-green-600' : 'text-red-600'
            }`}>
              {userSubscription.auto_renew ? 'Ativa' : 'Desativada'}
            </span>
          </li>
          */}
        </ul>
      </div>
      
      {/* Action buttons */}
      <div className="p-4 bg-gray-50 border-t border-gray-100">
        {userSubscription.status === 'active' && userSubscription.plan_type !== 'free' && (
          <div className="space-y-4">
            {/* 
            {userSubscription.auto_renew && (
              <div className="flex items-start mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-yellow-700">
                  Ao cancelar sua assinatura, você continuará tendo acesso aos recursos premium até {formatDate(userSubscription.end_date)}. Após essa data, seu plano será revertido para o gratuito.
                </p>
              </div>
            )}
            */}
            
            <button
              className="w-full py-2 px-4 bg-red-50 hover:bg-red-100 text-red-600 font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
              onClick={handleCancelSubscription}
              disabled={isCancelingSubscription}
            >
              {isCancelingSubscription ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Cancelando...
                </>
              ) : (
                'Cancelar assinatura'
              )}
            </button>
          </div>
        )}
        
        {(userSubscription.status === 'canceled' || userSubscription.status === 'expired') && (
          <div className="text-center text-gray-600 text-sm">
            Sua assinatura não está mais ativa. Considere fazer upgrade para voltar a ter acesso premium.
          </div>
        )}
      </div>
    </div>
  );
};

export default SubscriptionInfo; 