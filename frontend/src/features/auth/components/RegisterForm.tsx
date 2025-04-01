import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { EyeIcon, EyeSlashIcon, EnvelopeIcon, LockIcon, UserIcon, LogoIcon } from './AuthIcons';
import authService from '../api/authService';
import '../../../styles/auth.css';

const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{
    name?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});

  const validateForm = () => {
    const newErrors: {
      name?: string;
      email?: string;
      password?: string;
      confirmPassword?: string;
    } = {};
    
    // Validar nome (nome e sobrenome)
    if (!name.trim()) {
      newErrors.name = 'Por favor, informe seu nome';
    } else {
      const nameParts = name.trim().split(' ');
      if (nameParts.length < 2) {
        newErrors.name = 'Por favor, informe nome e sobrenome';
      } else if (!/^[a-zA-ZÀ-ÿ\s\-]+$/.test(name)) {
        newErrors.name = 'O nome contém caracteres inválidos';
      }
    }
    
    // Validar email
    if (!email) {
      newErrors.email = 'Por favor, informe seu e-mail';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Por favor, informe um e-mail válido';
    }
    
    // Validar senha (mínimo 8 caracteres, letras e números)
    if (!password) {
      newErrors.password = 'Por favor, informe sua senha';
    } else if (password.length < 8) {
      newErrors.password = 'A senha deve ter pelo menos 8 caracteres';
    } else if (!/[A-Za-z]/.test(password) || !/[0-9]/.test(password)) {
      newErrors.password = 'A senha deve conter letras e números';
    }
    
    // Validar confirmação de senha
    if (!confirmPassword) {
      newErrors.confirmPassword = 'Por favor, confirme sua senha';
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
      const response = await authService.register({
        name,
        email,
        password,
        password_confirmation: confirmPassword
      });

      // Verifica se o registro foi bem-sucedido
      if (response && (response.message || response.user_id)) {
        toast.success(response.message || 'Cadastro realizado com sucesso!');
        navigate('/login');
      } else if (response && response.access_token) {
        // Caso a API retorne um token diretamente (comportamento antigo)
        localStorage.setItem('token', response.access_token);
        toast.success('Cadastro realizado com sucesso!');
        navigate('/onboarding');
      } else {
        toast.error('Resposta inválida do servidor. Tente novamente.');
      }
    } catch (error: any) {
      if (error.message === 'Network Error') {
        toast.error('Erro de conexão com o servidor. Verifique se o backend está disponível.');
        console.error('Erro de rede:', error);
      } else {
        // Tratar erros de validação (422) e outros erros
        if (error.response?.status === 422) {
          const errorData = error.response.data;
          if (errorData.errors) {
            // Mapear erros do backend para os campos do formulário
            const formattedErrors: Record<string, string> = {};
            Object.entries(errorData.errors).forEach(([key, value]) => {
              switch (key) {
                case 'name':
                  formattedErrors.name = value as string;
                  break;
                case 'email':
                  formattedErrors.email = value as string;
                  break;
                case 'password':
                  formattedErrors.password = value as string;
                  break;
                default:
                  // Se for um erro geral, mostrar no toast
                  if (key === 'general') {
                    toast.error(value as string);
                  }
              }
            });
            setErrors(formattedErrors);
          } else {
            toast.error(errorData.message || 'Erro de validação. Verifique os dados informados.');
          }
        } else if (error.response?.status === 400) {
          // Erro de usuário já existente ou outro erro de negócio
          const errorData = error.response.data;
          if (errorData.errors?.email) {
            setErrors(prev => ({ ...prev, email: errorData.errors.email }));
          }
          toast.error(errorData.message || 'Não foi possível realizar o cadastro.');
        } else {
          // Outros erros (500, etc)
          const message = error.response?.data?.message || 'Ocorreu um erro inesperado. Tente novamente mais tarde.';
          toast.error(message);
        }
        console.error('Erro no registro:', error.response?.data);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <LogoIcon className="auth-logo" />
        <h1 className="auth-title">Inicie sua Jornada Espiritual</h1>
        <p className="auth-subtitle">Comece sua jornada espiritual hoje</p>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <UserIcon className="input-icon" />
            <input
              type="text"
              className="input-field"
              placeholder="Nome"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
            />
            {errors.name && <div className="error-message">{errors.name}</div>}
          </div>
          
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
          
          <div className="input-group">
            <LockIcon className="input-icon" />
            <input
              type={showPassword ? 'text' : 'password'}
              className="input-field"
              placeholder="Senha"
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
              placeholder="Confirme a senha"
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
            {isLoading ? 'Cadastrando...' : 'Cadastrar'}
          </button>
          
          <div className="auth-links">
            <Link to="/login" className="auth-link">
              Já tem uma conta? Faça login
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm; 