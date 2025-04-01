import React from 'react';
import { TrendingUp, Users, Clock, MessageSquare } from 'lucide-react';

/**
 * Interface para dados do dashboard
 */
interface DashboardData {
  metrics: {
    total_users: number;
    active_users_today: number;
    total_chat_messages: number;
  };
  growth: {
    users: number;
    chat_messages: number;
  };
}

/**
 * Componente que exibe as principais métricas no dashboard administrativo
 */
interface DashboardMetricsProps {
  dashboardData: DashboardData;
}

const DashboardMetrics: React.FC<DashboardMetricsProps> = ({ dashboardData }) => {
  if (!dashboardData || !dashboardData.metrics) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white p-6 rounded-lg shadow animate-pulse h-32"></div>
        <div className="bg-white p-6 rounded-lg shadow animate-pulse h-32"></div>
        <div className="bg-white p-6 rounded-lg shadow animate-pulse h-32"></div>
      </div>
    );
  }

  const { metrics, growth } = dashboardData;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Total de usuários */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-3 rounded-full bg-blue-100 mr-4">
            <Users className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Usuários totais</p>
            <p className="text-2xl font-semibold text-gray-900">{metrics.total_users.toLocaleString()}</p>
          </div>
        </div>
        <div className="mt-2">
          <p className="text-sm text-gray-600">
            <span className={`font-medium ${growth.users >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {growth.users >= 0 ? '+' : ''}{growth.users}%
            </span> desde o último mês
          </p>
        </div>
      </div>
      
      {/* Usuários ativos hoje */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-3 rounded-full bg-green-100 mr-4">
            <Clock className="h-6 w-6 text-green-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Usuários ativos (hoje)</p>
            <p className="text-2xl font-semibold text-gray-900">{metrics.active_users_today.toLocaleString()}</p>
          </div>
        </div>
        <div className="mt-2">
          <p className="text-sm text-gray-600">
            <span className={`font-medium text-green-600`}>
              {metrics.active_users_today / metrics.total_users * 100}%
            </span> do total de usuários
          </p>
        </div>
      </div>
      
      {/* Interações com IA */}
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center">
          <div className="p-3 rounded-full bg-purple-100 mr-4">
            <MessageSquare className="h-6 w-6 text-purple-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600">Chat mensagens (total)</p>
            <p className="text-2xl font-semibold text-gray-900">{metrics.total_chat_messages.toLocaleString()}</p>
          </div>
        </div>
        <div className="mt-2">
          <p className="text-sm text-gray-600">
            <span className={`font-medium ${growth.chat_messages >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {growth.chat_messages >= 0 ? '+' : ''}{growth.chat_messages}%
            </span> em relação ao período anterior
          </p>
        </div>
      </div>
    </div>
  );
};

export default DashboardMetrics; 