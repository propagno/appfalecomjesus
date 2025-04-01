import React, { useEffect, useState } from 'react';
import { useAdmin } from '../contexts/AdminContext';
import { DashboardMetricsCard } from '../components/Dashboard/DashboardMetricsCard';
import { TimeRange } from '../types';

export const DashboardPage: React.FC = () => {
  const { 
    dashboard, 
    fetchDashboardMetrics, 
    getChartData, 
    getTopUsers,
    isLoading, 
    error 
  } = useAdmin();

  const [selectedTimeRange, setSelectedTimeRange] = useState<TimeRange>('last_30_days');
  const [chartData, setChartData] = useState<any>(null);
  const [topUsers, setTopUsers] = useState<any[]>([]);
  const [isChartLoading, setIsChartLoading] = useState(false);
  
  // Carregar métricas iniciais
  useEffect(() => {
    fetchDashboardMetrics(selectedTimeRange);
  }, [fetchDashboardMetrics, selectedTimeRange]);
  
  // Carregar dados de gráfico e usuários mais ativos
  useEffect(() => {
    const loadChartData = async () => {
      setIsChartLoading(true);
      try {
        const data = await getChartData('active_users', selectedTimeRange);
        setChartData(data);
        
        const users = await getTopUsers();
        setTopUsers(users);
      } catch (error) {
        console.error('Erro ao carregar dados do gráfico:', error);
      } finally {
        setIsChartLoading(false);
      }
    };
    
    loadChartData();
  }, [getChartData, getTopUsers, selectedTimeRange]);
  
  // Função auxiliar para formatar números
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('pt-BR').format(num);
  };
  
  // Função auxiliar para calcular tendência 
  const calculateTrend = (current: number, previous: number): 'up' | 'down' | 'neutral' => {
    if (current > previous) return 'up';
    if (current < previous) return 'down';
    return 'neutral';
  };
  
  // Função auxiliar para calcular variação percentual
  const calculatePercentChange = (current: number, previous: number): number => {
    if (previous === 0) return 0;
    return Math.round(((current - previous) / previous) * 100);
  };

  if (isLoading) {
    return (
      <div className="p-6 bg-gray-50 min-h-screen">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="animate-pulse bg-white rounded-lg shadow-md p-4 h-28"></div>
          ))}
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 animate-pulse bg-white rounded-lg shadow-md p-4 h-80"></div>
          <div className="animate-pulse bg-white rounded-lg shadow-md p-4 h-80"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-gray-50 min-h-screen">
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 mb-6">
          Erro ao carregar dados do dashboard: {error}
        </div>
        <button 
          onClick={() => fetchDashboardMetrics(selectedTimeRange)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Tentar Novamente
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        
        <div className="flex space-x-2">
          <select 
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value as TimeRange)}
            className="border border-gray-300 rounded-md shadow-sm py-2 px-3 bg-white text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="today">Hoje</option>
            <option value="last_7_days">Últimos 7 dias</option>
            <option value="last_30_days">Últimos 30 dias</option>
            <option value="last_quarter">Último trimestre</option>
            <option value="last_year">Último ano</option>
          </select>
          
          <button 
            onClick={() => fetchDashboardMetrics(selectedTimeRange)}
            className="bg-white p-2 rounded-md border border-gray-300 shadow-sm"
            title="Atualizar dados"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>
      
      {dashboard && (
        <>
          {/* Métricas principais */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <DashboardMetricsCard
              title="Usuários Totais"
              value={formatNumber(dashboard.userMetrics.totalUsers)}
              change={calculatePercentChange(
                dashboard.userMetrics.totalUsers,
                dashboard.trends.userGrowth[0]?.value || 0
              )}
              trend={calculateTrend(
                dashboard.userMetrics.totalUsers,
                dashboard.trends.userGrowth[0]?.value || 0
              )}
            />
            
            <DashboardMetricsCard
              title="Usuários Ativos"
              value={formatNumber(dashboard.userMetrics.activeUsersMonth)}
              change={calculatePercentChange(
                dashboard.userMetrics.activeUsersMonth,
                dashboard.userMetrics.activeUsersMonth * 0.9
              )}
              trend="up"
            />
            
            <DashboardMetricsCard
              title="Estudos Completos"
              value={formatNumber(dashboard.studyMetrics.completedStudiesMonth)}
              change={calculatePercentChange(
                dashboard.studyMetrics.completedStudiesMonth,
                dashboard.trends.studyGrowth[0]?.value || 0
              )}
              trend={calculateTrend(
                dashboard.studyMetrics.completedStudiesMonth,
                dashboard.trends.studyGrowth[0]?.value || 0
              )}
            />
            
            <DashboardMetricsCard
              title="Taxa de Conversão"
              value={`${dashboard.subscriptionMetrics.conversionRate}%`}
              change={calculatePercentChange(
                dashboard.subscriptionMetrics.conversionRate,
                dashboard.trends.conversionRateGrowth[0]?.value || 0
              )}
              trend={calculateTrend(
                dashboard.subscriptionMetrics.conversionRate,
                dashboard.trends.conversionRateGrowth[0]?.value || 0
              )}
            />
          </div>
          
          {/* Gráficos e tabelas */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Gráfico principal */}
            <div className="lg:col-span-2 bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-medium mb-4">Usuários Ativos</h2>
              
              {isChartLoading ? (
                <div className="animate-pulse h-64 bg-gray-100 rounded"></div>
              ) : chartData ? (
                <div className="h-64">
                  {/* Aqui seria integrado um componente de gráfico como recharts */}
                  <div className="text-gray-500 flex items-center justify-center h-full">
                    <p>Gráfico de usuários ativos ao longo do tempo</p>
                    {/* Na implementação real, usar biblioteca de gráficos como:
                    <LineChart width={500} height={300} data={chartData.datasets[0].data}>
                      <XAxis dataKey="name" />
                      <YAxis />
                      <CartesianGrid strokeDasharray="3 3" />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="value" stroke="#8884d8" />
                    </LineChart> */}
                  </div>
                </div>
              ) : (
                <div className="text-gray-500 flex items-center justify-center h-64">
                  Não foi possível carregar o gráfico
                </div>
              )}
            </div>
            
            {/* Usuários mais ativos */}
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="text-lg font-medium mb-4">Usuários Mais Ativos</h2>
              
              {topUsers.length > 0 ? (
                <div className="overflow-hidden">
                  <ul className="divide-y divide-gray-200">
                    {topUsers.map((user) => (
                      <li key={user.id} className="py-3">
                        <div className="flex items-center space-x-4">
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {user.name}
                            </p>
                            <p className="text-sm text-gray-500 truncate">
                              {user.email}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm font-medium text-gray-900">
                              {user.engagement.activity_level}
                            </p>
                            <p className="text-sm text-gray-500">
                              {user.engagement.study_count + user.engagement.chat_count} sessões
                            </p>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <div className="text-gray-500 flex items-center justify-center h-64">
                  Não foi possível carregar usuários
                </div>
              )}
            </div>
          </div>
          
          {/* Distribuição de planos */}
          <div className="mt-6 bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-medium mb-4">Distribuição de Planos</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-600 font-medium">Usuários Free</p>
                <p className="text-2xl font-bold">{formatNumber(dashboard.subscriptionMetrics.freeUsers)}</p>
                <p className="text-sm text-gray-500">{Math.round((dashboard.subscriptionMetrics.freeUsers / dashboard.userMetrics.totalUsers) * 100)}% do total</p>
              </div>
              
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-purple-600 font-medium">Assinantes Premium Mensal</p>
                <p className="text-2xl font-bold">{formatNumber(dashboard.subscriptionMetrics.premiumMonthlyUsers)}</p>
                <p className="text-sm text-gray-500">{Math.round((dashboard.subscriptionMetrics.premiumMonthlyUsers / dashboard.userMetrics.totalUsers) * 100)}% do total</p>
              </div>
              
              <div className="bg-indigo-50 p-4 rounded-lg">
                <p className="text-sm text-indigo-600 font-medium">Assinantes Premium Anual</p>
                <p className="text-2xl font-bold">{formatNumber(dashboard.subscriptionMetrics.premiumAnnualUsers)}</p>
                <p className="text-sm text-gray-500">{Math.round((dashboard.subscriptionMetrics.premiumAnnualUsers / dashboard.userMetrics.totalUsers) * 100)}% do total</p>
              </div>
            </div>
          </div>
          
          {/* Tópicos populares */}
          <div className="mt-6 bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-medium mb-4">Tópicos Mais Populares</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              {dashboard.studyMetrics.popularTopics.map((topic, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm font-medium text-gray-900">{topic.name}</p>
                  <p className="text-xl font-bold">{formatNumber(topic.count)}</p>
                  <p className="text-sm text-gray-500">estudos</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}; 