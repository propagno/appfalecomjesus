import React, { useState } from 'react';
import useAdminQuery from '../hooks/useAdminQuery';
import { useAdmin } from '../providers/AdminProvider';

const UsersList: React.FC = () => {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  
  const { activeUserFilters, setActiveUserFilters } = useAdmin();
  
  // Combina os filtros com a paginação
  const filters = {
    ...activeUserFilters,
    page,
    limit: pageSize,
    search: searchTerm || undefined
  };
  
  const { useUsersQuery, useToggleUserBlockMutation } = useAdminQuery;
  const { data, isLoading, error } = useUsersQuery(filters);
  const toggleBlockMutation = useToggleUserBlockMutation();

  // Manipulador de busca
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1); // Volta para a primeira página ao buscar
  };

  // Manipulador de filtros
  const applyFilter = (filterKey: string, value: string | boolean) => {
    setActiveUserFilters({
      ...activeUserFilters,
      [filterKey]: value
    });
    setPage(1); // Volta para a primeira página ao filtrar
  };

  // Manipulador para bloqueio/desbloqueio
  const handleToggleBlock = (userId: string, currentlyBlocked: boolean) => {
    toggleBlockMutation.mutate({
      userId,
      isBlocked: !currentlyBlocked
    });
  };

  if (isLoading) {
    return <div className="p-4 text-center">Carregando usuários...</div>;
  }

  if (error || !data) {
    return (
      <div className="p-4 text-center text-red-500">
        Erro ao carregar usuários. Tente novamente mais tarde.
      </div>
    );
  }

  const { users, total, total_pages: totalPages } = data;

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b">
        <div className="flex flex-wrap justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">Usuários ({total})</h2>
          
          {/* Formulário de busca */}
          <form onSubmit={handleSearch} className="flex">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Buscar por nome ou email"
              className="px-3 py-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700"
            >
              Buscar
            </button>
          </form>
        </div>
        
        {/* Filtros */}
        <div className="flex flex-wrap gap-2 mb-2">
          <select
            onChange={(e) => applyFilter('subscription', e.target.value)}
            value={activeUserFilters.subscription || ''}
            className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todos os planos</option>
            <option value="free">Free</option>
            <option value="premium">Premium</option>
            <option value="premium_annual">Premium Anual</option>
          </select>
          
          <select
            onChange={(e) => applyFilter('status', e.target.value)}
            value={activeUserFilters.status || ''}
            className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Todos os status</option>
            <option value="active">Ativo</option>
            <option value="blocked">Bloqueado</option>
            <option value="unverified">Não verificado</option>
          </select>
          
          <select
            onChange={(e) => applyFilter('sortBy', e.target.value)}
            value={activeUserFilters.sortBy || 'created_at'}
            className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="created_at">Data de cadastro</option>
            <option value="last_login">Último login</option>
            <option value="name">Nome</option>
            <option value="email">Email</option>
          </select>
          
          <select
            onChange={(e) => applyFilter('sortOrder', e.target.value)}
            value={activeUserFilters.sortOrder || 'desc'}
            className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="desc">Decrescente</option>
            <option value="asc">Crescente</option>
          </select>
          
          <button
            onClick={() => {
              setActiveUserFilters({});
              setSearchTerm('');
              setPage(1);
            }}
            className="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Limpar filtros
          </button>
        </div>
      </div>
      
      {/* Tabela de usuários */}
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Nome</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Email</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Plano</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Cadastro</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Último login</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Status</th>
              <th className="px-4 py-3 text-sm font-medium text-gray-500">Ações</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-3">{user.name}</td>
                <td className="px-4 py-3">{user.email}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    user.subscription === 'premium' || user.subscription === 'premium_annual'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {user.subscription === 'premium' ? 'Premium' : 
                     user.subscription === 'premium_annual' ? 'Premium Anual' : 'Free'}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm">{new Date(user.created_at).toLocaleDateString()}</td>
                <td className="px-4 py-3 text-sm">{user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Nunca'}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    user.is_blocked
                      ? 'bg-red-100 text-red-800'
                      : !user.is_verified
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {user.is_blocked
                      ? 'Bloqueado'
                      : !user.is_verified
                      ? 'Não verificado'
                      : 'Ativo'}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleToggleBlock(user.id, user.is_blocked)}
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        user.is_blocked
                          ? 'bg-green-500 text-white hover:bg-green-600'
                          : 'bg-red-500 text-white hover:bg-red-600'
                      }`}
                    >
                      {user.is_blocked ? 'Desbloquear' : 'Bloquear'}
                    </button>
                    <button
                      onClick={() => window.location.href = `/admin/users/${user.id}`}
                      className="px-2 py-1 bg-blue-500 text-white rounded text-xs font-medium hover:bg-blue-600"
                    >
                      Detalhes
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Paginação */}
      <div className="p-4 border-t flex justify-between items-center">
        <div>
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(1);
            }}
            className="px-2 py-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="10">10 por página</option>
            <option value="25">25 por página</option>
            <option value="50">50 por página</option>
            <option value="100">100 por página</option>
          </select>
        </div>
        
        <div className="flex space-x-2">
          <button
            disabled={page === 1}
            onClick={() => setPage(page - 1)}
            className={`px-3 py-1 rounded-md ${
              page === 1
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Anterior
          </button>
          
          <span className="px-3 py-1">
            Página {page} de {totalPages}
          </span>
          
          <button
            disabled={page === totalPages}
            onClick={() => setPage(page + 1)}
            className={`px-3 py-1 rounded-md ${
              page === totalPages
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Próxima
          </button>
        </div>
      </div>
    </div>
  );
};

export default UsersList; 