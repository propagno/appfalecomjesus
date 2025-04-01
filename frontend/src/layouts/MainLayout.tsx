import React, { ReactNode, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../features/auth/contexts/AuthContext';

interface MainLayoutProps {
  children?: ReactNode;
}

/**
 * Layout principal da aplicação para páginas protegidas
 * Inclui sidebar, header e área de conteúdo
 */
const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthContext();
  
  // Verificar se o usuário completou o onboarding
  useEffect(() => {
    // Verificar se o usuário existe e se não completou o onboarding
    if (user && user.onboarding_completed === false) {
      console.log('MainLayout: Usuário não completou o onboarding. Redirecionando para /onboarding');
      // Redirecionar para a página de onboarding
      navigate('/onboarding');
    }
  }, [user, navigate]);
  
  // Verificar qual item do menu está ativo
  const isActive = (path: string) => {
    return location.pathname.startsWith(path);
  };
  
  // Se o usuário não tiver completado o onboarding, não renderizar o layout
  if (user && user.onboarding_completed === false) {
    return null; // Não renderiza nada enquanto redireciona
  }
  
  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="w-64 bg-blue-700 text-white hidden md:block">
        <div className="p-4">
          <h1 className="text-2xl font-bold mb-8">FaleComJesus</h1>
          
          <nav className="space-y-2">
            <Link 
              to="/home" 
              className={`flex items-center p-3 rounded-lg ${isActive('/home') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">home</span>
              Início
            </Link>
            
            <Link 
              to="/plans" 
              className={`flex items-center p-3 rounded-lg ${isActive('/plans') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">book</span>
              Planos de Estudo
            </Link>
            
            <Link 
              to="/bible" 
              className={`flex items-center p-3 rounded-lg ${isActive('/bible') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">menu_book</span>
              Explorar Bíblia
            </Link>
            
            <Link 
              to="/chat" 
              className={`flex items-center p-3 rounded-lg ${isActive('/chat') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">chat</span>
              Chat IA
            </Link>
            
            <Link 
              to="/gamification" 
              className={`flex items-center p-3 rounded-lg ${isActive('/gamification') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">emoji_events</span>
              Conquistas
            </Link>
            
            <Link 
              to="/settings" 
              className={`flex items-center p-3 rounded-lg ${isActive('/settings') ? 'bg-blue-800 font-medium' : 'hover:bg-blue-600'}`}
            >
              <span className="material-icons mr-3">settings</span>
              Configurações
            </Link>
          </nav>
        </div>
      </aside>
      
      {/* Conteúdo principal */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm p-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-800">
              {location.pathname === '/home' && 'Início'}
              {location.pathname === '/plans' && 'Planos de Estudo'}
              {location.pathname.startsWith('/bible') && 'Explorar Bíblia'}
              {location.pathname.startsWith('/chat') && 'Chat IA'}
              {location.pathname === '/gamification' && 'Conquistas'}
              {location.pathname === '/settings' && 'Configurações'}
              {location.pathname === '/monetization' && 'Planos Premium'}
            </h2>
            
            <div className="flex items-center">
              <span className="mr-2 text-sm text-gray-600">Olá, {user?.name}</span>
              <button 
                onClick={() => logout()} 
                className="text-gray-600 hover:text-red-600"
              >
                <span className="material-icons">logout</span>
              </button>
            </div>
          </div>
        </header>
        
        {/* Conteúdo da página */}
        <main className="flex-1 p-6">
          {children || <Outlet />}
        </main>
        
        {/* Footer */}
        <footer className="bg-white p-4 border-t">
          <div className="text-center text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} FaleComJesus. Todos os direitos reservados.
          </div>
        </footer>
      </div>
    </div>
  );
};

export default MainLayout; 