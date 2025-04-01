import React, { ReactNode, useEffect } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthContext } from '../features/auth/contexts/AuthContext';
import '../styles/auth.css';

// Ícones consistentes com o estilo visual
const HomeIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 2.5L2.5 8.33333V17.5H7.5V11.6667H12.5V17.5H17.5V8.33333L10 2.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BookIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3.33337 16.25C3.33337 15.6975 3.55287 15.1676 3.94357 14.7769C4.33427 14.3862 4.86417 14.1667 5.41671 14.1667H16.6667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5.41671 1.66669H16.6667V18.3334H5.41671C4.86417 18.3334 4.33427 18.1139 3.94357 17.7232C3.55287 17.3325 3.33337 16.8026 3.33337 16.25V3.75002C3.33337 3.19749 3.55287 2.66758 3.94357 2.27688C4.33427 1.88618 4.86417 1.66669 5.41671 1.66669Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BibleIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 5V18.3333" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5 6.66669H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2.5 1.66669V18.3334H17.5V1.66669H2.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M7.5 10H12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const ChatIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M17.5 12.5C17.5 12.942 17.3244 13.366 17.0118 13.6785C16.6993 13.9911 16.2754 14.1667 15.8334 14.1667H5.83335L2.5 17.5V4.16667C2.5 3.72464 2.67559 3.30072 2.98816 2.98816C3.30072 2.67559 3.72464 2.5 4.16668 2.5H15.8334C16.2754 2.5 16.6993 2.67559 17.0118 2.98816C17.3244 3.30072 17.5 3.72464 17.5 4.16667V12.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const AwardIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 12.5C12.3012 12.5 14.1667 10.6345 14.1667 8.33333C14.1667 6.03215 12.3012 4.16667 10 4.16667C7.69881 4.16667 5.83334 6.03215 5.83334 8.33333C5.83334 10.6345 7.69881 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10 12.5V17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M13.3333 15.8333H6.66666" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const SettingsIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 12.5C11.3807 12.5 12.5 11.3807 12.5 10C12.5 8.61929 11.3807 7.5 10 7.5C8.61929 7.5 7.5 8.61929 7.5 10C7.5 11.3807 8.61929 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M16.1667 10C16.1667 10.2333 16.15 10.4667 16.1167 10.6917L17.9667 12.1333C18.1417 12.275 18.1834 12.525 18.075 12.725L16.4084 15.6083C16.3 15.8083 16.0584 15.8833 15.8584 15.8083L13.6834 15C13.2584 15.3167 12.7917 15.575 12.2834 15.7583L11.9084 18.0167C11.8667 18.2333 11.675 18.3333 11.4584 18.3333H8.125C7.90833 18.3333 7.71667 18.2333 7.675 18.0167L7.3 15.7583C6.79167 15.575 6.325 15.3167 5.9 15L3.725 15.8083C3.525 15.8833 3.28333 15.8083 3.175 15.6083L1.50833 12.725C1.4 12.525 1.44167 12.275 1.61667 12.1333L3.46667 10.6917C3.43333 10.4667 3.41667 10.2333 3.41667 10C3.41667 9.76667 3.43333 9.53333 3.46667 9.30833L1.61667 7.86667C1.44167 7.725 1.4 7.475 1.50833 7.275L3.175 4.39167C3.28333 4.19167 3.525 4.11667 3.725 4.19167L5.9 5C6.325 4.68333 6.79167 4.425 7.3 4.24167L7.675 1.98333C7.71667 1.76667 7.90833 1.66667 8.125 1.66667H11.4584C11.675 1.66667 11.8667 1.76667 11.9084 1.98333L12.2834 4.24167C12.7917 4.425 13.2584 4.68333 13.6834 5L15.8584 4.19167C16.0584 4.11667 16.3 4.19167 16.4084 4.39167L18.075 7.275C18.1834 7.475 18.1417 7.725 17.9667 7.86667L16.1167 9.30833C16.15 9.53333 16.1667 9.76667 16.1667 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const LogoutIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M7.5 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V4.16667C2.5 3.72464 2.67559 3.30072 2.98816 2.98816C3.30072 2.67559 3.72464 2.5 4.16667 2.5H7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M13.3334 14.1667L17.5 10L13.3334 5.83337" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M17.5 10H7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

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
    <div className="min-h-screen flex" style={{ background: 'linear-gradient(to right bottom, #CCE4F6, #FFFFFF)' }}>
      {/* Sidebar */}
      <aside 
        className="w-64 hidden md:block"
        style={{ 
          background: 'white',
          boxShadow: '2px 0 10px rgba(0, 0, 0, 0.05)',
          borderRadius: '0 20px 20px 0'
        }}
      >
        <div className="p-6">
          <h1 
            style={{ 
              color: '#333',
              fontFamily: 'Montserrat, sans-serif',
              fontSize: '1.5rem',
              fontWeight: 'bold',
              marginBottom: '2rem',
              textAlign: 'center'
            }}
          >
            FaleComJesus
          </h1>
          
          <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <Link 
              to="/home" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/home') ? '#333' : '#666',
                background: isActive('/home') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/home') ? '#333' : '#888' }}>
                <HomeIcon />
              </span>
              Início
            </Link>
            
            <Link 
              to="/plans" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/plans') ? '#333' : '#666',
                background: isActive('/plans') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/plans') ? '#333' : '#888' }}>
                <BookIcon />
              </span>
              Planos de Estudo
            </Link>
            
            <Link 
              to="/bible" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/bible') ? '#333' : '#666',
                background: isActive('/bible') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/bible') ? '#333' : '#888' }}>
                <BibleIcon />
              </span>
              Explorar Bíblia
            </Link>
            
            <Link 
              to="/chat" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/chat') ? '#333' : '#666',
                background: isActive('/chat') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/chat') ? '#333' : '#888' }}>
                <ChatIcon />
              </span>
              Chat IA
            </Link>
            
            <Link 
              to="/gamification" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/gamification') ? '#333' : '#666',
                background: isActive('/gamification') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/gamification') ? '#333' : '#888' }}>
                <AwardIcon />
              </span>
              Conquistas
            </Link>
            
            <Link 
              to="/settings" 
              style={{ 
                display: 'flex',
                alignItems: 'center',
                padding: '12px 16px',
                borderRadius: '8px',
                textDecoration: 'none',
                color: isActive('/settings') ? '#333' : '#666',
                background: isActive('/settings') ? 'rgba(204, 228, 246, 0.3)' : 'transparent',
                fontFamily: 'Lora, serif',
                transition: 'all 0.3s ease',
                marginTop: '1rem'
              }}
            >
              <span style={{ marginRight: '12px', color: isActive('/settings') ? '#333' : '#888' }}>
                <SettingsIcon />
              </span>
              Configurações
            </Link>
          </nav>
        </div>
      </aside>
      
      {/* Conteúdo principal */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header 
          style={{ 
            background: 'white',
            padding: '1rem 1.5rem',
            borderBottom: '1px solid rgba(204, 228, 246, 0.3)',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.03)',
            marginBottom: '1rem'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2 
              style={{ 
                color: '#333',
                fontSize: '1.25rem',
                fontWeight: 'bold',
                fontFamily: 'Montserrat, sans-serif'
              }}
            >
              {location.pathname === '/home' && 'Início'}
              {location.pathname === '/plans' && 'Planos de Estudo'}
              {location.pathname.startsWith('/bible') && 'Explorar Bíblia'}
              {location.pathname.startsWith('/chat') && 'Chat IA'}
              {location.pathname === '/gamification' && 'Conquistas'}
              {location.pathname === '/settings' && 'Configurações'}
              {location.pathname === '/monetization' && 'Planos Premium'}
            </h2>
            
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span 
                style={{ 
                  marginRight: '1rem', 
                  fontSize: '0.9rem', 
                  color: '#666',
                  fontFamily: 'Lora, serif'
                }}
              >
                Olá, {user?.name}
              </span>
              <button 
                onClick={() => logout()} 
                style={{ 
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: '#666',
                  transition: 'color 0.3s ease',
                  display: 'flex',
                  alignItems: 'center'
                }}
              >
                <span><LogoutIcon /></span>
              </button>
            </div>
          </div>
        </header>
        
        {/* Conteúdo da página */}
        <main className="flex-1 p-6">
          {children || <Outlet />}
        </main>
        
        {/* Footer */}
        <footer 
          style={{ 
            padding: '1rem',
            textAlign: 'center',
            color: '#888',
            fontSize: '0.85rem',
            borderTop: '1px solid rgba(204, 228, 246, 0.3)',
            background: 'white'
          }}
        >
          &copy; {new Date().getFullYear()} FaleComJesus. Todos os direitos reservados.
        </footer>
      </div>
    </div>
  );
};

export default MainLayout; 