import React, { useState } from 'react';
import { useAdmin } from '../contexts/AdminContext';
import { UserRole } from '../types';

const UserManagementPage: React.FC = () => {
  const { users, isLoadingUsers, updateUser, deleteUser, error } = useAdmin();

  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [filterText, setFilterText] = useState('');

  // Filtrar usuários com base no texto de busca
  const filteredUsers = users?.filter(
    user =>
      user.name.toLowerCase().includes(filterText.toLowerCase()) ||
      user.email.toLowerCase().includes(filterText.toLowerCase())
  );

  // Manipular mudança de status do usuário
  const handleStatusChange = (userId: string, newStatus: 'active' | 'suspended' | 'disabled') => {
    updateUser({ id: userId, status: newStatus });
  };

  // Manipular mudança de role do usuário
  const handleRoleChange = (userId: string, newRole: UserRole) => {
    updateUser({ id: userId, role: newRole });
  };

  // Manipular exclusão de usuário (com confirmação)
  const handleDeleteUser = (userId: string) => {
    if (
      window.confirm(
        'Tem certeza que deseja remover este usuário? Esta ação não pode ser desfeita.'
      )
    ) {
      deleteUser(userId);
    }
  };

  if (isLoadingUsers) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 text-red-800 rounded-md">
        <h3 className="font-bold">Erro ao carregar usuários</h3>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Gerenciamento de Usuários</h1>
        <div className="relative">
          <input
            type="text"
            placeholder="Buscar usuários..."
            className="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            value={filterText}
            onChange={e => setFilterText(e.target.value)}
          />
          <div className="absolute left-3 top-2.5 text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Tabela de usuários */}
      <div className="overflow-x-auto bg-white rounded-lg shadow">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Usuário
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Email
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Função
              </th>
              <th
                scope="col"
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredUsers && filteredUsers.length > 0 ? (
              filteredUsers.map(user => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="h-10 w-10 flex-shrink-0 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                        {user.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{user.name}</div>
                        <div className="text-sm text-gray-500">
                          Desde {new Date(user.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{user.email}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <select
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        user.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : user.status === 'suspended'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                      }`}
                      value={user.status}
                      onChange={e =>
                        handleStatusChange(
                          user.id,
                          e.target.value as 'active' | 'suspended' | 'disabled'
                        )
                      }
                    >
                      <option value="active">Ativo</option>
                      <option value="suspended">Suspenso</option>
                      <option value="disabled">Desativado</option>
                    </select>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <select
                      className="px-3 py-1 rounded border border-gray-300"
                      value={user.role}
                      onChange={e => handleRoleChange(user.id, e.target.value as UserRole)}
                    >
                      <option value="user">Usuário</option>
                      <option value="editor">Editor</option>
                      <option value="admin">Admin</option>
                      <option value="super_admin">Super Admin</option>
                    </select>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => setSelectedUser(user.id)}
                      className="text-blue-600 hover:text-blue-900 mr-3"
                    >
                      Detalhes
                    </button>
                    <button
                      onClick={() => handleDeleteUser(user.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Remover
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                  {filterText
                    ? 'Nenhum usuário encontrado com os critérios de busca.'
                    : 'Nenhum usuário cadastrado.'}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Modal de detalhes do usuário - pode ser implementado posteriormente */}
      {selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-2xl w-full">
            <h2 className="text-xl font-bold mb-4">Detalhes do Usuário</h2>
            <div className="mb-4">
              {/* Aqui seriam exibidos detalhes adicionais do usuário */}
              <p>Detalhes expandidos do usuário {users?.find(u => u.id === selectedUser)?.name}</p>
            </div>
            <div className="flex justify-end">
              <button
                onClick={() => setSelectedUser(null)}
                className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagementPage;
