import React, { useEffect } from 'react';
import LoginForm from '../components/LoginForm';
import { useNavigate } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';

/**
 * Página de Login
 */
const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, isAuthStatusChecked } = useAuthContext();
  
  useEffect(() => {
    // Verificar se o usuário já está autenticado
    if (isAuthStatusChecked && isAuthenticated) {
      navigate('/home');
    }
  }, [isAuthStatusChecked, isAuthenticated, navigate]);
  
  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gray-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Entre na sua conta
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <LoginForm />
        </div>
      </div>
    </div>
  );
};

export default LoginPage; 