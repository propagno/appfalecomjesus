import React, { useState } from 'react';
import { DashboardPeriod } from '../types';
import UsersList from '../components/UsersList';

const AdminDashboardPage: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState<DashboardPeriod>(DashboardPeriod.WEEK);
  const [isMaintenanceMode, setIsMaintenanceMode] = useState(false);

  const handlePeriodChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value as DashboardPeriod;
    setSelectedPeriod(value);
  };

  const toggleMaintenanceMode = () => {
    setIsMaintenanceMode(!isMaintenanceMode);
    // In a real implementation, this would call a backend API
  };

  const refreshData = () => {
    // In a real implementation, this would refresh data from API
    console.log('Refreshing data for period:', selectedPeriod);
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Painel Administrativo</h1>
          <p className="text-gray-600 mt-1">
            Visualize métricas e gerenciar conteúdos do sistema
          </p>
        </div>
        
        <div className="mt-4 md:mt-0 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
          <div className="flex items-center">
            <span className="mr-2 text-sm text-gray-700">Período:</span>
            <select
              value={selectedPeriod}
              onChange={handlePeriodChange}
              className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={DashboardPeriod.TODAY}>Hoje</option>
              <option value={DashboardPeriod.YESTERDAY}>Ontem</option>
              <option value={DashboardPeriod.WEEK}>Última semana</option>
              <option value={DashboardPeriod.MONTH}>Último mês</option>
              <option value={DashboardPeriod.QUARTER}>Último trimestre</option>
              <option value={DashboardPeriod.YEAR}>Último ano</option>
              <option value={DashboardPeriod.ALL_TIME}>Todo o período</option>
            </select>
          </div>
          
          <button
            onClick={refreshData}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200"
          >
            Atualizar Dados
          </button>
          
          <button
            onClick={toggleMaintenanceMode}
            className={`px-4 py-2 rounded-md transition-colors duration-200 ${
              isMaintenanceMode
                ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            {isMaintenanceMode ? 'Desativar Manutenção' : 'Ativar Manutenção'}
          </button>
        </div>
      </div>
      
      {/* Alert para modo de manutenção */}
      {isMaintenanceMode && (
        <div className="mb-6 p-4 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700">
          <div className="flex items-center">
            <svg
              className="h-5 w-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              ></path>
            </svg>
            <p className="font-medium">
              O sistema está em modo de manutenção. Os usuários não podem acessar o sistema.
            </p>
          </div>
        </div>
      )}
      
      {/* Métricas principais */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Métricas do Sistema</h2>
        <p className="text-gray-600">
          As métricas para o período {selectedPeriod} serão exibidas aqui.
        </p>
      </div>
      
      {/* Lista de usuários */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Gerenciamento de Usuários</h2>
        <UsersList />
      </div>
      
      {/* Links para outras seções administrativas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
          <h3 className="text-xl font-semibold mb-2">Logs do Sistema</h3>
          <p className="text-gray-600 mb-4">
            Visualize logs de erro, atividade e segurança do sistema
          </p>
          <a
            href="/admin/logs"
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            Acessar Logs →
          </a>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
          <h3 className="text-xl font-semibold mb-2">Tarefas de Manutenção</h3>
          <p className="text-gray-600 mb-4">
            Gerenciar backups, limpeza de dados e otimizações
          </p>
          <a
            href="/admin/maintenance"
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            Gerenciar Tarefas →
          </a>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow">
          <h3 className="text-xl font-semibold mb-2">Configurações</h3>
          <p className="text-gray-600 mb-4">
            Ajustar parâmetros e configurações do sistema
          </p>
          <a
            href="/admin/settings"
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            Acessar Configurações →
          </a>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage; 