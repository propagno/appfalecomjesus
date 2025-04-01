import React from 'react';
import { useMonetization } from '../hooks/useMonetization';
import PlanCard from '../components/PlanCard';
import SubscriptionInfo from '../components/SubscriptionInfo';
import UsageLimits from '../components/UsageLimits';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../../components/base/Tabs';
import { CreditCard, Settings, BarChart2 } from 'lucide-react';

/**
 * Main monetization page - shows plans, subscription info, and usage limits
 */
export const MonetizationPage: React.FC = () => {
  const { availablePlans, userSubscription, isLoading } = useMonetization();

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-2/4 mb-10"></div>
          <div className="h-80 bg-gray-200 rounded mb-6"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
      {/* Page header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Assinatura e Limites</h1>
        <p className="text-gray-600 mt-2">
          Gerencie sua assinatura, planos disponíveis e limites de uso
        </p>
      </div>

      {/* Tabs for navigation */}
      <Tabs defaultValue={0}>
        <TabsList>
          <TabsTrigger>
            <div className="flex items-center">
              <CreditCard className="mr-2 h-5 w-5" />
              <span>Assinatura</span>
            </div>
          </TabsTrigger>
          <TabsTrigger>
            <div className="flex items-center">
              <Settings className="mr-2 h-5 w-5" />
              <span>Planos</span>
            </div>
          </TabsTrigger>
          <TabsTrigger>
            <div className="flex items-center">
              <BarChart2 className="mr-2 h-5 w-5" />
              <span>Limites de uso</span>
            </div>
          </TabsTrigger>
        </TabsList>

        {/* Subscription tab content */}
        <TabsContent value={0}>
          <div className="grid gap-6">
            <SubscriptionInfo />
            <UsageLimits />
          </div>
        </TabsContent>

        {/* Plans tab content */}
        <TabsContent value={1}>
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-1">Planos disponíveis</h2>
            <p className="text-gray-600">
              Escolha o plano que melhor atende às suas necessidades
            </p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {availablePlans.map(plan => (
              <PlanCard
                key={plan.id}
                plan={plan}
                isCurrentPlan={userSubscription?.plan_id === plan.id}
              />
            ))}
          </div>
        </TabsContent>

        {/* Usage limits tab content */}
        <TabsContent value={2}>
          <UsageLimits />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MonetizationPage; 