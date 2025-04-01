import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { EnvelopeIcon, LogoIcon } from './AuthIcons';
import authService from '../api/authService';
import '../../../styles/auth.css';

const ForgotPasswordForm: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [errors, setErrors] = useState<{ email?: string }>({});

  const validateForm = () => {
    const newErrors: { email?: string } = {};
    
    if (!email) {
      newErrors.email = 'Por favor, informe seu e-mail';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Por favor, informe um e-mail válido';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    
    try {
      await authService.forgotPassword({ email });
      setEmailSent(true);
      toast.success('Enviamos um link de recuperação para seu e-mail!');
    } catch (error: any) {
      if (error.message === 'Network Error') {
        toast.error('Erro de conexão com o servidor. Verifique se o backend está disponível.');
        console.error('Erro de rede:', error);
      } else {
        const message = error.response?.data?.detail || 
          'Não foi possível enviar o e-mail de recuperação. Tente novamente.';
        toast.error(message);
        console.error('Recuperação de senha error:', error);
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (emailSent) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <LogoIcon className="auth-logo" />
          <h1 className="auth-title">E-mail Enviado</h1>
          
          <div className="success-message">
            <svg viewBox="0 0 24 24" width="64" height="64" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="success-icon">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            
            <p>
              Enviamos um link de recuperação para:<br/>
              <strong>{email}</strong>
            </p>
            
            <p>
              Verifique sua caixa de entrada e spam. O link expirará em 60 minutos.
            </p>
            
            <div className="auth-links">
              <Link to="/login" className="auth-link">
                Voltar para o login
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <LogoIcon className="auth-logo" />
        <h1 className="auth-title">Recuperar Senha</h1>
        <p className="auth-description">
          Informe seu e-mail e enviaremos um link para você recuperar sua senha.
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <EnvelopeIcon className="input-icon" />
            <input
              type="email"
              className="input-field"
              placeholder="E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
            />
            {errors.email && <div className="error-message">{errors.email}</div>}
          </div>
          
          <button
            type="submit"
            className="auth-button"
            disabled={isLoading}
          >
            {isLoading ? 'Enviando...' : 'Enviar link'}
          </button>
          
          <div className="auth-links">
            <Link to="/login" className="auth-link">
              Voltar para o login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ForgotPasswordForm; 