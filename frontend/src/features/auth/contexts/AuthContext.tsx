import React, { createContext, ReactNode, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { 
  User, 
  LoginCredentials, 
  RegisterData, 
  ForgotPasswordData, 
  ResetPasswordData, 
  ProfileUpdateData,
  UserPreferences,
  AuthResponse
} from '../types';
import { useToast } from '../../../shared/hooks/useToast';
import { useAuth } from '../hooks/useAuth';
import { startTokenRefreshMonitor, stopTokenRefreshMonitor, clearAuth, getUserData, storeUserData } from '../../../shared/utils/auth';
import authService from '../api/authService';

// Interface para o valor do contexto de autenticação
export interface AuthContextValue {
  // Estado
  user: User | null;
  isAuthenticated: boolean;
  isAuthStatusChecked: boolean;
  isLoading: boolean;
  error: unknown | null;
  
  // Métodos de autenticação
  login: (credentials: LoginCredentials) => Promise<AuthResponse>;
  register: (data: RegisterData) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  updateProfile: (data: ProfileUpdateData) => Promise<User>;
  forgotPassword: (data: ForgotPasswordData) => Promise<void>;
  resetPassword: (data: ResetPasswordData) => Promise<void>;
  savePreferences: (preferences: UserPreferences) => Promise<UserPreferences>;
  
  // Estados de loading
  isLoginLoading: boolean;
  isRegisterLoading: boolean;
  isLogoutLoading: boolean;
  isUpdatingProfile: boolean;
  isForgotPasswordLoading: boolean;
  isResetPasswordLoading: boolean;
  isSavingPreferences: boolean;
}

// Criar o contexto
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// Props para o provedor do contexto
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provedor do contexto de autenticação
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const auth = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  
  // Iniciar o monitoramento para renovação automática do token quando autenticado
  useEffect(() => {
    if (auth.isAuthenticated) {
      // Funções de callback para o monitor de token
      const handleTokenRefreshSuccess = () => {
        auth.refetchUser();
        toast.info('Sua sessão foi renovada automaticamente', { autoClose: 2000 });
      };
      
      const handleTokenRefreshFailure = () => {
        toast.error('Sua sessão expirou. Por favor, faça login novamente.');
        navigate('/login?session=expired');
      };
      
      // Iniciar o monitoramento
      startTokenRefreshMonitor(handleTokenRefreshSuccess, handleTokenRefreshFailure);
      
      // Limpar ao desmontar ou quando o estado de autenticação mudar
      return () => stopTokenRefreshMonitor();
    }
  }, [auth.isAuthenticated, auth.refetchUser, navigate, toast]);
  
  // Gerenciamento de erros de autenticação
  useEffect(() => {
    if (auth.error) {
      const errorMessage = getErrorMessage(auth.error);
      if (errorMessage) {
        toast.error(errorMessage);
      }
    }
  }, [auth.error, toast]);
  
  // Função auxiliar para extrair mensagens de erro
  const getErrorMessage = (error: any): string => {
    if (typeof error === 'string') return error;
    if (error?.message) return error.message;
    if (error?.response?.data?.detail) return error.response.data.detail;
    return 'Ocorreu um erro durante a autenticação. Tente novamente.';
  };
  
  // Wrappers para funções com feedback de toast
  const loginWithFeedback = async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const result = await auth.login(credentials);
      toast.success('Login realizado com sucesso!');
      return result;
    } catch (error) {
      // Erro já será tratado pelo efeito de erro
      throw error;
    }
  };
  
  const registerWithFeedback = async (data: RegisterData): Promise<AuthResponse> => {
    try {
      const result = await auth.register(data);
      toast.success('Registro realizado com sucesso!');
      return result;
    } catch (error) {
      throw error;
    }
  };
  
  const logoutWithFeedback = async () => {
    try {
      await auth.logout();
      toast.info('Logout realizado com sucesso.');
      navigate('/login');
    } catch (error) {
      toast.error('Erro ao realizar logout. Tente novamente.');
      throw error;
    }
  };
  
  const forgotPasswordWithFeedback = async (data: ForgotPasswordData) => {
    try {
      await auth.forgotPassword(data);
      toast.success('Instruções de recuperação de senha enviadas para seu email.');
    } catch (error) {
      throw error;
    }
  };
  
  const resetPasswordWithFeedback = async (data: ResetPasswordData) => {
    try {
      await auth.resetPassword(data);
      toast.success('Senha redefinida com sucesso. Você já pode fazer login.');
      navigate('/login');
    } catch (error) {
      throw error;
    }
  };
  
  const updateProfileWithFeedback = async (data: ProfileUpdateData) => {
    try {
      const result = await auth.updateProfile(data);
      toast.success('Perfil atualizado com sucesso!');
      return result;
    } catch (error) {
      throw error;
    }
  };
  
  const savePreferencesWithFeedback = async (preferences: UserPreferences): Promise<UserPreferences> => {
    try {
      const result = await auth.savePreferences(preferences);
        toast.success('Preferências salvas com sucesso!');
      return result;
    } catch (error) {
      toast.error('Erro ao salvar preferências. Tente novamente.');
      throw error;
    }
  };
  
  // Valor do contexto com as funções aprimoradas
  const contextValue: AuthContextValue = {
    user: auth.user,
    isAuthenticated: auth.isAuthenticated,
    isAuthStatusChecked: auth.isAuthStatusChecked,
    isLoading: auth.isLoading,
    error: auth.error,
    
    login: loginWithFeedback,
    register: registerWithFeedback,
    logout: logoutWithFeedback,
    updateProfile: updateProfileWithFeedback,
    forgotPassword: forgotPasswordWithFeedback,
    resetPassword: resetPasswordWithFeedback,
    savePreferences: savePreferencesWithFeedback,
    
    isLoginLoading: auth.isAuthenticating,
    isRegisterLoading: auth.isRegistering,
    isLogoutLoading: auth.isLoggingOut,
    isUpdatingProfile: auth.isUpdatingProfile,
    isForgotPasswordLoading: auth.isForgotPasswordLoading,
    isResetPasswordLoading: auth.isResetPasswordLoading,
    isSavingPreferences: auth.isSavingPreferences
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Hook para utilizar o contexto de autenticação
 */
export const useAuthContext = (): AuthContextValue => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuthContext deve ser usado dentro de um AuthProvider');
  }
  
  return context;
};

export default AuthContext; 