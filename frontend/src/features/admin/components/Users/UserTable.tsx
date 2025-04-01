import React, { useState } from 'react';
import { UserDetails, UserStatus, UserRole } from '../../types';
import { useAdmin } from '../../contexts/AdminContext';

interface UserTableProps {
  users: UserDetails[];
  isLoading: boolean;
  onViewDetails: (userId: string) => void;
  onStatusChange: (userId: string, status: UserStatus) => void;
}

export const UserTable: React.FC<UserTableProps> = ({
  users,
  isLoading,
  onViewDetails,
  onStatusChange
}) => {
  const [statusFilter, setStatusFilter] = useState<UserStatus | 'all'>('all');

  // Filtragem por status
  const filteredUsers = statusFilter === 'all'
    ? users
    : users.filter(user => user.status === statusFilter);

  // Renderização dos estados com cores
  const renderStatus = (status: UserStatus) => {
    const statusClasses = {
      active: 'bg-green-100 text-green-800',
      suspended: 'bg-yellow-100 text-yellow-800',
      disabled: 'bg-red-100 text-red-800',
      pending: 'bg-blue-100 text-blue-800'
    };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusClasses[status]}`}>
        {status}
      </span>
    );
  };

  // Renderização das funções de usuário
  const renderRole = (role: UserRole) => {
    const roleClasses = {
      user: 'text-gray-600',
      editor: 'text-indigo-600 font-medium',
      admin: 'text-purple-600 font-medium',
      super_admin: 'text-red-600 font-medium'
    };

    return (
      <span className={roleClasses[role]}>
        {role}
      </span>
    );
  };

  // Menu de ações para cada usuário
  const renderActions = (user: UserDetails) => {
    return (
      <div className="flex space-x-2">
        <button
          onClick={() => onViewDetails(user.id)}
          className="text-blue-600 hover:text-blue-800"
        >
          Detalhes
        </button>
        
        <div className="relative group">
          <button className="text-gray-600 hover:text-gray-800">
            Status
          </button>
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 hidden group-hover:block">
            {user.status !== 'active' && (
              <button
                onClick={() => onStatusChange(user.id, 'active')}
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                Ativar
              </button>
            )}
            
            {user.status !== 'suspended' && (
              <button
                onClick={() => onStatusChange(user.id, 'suspended')}
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                Suspender
              </button>
            )}
            
            {user.status !== 'disabled' && (
              <button
                onClick={() => onStatusChange(user.id, 'disabled')}
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
              >
                Desativar
              </button>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded mb-4"></div>
        {[1, 2, 3, 4, 5].map(index => (
          <div key={index} className="h-16 bg-gray-100 rounded mb-2"></div>
        ))}
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      {/* Filtros */}
      <div className="mb-4 flex space-x-2">
        <button 
          onClick={() => setStatusFilter('all')}
          className={`px-3 py-1 rounded text-sm ${statusFilter === 'all' ? 'bg-gray-200' : 'bg-gray-100'}`}
        >
          Todos
        </button>
        <button 
          onClick={() => setStatusFilter('active')}
          className={`px-3 py-1 rounded text-sm ${statusFilter === 'active' ? 'bg-green-200' : 'bg-gray-100'}`}
        >
          Ativos
        </button>
        <button 
          onClick={() => setStatusFilter('suspended')}
          className={`px-3 py-1 rounded text-sm ${statusFilter === 'suspended' ? 'bg-yellow-200' : 'bg-gray-100'}`}
        >
          Suspensos
        </button>
        <button 
          onClick={() => setStatusFilter('disabled')}
          className={`px-3 py-1 rounded text-sm ${statusFilter === 'disabled' ? 'bg-red-200' : 'bg-gray-100'}`}
        >
          Desativados
        </button>
      </div>
      
      {/* Tabela */}
      <table className="min-w-full bg-white rounded-lg overflow-hidden">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Usuário
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Função
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Plano
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Engajamento
            </th>
            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Ações
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {filteredUsers.length === 0 ? (
            <tr>
              <td colSpan={6} className="px-4 py-4 text-center text-gray-500">
                Nenhum usuário encontrado
              </td>
            </tr>
          ) : (
            filteredUsers.map(user => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="px-4 py-3">
                  <div className="flex items-center">
                    <div className="ml-3">
                      <div className="text-sm font-medium text-gray-900">{user.name}</div>
                      <div className="text-xs text-gray-500">{user.email}</div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  {renderStatus(user.status)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  {renderRole(user.role)}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                  {user.subscription.plan}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm">
                  <div className="text-gray-900">Sessions: {user.engagement.study_count + user.engagement.chat_count}</div>
                  <div className="text-xs text-gray-500">Streak: {user.engagement.login_streak} dias</div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm">
                  {renderActions(user)}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}; 