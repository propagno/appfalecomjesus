import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

interface UseProtectedRouteOptions {
  requiredRole?: string | string[];
  redirectTo?: string;
  onlyUnauthenticated?: boolean;
}

/**
 * Hook para proteger rotas que requerem autenticação ou roles específicas.
 * Redireciona usuários não autorizados para o login ou outra rota especificada.
 * 
 * @param options Opções de configuração
 * @returns Um objeto contendo o estado de carregamento, autenticação e autorização
 */
export const useProtectedRoute = (options: UseProtectedRouteOptions = {}) => {
  const { 
    requiredRole, 
    redirectTo = '/login', 
    onlyUnauthenticated = false 
  } = options;
  
  const { isAuthenticated, isAuthStatusChecked, user, isLoading } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();

  // Verificar se o usuário tem a role necessária
  const hasRequiredRole = (): boolean => {
    if (!requiredRole || !user) return false;
    
    const userRole = user.role || 'user';
    
    if (Array.isArray(requiredRole)) {
      return requiredRole.includes(userRole);
    }
    
    return requiredRole === userRole;
  };

  // Efeito para verificar autenticação e redirecionamento
  useEffect(() => {
    // Aguardar verificação completa do status de autenticação
    if (isLoading || !isAuthStatusChecked) return;
    
    // Caso 1: Rota só para usuários não autenticados (ex: login, registro)
    if (onlyUnauthenticated && isAuthenticated) {
      navigate('/home');
      return;
    }
    
    // Caso 2: Rota protegida que requer autenticação
    if (!onlyUnauthenticated && !isAuthenticated) {
      // Salvar a URL atual para redirecionamento após login
      const returnUrl = encodeURIComponent(location.pathname + location.search);
      navigate(`${redirectTo}?returnUrl=${returnUrl}`);
      return;
    }
    
    // Caso 3: Rota que requer role específica
    if (requiredRole && !hasRequiredRole()) {
      navigate('/unauthorized', { replace: true });
      return;
    }
  }, [isAuthenticated, isAuthStatusChecked, isLoading, navigate, redirectTo, onlyUnauthenticated, location, requiredRole]);

  return {
    isLoading,
    isAuthenticated,
    isAuthStatusChecked,
    isAuthorized: !requiredRole || hasRequiredRole(),
    user
  };
};

export default useProtectedRoute; 