import React, { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { useAuth } from '@/features/auth/hooks/useAuth';
import { User } from '@/features/auth/types';

interface UserWithRole extends User {
  role?: 'user' | 'editor' | 'admin' | 'super_admin';
}

export const AdminLayout: React.FC = () => {
  const { isLoading } = useAdmin();
  const { user } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const location = useLocation();
  
  // Converter user para UserWithRole para acessar a propriedade role
  const currentUser = user as UserWithRole;

  const navigation = [
    { name: 'Dashboard', path: '/admin', icon: 'chart-bar' },
    { name: 'Usuários', path: '/admin/users', icon: 'users' },
    { name: 'Configurações', path: '/admin/settings', icon: 'cog' },
    { name: 'Logs', path: '/admin/logs', icon: 'document-text' },
    { name: 'Relatórios', path: '/admin/reports', icon: 'document-report' }
  ];

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  // Função para renderizar ícones baseados em nomes
  const renderIcon = (iconName: string) => {
    // Função simplificada para exemplo - em produção usaria uma biblioteca de ícones
    switch (iconName) {
      case 'chart-bar':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        );
      case 'users':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        );
      case 'cog':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        );
      case 'document-text':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      case 'document-report':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        );
      default:
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        );
    }
  };

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Sidebar para desktop */}
      <aside 
        className={`${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } fixed inset-y-0 z-10 flex flex-col flex-shrink-0 w-64 max-h-screen overflow-hidden transition-all transform bg-white border-r shadow-lg lg:z-auto lg:static lg:shadow-none ${
          !isSidebarOpen && 'lg:translate-x-0 lg:w-20'
        }`}
      >
        {/* Cabeçalho do Sidebar */}
        <div className="flex items-center justify-between flex-shrink-0 p-2">
          <Link to="/admin" className="p-2 text-xl font-semibold text-gray-800">
            {isSidebarOpen ? 'Admin Panel' : 'AP'}
          </Link>
          <button onClick={toggleSidebar} className="p-2 rounded-md lg:hidden">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Links de navegação */}
        <nav className="flex-1 overflow-auto">
          <ul className="p-2 overflow-auto">
            {navigation.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <li key={item.name}>
                  <Link
                    to={item.path}
                    className={`flex items-center p-2 space-x-2 rounded-md hover:bg-gray-100 ${
                      isActive ? 'bg-blue-50 text-blue-600' : 'text-gray-700'
                    }`}
                  >
                    <span className="text-gray-500">{renderIcon(item.icon)}</span>
                    {isSidebarOpen && <span>{item.name}</span>}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Rodapé com informações do usuário */}
        {currentUser && (
          <div className="flex-shrink-0 p-2 border-t max-h-14">
            <div className="flex items-center space-x-2">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                {currentUser.name.charAt(0)}
              </div>
              {isSidebarOpen && (
                <div className="flex flex-col">
                  <span className="text-sm font-medium">{currentUser.name}</span>
                  <span className="text-xs text-gray-500">{currentUser.role || 'user'}</span>
                </div>
              )}
            </div>
          </div>
        )}
      </aside>

      {/* Área de conteúdo principal */}
      <div className="flex flex-col flex-1 max-h-screen overflow-x-hidden overflow-y-auto">
        {/* Cabeçalho móvel (para telas pequenas) */}
        <header className="flex items-center justify-between p-4 bg-white border-b lg:hidden">
          <button onClick={toggleSidebar} className="p-1">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 className="text-lg font-semibold">Admin Panel</h1>
          <span></span> {/* Espaço vazio para balancear o flex */}
        </header>

        {/* Conteúdo principal - renderiza as rotas filhas */}
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}; 