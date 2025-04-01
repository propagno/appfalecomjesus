import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ForgotPasswordForm from '../components/ForgotPasswordForm';
import { useAuthContext } from '../contexts/AuthContext';

/**
 * Página de solicitação de recuperação de senha
 */
const ForgotPasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, isAuthStatusChecked } = useAuthContext();
  
  useEffect(() => {
    // Se já estiver autenticado, redireciona para o dashboard
    if (isAuthStatusChecked && isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthStatusChecked, isAuthenticated, navigate]);
  
  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gray-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Recuperar Senha
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Digite seu email para receber instruções
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <ForgotPasswordForm />
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage; 