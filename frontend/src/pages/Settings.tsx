import React from 'react';
import { useAuthContext } from '../features/auth/contexts/AuthContext';

/**
 * Página de configurações do usuário
 */
const SettingsPage: React.FC = () => {
  const { user } = useAuthContext();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Configurações</h1>
      
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Perfil do Usuário</h2>
        
        <div className="mb-4">
          <p className="text-gray-600">Nome</p>
          <p className="font-medium">{user?.name}</p>
        </div>
        
        <div className="mb-4">
          <p className="text-gray-600">Email</p>
          <p className="font-medium">{user?.email}</p>
        </div>
        
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Editar Perfil
        </button>
      </div>
      
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Segurança</h2>
        
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mb-4">
          Alterar Senha
        </button>
        
        <button className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">
          Verificar Dispositivos Conectados
        </button>
      </div>
      
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Preferências</h2>
        
        <div className="mb-4">
          <label className="flex items-center">
            <input type="checkbox" className="form-checkbox h-5 w-5 text-blue-600" />
            <span className="ml-2 text-gray-700">Receber notificações por email</span>
          </label>
        </div>
        
        <div className="mb-4">
          <label className="flex items-center">
            <input type="checkbox" className="form-checkbox h-5 w-5 text-blue-600" />
            <span className="ml-2 text-gray-700">Receber lembretes diários</span>
          </label>
        </div>
        
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Salvar Preferências
        </button>
      </div>
      
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 text-red-600">Zona de Perigo</h2>
        
        <button className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
          Excluir Conta
        </button>
      </div>
    </div>
  );
};

export default SettingsPage; 