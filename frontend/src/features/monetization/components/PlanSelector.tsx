import React from 'react';
import { Plan } from '../types';
import PlanCard from './PlanCard';
import { useMonetizationContext } from '../contexts/MonetizationContext';

interface PlanSelectorProps {
  onSelectPlan: (planId: string) => void;
}

/**
 * Componente que exibe todos os planos disponíveis para assinatura
 */
const PlanSelector: React.FC<PlanSelectorProps> = ({ onSelectPlan }) => {
  const { 
    state: { availablePlans, userSubscription, isLoading }
  } = useMonetizationContext();

  // Verifica se o plano é o plano atual do usuário
  const isCurrentPlan = (plan: Plan): boolean => {
    if (!userSubscription) return plan.type === 'free';
    return userSubscription.plan_id === plan.id;
  };

  // Organizar planos por ordem (free primeiro, depois premium)
  const sortedPlans = [...availablePlans].sort((a, b) => {
    if (a.type === 'free') return -1;
    if (b.type === 'free') return 1;
    return a.price - b.price;
  });

  if (isLoading) {
    return (
      <div className="w-full py-8 flex justify-center items-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!availablePlans.length) {
    return (
      <div className="w-full py-8 text-center">
        <p className="text-gray-500">Nenhum plano disponível no momento</p>
      </div>
    );
  }

  return (
    <div className="w-full">
      <h2 className="text-2xl font-bold mb-6 text-center">Escolha seu plano</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sortedPlans.map((plan) => (
          <PlanCard
            key={plan.id}
            plan={plan}
            isCurrentPlan={isCurrentPlan(plan)}
            onSelectPlan={onSelectPlan}
            isLoading={isLoading}
          />
        ))}
      </div>
      
      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          Ao assinar, você concorda com nossos Termos de Serviço e Política de Privacidade
        </p>
      </div>
    </div>
  );
};

export default PlanSelector; 