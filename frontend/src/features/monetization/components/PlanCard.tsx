import React from 'react';
import { Plan, PlanType } from '../types';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import { Button } from '../../../shared/components/ui/Button';
import { toast } from 'react-toastify';

interface PlanCardProps {
  plan: Plan;
  isCurrentPlan?: boolean;
  onSelectPlan?: (planId: string) => void;
  isLoading?: boolean;
}

/**
 * Componente que exibe um plano de assinatura com seus detalhes e possibilita que o usuário inicie o checkout
 */
const PlanCard: React.FC<PlanCardProps> = ({ plan, isCurrentPlan = false, onSelectPlan, isLoading }) => {
  const { initiateCheckout, state, isPremium } = useMonetizationContext();
  const [loading, setLoading] = React.useState(false);
  const [couponCode, setCouponCode] = React.useState('');
  
  // Formatar preço de acordo com a moeda e periodicidade
  const formatPrice = () => {
    const currencyFormatter = new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: plan.currency || 'BRL',
    });
    
    const price = currencyFormatter.format(plan.price);
    
    if (plan.type === PlanType.FREE) {
      return 'Grátis';
    }
    
    if (plan.billing_interval === 'monthly') {
      return `${price}/mês`;
    }
    
    if (plan.billing_interval === 'yearly') {
      const monthlyPrice = plan.price / 12;
      const monthlyFormatted = currencyFormatter.format(monthlyPrice);
      return `${price}/ano (${monthlyFormatted}/mês)`;
    }
    
    return price;
  };
  
  // Iniciar processo de checkout
  const handleSubscribe = async () => {
    if (isCurrentPlan) {
      toast.info('Você já está inscrito neste plano.', {
        position: "top-right",
        autoClose: 3000,
      });
      return;
    }
    
    try {
      setLoading(true);
      
      // Se onSelectPlan foi fornecido, usar ele
      if (onSelectPlan) {
        onSelectPlan(plan.id);
        return;
      }
      
      // Caso contrário, usar o comportamento padrão com initiateCheckout
      const checkoutUrl = await initiateCheckout(plan.id, couponCode || undefined);
      
      // Redirecionar para a página de checkout
      window.location.href = checkoutUrl;
    } catch (error) {
      console.error('Erro ao iniciar checkout:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Estilo do cartão depende do tipo de plano
  const getCardClassName = () => {
    let baseClass = 'rounded-lg border p-6 shadow-md transition-all hover:shadow-lg';
    
    if (isCurrentPlan) {
      baseClass += ' border-2 border-indigo-500 bg-indigo-50';
    } else if (plan.type === PlanType.PREMIUM_ANNUAL) {
      baseClass += ' border-amber-400 bg-amber-50';
    } else if (plan.type === PlanType.PREMIUM) {
      baseClass += ' border-blue-400 bg-blue-50';
    } else {
      baseClass += ' border-gray-200 bg-gray-50';
    }
    
    return baseClass;
  };
  
  // Exibe o label do plano atual ou recomendado
  const renderLabel = () => {
    if (isCurrentPlan) {
      return (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-500 px-3 py-1 text-sm font-semibold text-white rounded-full">
          Plano Atual
        </div>
      );
    }
    
    if (plan.recommended) {
      return (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-amber-500 px-3 py-1 text-sm font-semibold text-white rounded-full">
          Recomendado
        </div>
      );
    }
    
    return null;
  };
  
  return (
    <div className={`${getCardClassName()} relative flex flex-col h-full`}>
      {renderLabel()}
      
      <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
      <div className="text-2xl font-bold mb-4">{formatPrice()}</div>
      
      <div className="mb-4 flex-grow">
        <p className="text-gray-700 mb-4">{plan.description}</p>
        
        <ul className="space-y-2">
          {plan.features.map((feature, index) => (
            <li key={index} className="flex items-start">
              <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
              <span>{feature}</span>
            </li>
          ))}
        </ul>
      </div>
      
      {plan.type !== PlanType.FREE && (
        <div className="mb-4">
          <label htmlFor={`coupon-${plan.id}`} className="block text-sm font-medium text-gray-700 mb-1">
            Cupom de desconto
          </label>
          <input
            id={`coupon-${plan.id}`}
            type="text"
            value={couponCode}
            onChange={(e) => setCouponCode(e.target.value)}
            placeholder="Digite seu cupom"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )}
      
      <Button
        onClick={handleSubscribe}
        disabled={loading || (plan.type === PlanType.FREE && isPremium)}
        loading={loading}
        variant={
          plan.type === PlanType.PREMIUM_ANNUAL 
            ? "primary" 
            : plan.type === PlanType.PREMIUM 
              ? "secondary" 
              : "outline"
        }
        className="w-full justify-center mt-auto"
      >
        {isCurrentPlan
          ? 'Plano Atual'
          : plan.type === PlanType.FREE
            ? isPremium
              ? 'Downgrade (após expiração)'
              : 'Plano Atual'
            : `Assinar ${plan.name}`
        }
      </Button>
    </div>
  );
};

export default PlanCard; 