import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { EyeIcon, EyeSlashIcon, EnvelopeIcon, LockIcon, LogoIcon } from './AuthIcons';
import authService from '../api/authService';
import { checkAuthConnection, tryConnectWithRetry, diagnosticAuth } from '../api/apiCheck';
import '../../../styles/auth.css';

const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingConnection, setIsCheckingConnection] = useState(false);
  const [serverStatus, setServerStatus] = useState<'checking' | 'online' | 'offline' | 'unknown'>('checking');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [connectionDetails, setConnectionDetails] = useState<string>('');
  const [diagnosticResults, setDiagnosticResults] = useState<string>('');
  
  // Estado para armazenar o destino após autenticação bem-sucedida
  const [authSuccess, setAuthSuccess] = useState(false);
  const [redirectDestination, setRedirectDestination] = useState<string | null>(null);

  // Verificar conexão ao carregar o componente
  useEffect(() => {
    const verifyConnection = async () => {
      try {
        setServerStatus('checking');
        
        // Usar o método mais robusto com retentativas
        const connectionResult = await tryConnectWithRetry(2); // Tenta no máximo 2 vezes
        
        setServerStatus(connectionResult.success ? 'online' : 'offline');
        setConnectionDetails(connectionResult.details || '');
        
        if (!connectionResult.success) {
          console.warn('Aviso: Servidor de autenticação não está respondendo', connectionResult);
          
          // Se falhar, tenta diagnóstico automático para encontrar rotas alternativas
          const diagnostic = await diagnosticAuth();
          console.info('Diagnóstico de rotas:', diagnostic);
          
          if (diagnostic.summary) {
            setConnectionDetails(prev => `${prev}\n\nDiagnóstico: ${diagnostic.summary}`);
          }
        }
      } catch (error) {
        console.error('Erro ao verificar status do servidor:', error);
        setServerStatus('offline');
      }
    };

    verifyConnection();
  }, []);

  // useEffect para redirecionamento após autenticação bem-sucedida
  useEffect(() => {
    if (authSuccess && redirectDestination) {
      console.log(`Executando redirecionamento FORÇADO para ${redirectDestination}`);
      const timeoutId = setTimeout(() => {
        window.location.href = redirectDestination;
      }, 500);
      return () => clearTimeout(timeoutId);
    }
  }, [authSuccess, redirectDestination]);

  const validateForm = () => {
    const newErrors: { email?: string; password?: string } = {};
    
    if (!email) {
      newErrors.email = 'Por favor, informe seu e-mail';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Por favor, informe um e-mail válido';
    }
    
    if (!password) {
      newErrors.password = 'Por favor, informe sua senha';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleTestConnection = async () => {
    setIsCheckingConnection(true);
    setDiagnosticResults('');
    
    try {
      // Primeiro tenta a conexão normal
      const result = await tryConnectWithRetry(2);
      
      if (result.success) {
        toast.success(result.message);
        setServerStatus('online');
        setConnectionDetails(result.details || '');
      } else {
        toast.error(result.message);
        setServerStatus('offline');
        setConnectionDetails(result.details || '');
        
        // Se falhar, faz diagnóstico completo
        toast.loading('Executando diagnóstico avançado...', { id: 'diagnostic' });
        const diagnostic = await diagnosticAuth();
        toast.dismiss('diagnostic');
        
        // Formatar resultados do diagnóstico para exibição
        const formattedResults = Object.entries(diagnostic.routes)
          .map(([route, result]) => 
            `${route}: ${result.success ? '✅' : '❌'} ${result.statusCode || '-'}`
          )
          .join('\n');
        
        setDiagnosticResults(`${diagnostic.summary}\n\n${formattedResults}`);
        
        // Se encontrou uma rota que funciona, atualiza status
        const workingRoute = Object.values(diagnostic.routes).some(r => r.success);
        if (workingRoute) {
          setServerStatus('online');
          toast.success('Encontrada uma rota alternativa funcional!');
        }
      }
    } catch (error) {
      toast.error('Erro ao testar conexão');
      console.error('Erro ao testar conexão:', error);
      setServerStatus('offline');
    } finally {
      setIsCheckingConnection(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    if (serverStatus === 'offline') {
      toast.error('O servidor parece estar indisponível no momento. Tente novamente mais tarde ou verifique sua conexão.');
      return;
    }
    
    setIsLoading(true);
    
    try {
      console.log('Iniciando login...');
      const response = await authService.login({ email, password });
      console.log('Login realizado com sucesso. Resposta:', response);
      
      // Salva o token e informações do usuário
      if (response && response.access_token) {
        localStorage.setItem('token', response.access_token);
        toast.success('Login realizado com sucesso!');
        
        // Verifica se o usuário possui dados e se já completou o onboarding
        if (response.user) {
          console.log('Dados do usuário recebidos diretamente no login:', response.user);
          
          // Armazena os dados do usuário localmente
          const userData = {
            id: response.user.id,
            name: response.user.name,
            email: response.user.email,
            onboarding_completed: response.user.onboarding_completed || false
          };
          
          localStorage.setItem('user', JSON.stringify(userData));
          console.log('Status de onboarding do usuário:', userData.onboarding_completed);
          
          // Definir destino de redirecionamento
          if (userData.onboarding_completed === true) {
            console.log('Preparando redirecionamento FORÇADO para /home - onboarding confirmado como true');
            setRedirectDestination('/home');
            setAuthSuccess(true);
          } else {
            console.log('Preparando redirecionamento FORÇADO para /onboarding - onboarding não é true');
            setRedirectDestination('/onboarding');
            setAuthSuccess(true);
          }
        } else {
          console.log('Dados do usuário não recebidos no login. Buscando dados do usuário...');
          
          // Se não tiver informações do usuário, busca-as primeiro
          try {
            const userData = await authService.getCurrentUser();
            console.log('Dados do usuário obtidos após login:', userData);
            
            localStorage.setItem('user', JSON.stringify({
              id: userData.id,
              name: userData.name,
              email: userData.email,
              onboarding_completed: userData.onboarding_completed || false
            }));
            
            console.log('Status de onboarding do usuário:', userData.onboarding_completed);
            
            // Definir destino de redirecionamento
            if (userData.onboarding_completed === true) {
              console.log('Preparando redirecionamento FORÇADO para /home - onboarding confirmado como true');
              setRedirectDestination('/home');
              setAuthSuccess(true);
            } else {
              console.log('Preparando redirecionamento FORÇADO para /onboarding - onboarding não é true');
              setRedirectDestination('/onboarding');
              setAuthSuccess(true);
            }
          } catch (userError) {
            console.error('Erro ao obter dados do usuário:', userError);
            console.log('Redirecionando para /onboarding por padrão');
            setRedirectDestination('/onboarding');
            setAuthSuccess(true);
          }
        }
      } else {
        toast.error('Resposta inválida do servidor. Tente novamente.');
      }
    } catch (error: any) {
      // Tratando especificamente erros de rede (CORS e conexão)
      if (error.message === 'Network Error' || error.code === 'ECONNABORTED' || 
          (error.response && (error.response.status === 504 || error.response.status === 502))) {
        toast.error('Servidor está demorando para responder ou pode estar indisponível. Tente novamente em alguns instantes.');
        console.error('Erro de conexão:', error);
        setServerStatus('offline');
        
        // Tentar detectar o problema específico
        const result = await checkAuthConnection();
        setConnectionDetails(result.details || '');
        
        // Executar diagnóstico em caso de erros graves
        if (error.response && error.response.status === 502) {
          const diagnostic = await diagnosticAuth();
          if (diagnostic.summary) {
            setConnectionDetails(prev => `${prev}\n\nDiagnóstico: ${diagnostic.summary}`);
          }
        }
      } else if (error.response?.status === 422) {
        // Erro de validação
        const errorDetail = error.response.data.detail;
        if (typeof errorDetail === 'string') {
          toast.error(errorDetail);
        } else if (Array.isArray(errorDetail)) {
          // Tratar erros de validação do FastAPI
          const newErrors: { [key: string]: string } = {};
          errorDetail.forEach(err => {
            if (err.loc && err.loc[1]) {
              newErrors[err.loc[1]] = err.msg;
            }
          });
          setErrors(newErrors);
        }
      } else if (error.response?.status === 401) {
        toast.error('Email ou senha incorretos');
      } else {
        const message = error.response?.data?.detail || 'Não foi possível realizar o login. Verifique suas credenciais.';
        if (typeof message === 'string') {
          toast.error(message);
        }
        console.error('Login error:', error);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <LogoIcon className="auth-logo" />
        <h1 className="auth-title">Sua Jornada Diária com a Palavra</h1>
        
        {serverStatus === 'offline' && (
          <div className="server-status-warning">
            <div className="status-indicator offline"></div>
            <p>Servidor indisponível. Os serviços podem estar em manutenção ou com problemas de acesso.</p>
            {connectionDetails && (
              <p className="connection-details">{connectionDetails}</p>
            )}
            {diagnosticResults && (
              <div className="diagnostic-results">
                <p>Resultados do diagnóstico:</p>
                <pre>{diagnosticResults}</pre>
              </div>
            )}
          </div>
        )}
        
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
          
          <button
            type="submit"
            className="auth-button"
            disabled={isLoading || serverStatus === 'checking'}
          >
            {isLoading ? 'Entrando...' : 'Entrar'}
          </button>        
          
          <div className="auth-links">
            <Link to="/forgot-password" className="auth-link">
              Esqueceu a senha?
            </Link>
            <Link to="/register" className="auth-link">
              Ainda não tem conta? Cadastre-se
            </Link>
          </div>
          
        </form>
        
        <div className="social-login">
          <div className="social-divider">
            <span>Ou entre com</span>
          </div>
          
          <div className="social-buttons">
            <button className="social-button" type="button" disabled={isLoading}>
              <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12
                  s5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24
                  s8.955,20,20,20s20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z" fill="#FFC107"/>
                <path d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657
                  C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z" fill="#FF3D00"/>
                <path d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36
                  c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z" fill="#4CAF50"/>
                <path d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571
                  c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z" fill="#1976D2"/>
              </svg>
              <span style={{ marginLeft: '8px' }}>Google</span>
            </button>
            
            <button className="social-button" type="button" disabled={isLoading}>
              <svg width="20" height="20" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill="#3F51B5" d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5
                  V37z"/>
                <path fill="#FFFFFF" d="M34.368,25H31v13h-5V25h-3v-4h3v-2.41c0.002-3.508,1.459-5.59,5.592-5.59H35v4h-2.287
                  C31.104,17,31,17.6,31,18.723V21h4L34.368,25z"/>
              </svg>
              <span style={{ marginLeft: '8px' }}>Facebook</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm; 