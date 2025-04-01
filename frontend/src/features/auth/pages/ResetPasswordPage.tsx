import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ResetPasswordForm from '../components/ResetPasswordForm';
import { useAuthContext } from '../contexts/AuthContext';

/**
 * Página de Redefinição de Senha
 */
const ResetPasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, isAuthStatusChecked } = useAuthContext();

  useEffect(() => {
    if (isAuthStatusChecked && isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthStatusChecked, isAuthenticated, navigate]);

  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gray-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Redefinir Senha
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Digite sua nova senha para recuperar o acesso à sua conta
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <ResetPasswordForm />
        </div>
      </div>
    </div>
  );
};

export default ResetPasswordPage; 