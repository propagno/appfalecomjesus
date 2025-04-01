import React, { useState } from 'react';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import PlanCard from '../components/PlanCard';
import { Button } from '../../../shared/components/ui/Button';
import { SubscriptionStatus } from '../types';

/**
 * Página de planos e assinaturas
 * Exibe os planos disponíveis e permite ao usuário assinar ou gerenciar sua assinatura
 */
const PlansPage: React.FC = () => {
  const { state, cancelSubscription, reactivateSubscription } = useMonetizationContext();
  const [loading, setLoading] = useState(false);
  
  const handleCancelSubscription = async () => {
    if (!state.userSubscription) return;
    
    if (window.confirm('Tem certeza que deseja cancelar sua assinatura? Você terá acesso até o fim do período pago.')) {
      try {
        setLoading(true);
        await cancelSubscription(state.userSubscription.id);
      } catch (error) {
        console.error('Erro ao cancelar assinatura:', error);
      } finally {
        setLoading(false);
      }
    }
  };
  
  const handleReactivateSubscription = async () => {
    if (!state.userSubscription) return;
    
    try {
      setLoading(true);
      await reactivateSubscription(state.userSubscription.id);
    } catch (error) {
      console.error('Erro ao reativar assinatura:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Formatação da data em formato brasileiro
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(date);
  };
  
  // Renderiza o banner de status da assinatura atual
  const renderSubscriptionStatus = () => {
    if (!state.userSubscription) return null;
    
    const { status, end_date, plan_type } = state.userSubscription;
    
    // Determinar a cor do banner baseado no status
    let bannerClass = "rounded-lg p-4 mb-8 ";
    let actionButton = null;
    
    switch (status) {
      case SubscriptionStatus.ACTIVE:
        bannerClass += "bg-green-50 border border-green-200";
        actionButton = (
          <Button
            variant="outline"
            onClick={handleCancelSubscription}
            loading={loading}
            className="ml-4"
          >
            Cancelar Assinatura
          </Button>
        );
        break;
        
      case SubscriptionStatus.TRIAL:
        bannerClass += "bg-blue-50 border border-blue-200";
        actionButton = (
          <Button
            variant="outline"
            onClick={handleCancelSubscription}
            loading={loading}
            className="ml-4"
          >
            Cancelar Período de Teste
          </Button>
        );
        break;
        
      case SubscriptionStatus.CANCELED:
        bannerClass += "bg-amber-50 border border-amber-200";
        actionButton = (
          <Button
            variant="primary"
            onClick={handleReactivateSubscription}
            loading={loading}
            className="ml-4"
          >
            Reativar Assinatura
          </Button>
        );
        break;
        
      case SubscriptionStatus.EXPIRED:
        bannerClass += "bg-gray-50 border border-gray-200";
        break;
        
      default:
        bannerClass += "bg-gray-50 border border-gray-200";
    }
    
    return (
      <div className={bannerClass}>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h3 className="text-lg font-semibold mb-1">
              Status da sua assinatura: <span className="capitalize">{status}</span>
            </h3>
            <p className="text-gray-700">
              {status === SubscriptionStatus.ACTIVE && 
                `Sua assinatura ${plan_type} está ativa até ${formatDate(end_date)}`}
              
              {status === SubscriptionStatus.TRIAL && 
                `Seu período de teste está ativo até ${formatDate(end_date)}`}
              
              {status === SubscriptionStatus.CANCELED && 
                `Sua assinatura foi cancelada, mas você tem acesso até ${formatDate(end_date)}`}
              
              {status === SubscriptionStatus.EXPIRED && 
                `Sua assinatura expirou em ${formatDate(end_date)}`}
              
              {status === SubscriptionStatus.PENDING && 
                `Sua assinatura está pendente de confirmação de pagamento`}
            </p>
          </div>
          
          {actionButton}
        </div>
      </div>
    );
  };
  
  if (state.isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Planos FaleComJesus</h1>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin h-8 w-8 border-4 border-indigo-500 rounded-full border-t-transparent"></div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Planos FaleComJesus</h1>
      
      {renderSubscriptionStatus()}
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {state.availablePlans.map(plan => (
          <PlanCard
            key={plan.id}
            plan={plan}
            isCurrentPlan={
              state.userSubscription?.plan_id === plan.id && 
              (state.userSubscription?.status === SubscriptionStatus.ACTIVE || 
               state.userSubscription?.status === SubscriptionStatus.TRIAL)
            }
          />
        ))}
      </div>
      
      {!state.availablePlans.length && (
        <p className="text-center py-10 text-gray-500">
          Nenhum plano disponível no momento. Por favor, tente novamente mais tarde.
        </p>
      )}
      
      {/* Seção de FAQ */}
      <div className="mt-16">
        <h2 className="text-xl font-bold mb-6">Perguntas Frequentes</h2>
        
        <div className="space-y-6">
          <div>
            <h3 className="font-semibold mb-2">Como funciona a assinatura?</h3>
            <p>A assinatura FaleComJesus permite acesso a todos os recursos premium da plataforma. Você pode escolher entre planos mensais ou anuais com cobrança recorrente.</p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-2">Posso cancelar a qualquer momento?</h3>
            <p>Sim, você pode cancelar sua assinatura a qualquer momento. Após o cancelamento, você continuará tendo acesso aos recursos premium até o final do período pago.</p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-2">Como funciona o período de teste?</h3>
            <p>Novos assinantes têm acesso a um período de teste de 7 dias para experimentar todos os recursos premium. Você não será cobrado durante o período de teste.</p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-2">É seguro fornecer meus dados de pagamento?</h3>
            <p>Sim, todos os pagamentos são processados por gateways confiáveis (Stripe/Hotmart) com criptografia de ponta a ponta. Não armazenamos dados de cartão de crédito em nossos servidores.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlansPage; 