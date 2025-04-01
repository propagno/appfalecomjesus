import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * Componente para proteger rotas que requerem autenticação.
 * Redireciona para a página de login se o usuário não estiver autenticado.
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const location = useLocation();
  const { isAuthenticated, isAuthStatusChecked, isLoading } = useAuthContext();
  
  // Se ainda estiver carregando ou verificando o status, mostra um loader
  if (isLoading || !isAuthStatusChecked) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }
  
  // Se não estiver autenticado, redireciona para login
  if (!isAuthenticated) {
    // Redireciona para login com o caminho atual como state
    // para poder voltar após login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  
  return <>{children}</>;
};

export default ProtectedRoute; 