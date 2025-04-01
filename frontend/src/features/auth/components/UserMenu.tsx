import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

// Ícones inline
const UserIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const LogoutIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
  </svg>
);

/**
 * Menu de usuário com opções de perfil e logout
 */
const UserMenu: React.FC = () => {
  const { user, logout } = useAuthContext();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  
  // Fecha o menu quando clica fora dele
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);
  
  // Se não tiver usuário, não mostra nada
  if (!user) return null;
  
  // Manipula logout
  const handleLogout = () => {
    logout();
    setIsOpen(false);
  };
  
  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 focus:outline-none focus:ring-2 focus:ring-spirit-blue-300 focus:ring-opacity-50 rounded-full"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <div className="w-9 h-9 rounded-full overflow-hidden bg-spirit-earth-100 flex items-center justify-center border-2 border-spirit-earth-200">
          {user.avatar_url ? (
            <img 
              src={user.avatar_url} 
              alt={user.name} 
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-spirit-blue-500 font-heading font-medium">
              {user.name?.charAt(0).toUpperCase() || 'U'}
            </span>
          )}
        </div>
        <span className="text-sm font-medium text-spirit-earth-800 hidden md:block font-body">
          {user.name}
        </span>
        <svg
          className="h-5 w-5 text-spirit-earth-500 hidden md:block"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>
      
      {/* Menu dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 rounded-lg shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 z-50 border border-spirit-earth-100">
          <div className="px-4 py-3 border-b border-spirit-earth-100">
            <p className="text-sm font-medium text-spirit-earth-900 font-heading">{user.name}</p>
            <p className="text-xs text-spirit-earth-600 truncate font-body">{user.email}</p>
          </div>
          
          <Link
            to="/profile"
            className="flex items-center px-4 py-2 text-sm text-spirit-earth-700 hover:bg-spirit-blue-50 font-body transition-colors"
            onClick={() => setIsOpen(false)}
          >
            <UserIcon />
            <span className="ml-3">Meu perfil</span>
          </Link>
          
          <button
            onClick={handleLogout}
            className="flex items-center w-full text-left px-4 py-2 text-sm text-spirit-earth-700 hover:bg-spirit-blue-50 font-body transition-colors"
          >
            <LogoutIcon />
            <span className="ml-3">Sair</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu; 