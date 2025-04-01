import axios, { AxiosError, InternalAxiosRequestConfig, AxiosInstance } from 'axios';
import { API_URLS } from '../../../shared/constants/config';
import {
  User,
  LoginCredentials,
  RegisterData,
  ForgotPasswordData,
  ResetPasswordData,
  AuthResponse,
  UserPreferences,
  ProfileUpdateData
} from '../types';

// Estender o tipo InternalAxiosRequestConfig para incluir a propriedade _retry
interface ExtendedAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

// Configuração do Axios
const api = axios.create({
  baseURL: "/api",
  timeout: 30000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Cache-Control": "no-cache"
  },
});

// Adiciona logs de debug
api.interceptors.request.use(
  (config) => {
    console.debug('Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      baseURL: config.baseURL,
      timeout: config.timeout
    });
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Interceptador de resposta para logging e tratamento de erros
api.interceptors.response.use(
  (response) => {
    // Log detalhado da resposta
    console.debug('Response:', {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
      data: response.data,
      responseTime: response.headers['x-response-time']
    });
    return response;
  },
  (error) => {
    // Log detalhado do erro
    console.error('Response Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      message: error.message,
      data: error.response?.data,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL,
        timeout: error.config?.timeout
      }
    });

    // Tratamento específico para erro 502 (Bad Gateway)
    if (error.response?.status === 502) {
      error.message = 'O serviço de autenticação pode estar indisponível ou mal configurado. Por favor, tente novamente em alguns instantes.';
    }

    return Promise.reject(error);
  }
);

/**
 * Serviço de autenticação
 */
const authService = {
  /**
   * Login do usuário
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      // Criar FormData para enviar as credenciais
      const formData = new FormData();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);

      const response = await api.post<AuthResponse>('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }
  },

  /**
   * Registrar novo usuário
   */
  register: async (userData: RegisterData): Promise<AuthResponse> => {
    console.log('Iniciando registro com dados:', userData);
    try {
      // Se a API espera password_confirmation, mas não foi fornecido
      if (!userData.password_confirmation && userData.password) {
        userData.password_confirmation = userData.password;
      }
      
      // Log para debug
      console.log('Enviando requisição para /auth/register com Content-Type: application/json');
      console.log('Payload:', JSON.stringify(userData));
      
      const response = await api.post<AuthResponse>('/auth/register', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      console.log('Resposta do registro:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro durante o registro:', error);
      // Rethrow para ser tratado no componente
      throw error;
    }
  },

  /**
   * Realizar logout
   */
  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
    localStorage.removeItem('token');
  },

  /**
   * Obtém informações do usuário atual (autenticado)
   */
  getCurrentUser: async (): Promise<User> => {
    try {
      const response = await api.get<{ user: User }>('/auth/user');
      console.log('Resposta completa de /auth/user:', response.data);
      
      if (response.data && response.data.user) {
        const userData = response.data.user;
        console.log('Dados do usuário recebidos:', userData);
        console.log('Tipo do onboarding_completed:', typeof userData.onboarding_completed);
        console.log('Valor do onboarding_completed:', userData.onboarding_completed);
        
        // Garantir que onboarding_completed seja sempre um booleano estrito
        // === true força a comparação de tipo e valor
        const isCompleted = userData.onboarding_completed === true;
        userData.onboarding_completed = isCompleted;
        
        console.log('Valor final do onboarding_completed:', userData.onboarding_completed);
        console.log('Tipo final do onboarding_completed:', typeof userData.onboarding_completed);
        
        return userData;
      } else if ('id' in response.data) {
        // Caso a API retorne o usuário diretamente, sem o campo "user"
        const userData = response.data as unknown as User;
        
        // Também garantir a consistência do tipo aqui
        console.log('Dados diretos do usuário recebidos:', userData);
        console.log('Tipo do onboarding_completed:', typeof userData.onboarding_completed);
        console.log('Valor do onboarding_completed:', userData.onboarding_completed);
        
        // Garantir que onboarding_completed seja sempre um booleano estrito
        userData.onboarding_completed = userData.onboarding_completed === true;
        
        console.log('Valor final do onboarding_completed:', userData.onboarding_completed);
        console.log('Tipo final do onboarding_completed:', typeof userData.onboarding_completed);
        
        return userData;
      }
      
      throw new Error('Formato de resposta inválido');
    } catch (error) {
      console.error('Erro ao obter dados do usuário:', error);
      throw error;
    }
  },

  /**
   * Alias para getCurrentUser para compatibilidade com código existente
   */
  getUser: async (): Promise<User> => {
    return authService.getCurrentUser();
  },

  /**
   * Recuperação de senha
   */
  forgotPassword: async (data: ForgotPasswordData): Promise<void> => {
    await api.post('/auth/forgot-password', data);
  },

  /**
   * Redefinição de senha
   */
  resetPassword: async (data: ResetPasswordData): Promise<void> => {
    await api.post('/auth/reset-password', data);
  },

  /**
   * Verifica se o usuário está autenticado
   */
  isAuthenticated: async (): Promise<boolean> => {
    try {
      const response = await api.get('/auth/check');
      return response.data.authenticated;
    } catch (error) {
      console.error('Error checking authentication:', error);
      return false;
    }
  },

  /**
   * Atualizar preferências do usuário
   */
  updatePreferences: async (preferences: UserPreferences): Promise<void> => {
    await api.post('/auth/preferences', preferences);
  },

  /**
   * Renovar token de acesso
   */
  refreshToken: async (): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>(`/auth/refresh-token`, {});
    return response.data;
  },

  /**
   * Verificar token de email
   */
  verifyEmail: async (token: string): Promise<void> => {
    await api.post<void>(`/auth/verify-email/${token}`, {});
  },
  
  /**
   * Atualizar perfil do usuário
   */
  updateProfile: async (data: ProfileUpdateData): Promise<User> => {
    // Se tiver um arquivo de avatar, use FormData
    if (data.avatar) {
      const formData = new FormData();
      
      // Adicionar apenas os campos com valores
      if (data.name) formData.append('name', data.name);
      if (data.email) formData.append('email', data.email);
      if (data.current_password) formData.append('current_password', data.current_password);
      if (data.password) formData.append('password', data.password);
      if (data.password_confirmation) formData.append('password_confirmation', data.password_confirmation);
      
      // Adicionar avatar
      formData.append('avatar', data.avatar);
      
      const response = await api.post<User>(`/auth/profile`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      return response.data;
    }
    
    // Se não tiver avatar, use JSON normal
    const response = await api.post<User>(`/auth/profile`, data);
    return response.data;
  },
  
  /**
   * Salvar preferências do usuário (onboarding)
   */
  savePreferences: async (preferences: UserPreferences): Promise<UserPreferences> => {
    const response = await api.post<UserPreferences>(`/auth/preferences`, preferences);
    return response.data;
  },

  /**
   * Obter status da assinatura do usuário
   */
  getSubscriptionStatus: async (): Promise<any> => {
    const response = await api.get(`/auth/subscription/status`);
    return response.data;
  },

  /**
   * Verificar a saúde do servidor de autenticação
   */
  checkHealth: async (): Promise<{ status: string; service: string }> => {
    try {
      const response = await api.get('/auth/health');
      return response.data;
    } catch (error) {
      console.error('Error checking auth health:', error);
      throw error;
    }
  }
};

export default authService; 