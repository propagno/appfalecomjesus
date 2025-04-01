import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { EyeIcon, EyeSlashIcon, LockIcon, LogoIcon } from './AuthIcons';
import authService from '../api/authService';
import '../../../styles/auth.css';

const ResetPasswordForm: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [resetCompleted, setResetCompleted] = useState(false);
  const [errors, setErrors] = useState<{ 
    password?: string; 
    confirmPassword?: string;
    token?: string;
  }>({});

  // Extrair token e email dos parâmetros da query
  const queryParams = new URLSearchParams(location.search);
  const token = queryParams.get('token');
  const email = queryParams.get('email');

  useEffect(() => {
    // Verificar se token e email estão presentes
    if (!token || !email) {
      setErrors({
        token: 'Link de recuperação inválido. Solicite um novo link.'
      });
    }
  }, [token, email]);

  const validateForm = () => {
    const newErrors: { 
      password?: string; 
      confirmPassword?: string;
      token?: string;
    } = {};

    if (!token || !email) {
      newErrors.token = 'Link de recuperação inválido. Solicite um novo link.';
    }
    
    if (!password) {
      newErrors.password = 'Por favor, informe sua nova senha';
    } else if (password.length < 6) {
      newErrors.password = 'A senha deve ter pelo menos 6 caracteres';
    }
    
    if (!confirmPassword) {
      newErrors.confirmPassword = 'Por favor, confirme sua nova senha';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'As senhas não conferem';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    
    try {
      await authService.resetPassword({
        token: token!,
        email: email!,
        password,
        password_confirmation: confirmPassword
      });
      
      setResetCompleted(true);
      toast.success('Senha alterada com sucesso!');
    } catch (error: any) {
      if (error.message === 'Network Error') {
        toast.error('Erro de conexão com o servidor. Verifique se o backend está disponível.');
        console.error('Erro de rede:', error);
      } else {
        // Tratar erros de validação
        if (error.response?.data?.errors) {
          const formattedErrors: Record<string, string> = {};
          Object.entries(error.response.data.errors).forEach(([key, value]) => {
            if (Array.isArray(value)) {
              formattedErrors[key] = value[0];
            } else if (typeof value === 'string') {
              formattedErrors[key] = value;
            }
          });
          setErrors(formattedErrors);
        } else {
          const message = error.response?.data?.detail || 
            'Não foi possível alterar a senha. O link pode ter expirado.';
          toast.error(message);
          console.error('Reset password error:', error);
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (resetCompleted) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <LogoIcon className="auth-logo" />
          <h1 className="auth-title">Senha Alterada</h1>
          
          <div className="success-message">
            <svg viewBox="0 0 24 24" width="64" height="64" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="success-icon">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            
            <p>
              Sua senha foi alterada com sucesso!
            </p>
            
            <Link to="/login" className="auth-button">
              Ir para o Login
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <LogoIcon className="auth-logo" />
        <h1 className="auth-title">Redefinir Senha</h1>
        
        {errors.token ? (
          <div className="error-box">
            <p>{errors.token}</p>
            <Link to="/forgot-password" className="auth-button">
              Solicitar novo link
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <LockIcon className="input-icon" />
              <input
                type={showPassword ? 'text' : 'password'}
                className="input-field"
                placeholder="Nova senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
              >
                {showPassword ? <EyeSlashIcon /> : <EyeIcon />}
              </button>
              {errors.password && <div className="error-message">{errors.password}</div>}
            </div>
            
            <div className="input-group">
              <LockIcon className="input-icon" />
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                className="input-field"
                placeholder="Confirme a nova senha"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={isLoading}
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                tabIndex={-1}
              >
                {showConfirmPassword ? <EyeSlashIcon /> : <EyeIcon />}
              </button>
              {errors.confirmPassword && <div className="error-message">{errors.confirmPassword}</div>}
            </div>
            
            <button
              type="submit"
              className="auth-button"
              disabled={isLoading}
            >
              {isLoading ? 'Alterando senha...' : 'Alterar senha'}
            </button>
            
            <div className="auth-links">
              <Link to="/login" className="auth-link">
                Voltar para o login
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default ResetPasswordForm; 