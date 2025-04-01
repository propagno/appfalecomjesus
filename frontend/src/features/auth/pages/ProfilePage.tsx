import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';
import ProfileForm from '../components/ProfileForm';
import Card from '../../../shared/components/ui/Card';

/**
 * Página de perfil do usuário
 */
const ProfilePage: React.FC = () => {
  const { user, isAuthenticated, isAuthStatusChecked, isLoading } = useAuthContext();
  
  // Se não estiver autenticado, redireciona para o login
  if (isAuthStatusChecked && !isAuthenticated && !isLoading) {
    return <Navigate to="/login" replace />;
  }
  
  // Se estiver carregando, mostra spinner
  if (isLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-spirit-blue-600"></div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen py-12 container mx-auto px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold leading-tight text-gray-900 mb-8">
          Seu Perfil
        </h1>
        
        <Card 
          className="bg-white shadow rounded-lg divide-y divide-gray-200 p-6 rounded-lg shadow-sm"
        >
          <ProfileForm user={user} />
        </Card>
        
        <div className="mt-4 text-center text-sm text-gray-500">
          Mantenha seus dados atualizados para uma melhor experiência.
        </div>
      </div>
    </div>
  );
};

export default ProfilePage; 