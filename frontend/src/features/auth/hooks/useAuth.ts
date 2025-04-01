import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  User,
  LoginCredentials, 
  RegisterData, 
  ForgotPasswordData,
  ResetPasswordData,
  ProfileUpdateData,
  AuthResponse,
  UserPreferences
} from '../types';
import authService from '../api/authService';
import { clearAuth, storeUserData } from '../../../shared/utils/auth';

/**
 * Hook para gerenciar autenticação
 */
export const useAuth = () => {
  const queryClient = useQueryClient();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isAuthStatusChecked, setIsAuthStatusChecked] = useState<boolean>(false);
  
  // Verificar estado inicial de autenticação
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const isUserAuthenticated = await authService.isAuthenticated();
        setIsAuthenticated(isUserAuthenticated);
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setIsAuthStatusChecked(true);
      }
    };

    checkAuthStatus();
  }, []);
  
  // Configuração da query de usuário
  const { 
    data: user,
    error: userError,
    isLoading,
    refetch: refetchUser
  } = useQuery<User>({
    queryKey: ['currentUser'],
    queryFn: authService.getUser,
    retry: 1,
    staleTime: 5 * 60 * 1000, // 5 minutos
    gcTime: 10 * 60 * 1000, // 10 minutos
    enabled: isAuthStatusChecked && isAuthenticated, // Agora só busca se a verificação de autenticação foi concluída
  });
  
  // Efeito para gerenciar os dados do usuário quando a query é bem-sucedida
  useEffect(() => {
    if (user) {
      setIsAuthenticated(true);
      // Armazenar apenas dados não sensíveis do usuário
      storeUserData({
        id: user.id,
        name: user.name,
        email: user.email,
        role: user.role || 'user',
        onboarding_completed: user.onboarding_completed
      });
    }
  }, [user]);
  
  // Login
  const loginMutation = useMutation<AuthResponse, Error, LoginCredentials>({
    mutationFn: (credentials: LoginCredentials) => authService.login(credentials),
    onSuccess: (data) => {
      // Se a API retornar usuário diretamente, armazenar
      if (data.user) {
        storeUserData({
          id: data.user.id,
          name: data.user.name,
          email: data.user.email,
          role: data.user.role || 'user',
          onboarding_completed: data.user.onboarding_completed || false
        });
        queryClient.setQueryData(['currentUser'], data.user);
      }
      setIsAuthenticated(true);
      setIsAuthStatusChecked(true); // Garantir que o status foi verificado
      // Recarregar dados do usuário para garantir que temos informações atualizadas
      refetchUser();
    }
  });
  
  // Registro
  const registerMutation = useMutation<AuthResponse, Error, RegisterData>({
    mutationFn: (data: RegisterData) => authService.register(data),
    onSuccess: (data) => {
      // Se a API retornar usuário diretamente, armazenar
      if (data.user) {
        storeUserData({
          id: data.user.id,
          name: data.user.name,
          email: data.user.email,
          role: data.user.role || 'user',
          onboarding_completed: data.user.onboarding_completed || false
        });
        queryClient.setQueryData(['currentUser'], data.user);
      }
      setIsAuthenticated(true);
      setIsAuthStatusChecked(true); // Garantir que o status foi verificado
      // Recarregar dados do usuário se necessário
      refetchUser();
    }
  });
  
  // Logout
  const logoutMutation = useMutation<void, Error, void>({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      // Limpar dados de autenticação e cache
      clearAuth();
      queryClient.removeQueries({ queryKey: ['currentUser'] });
      setIsAuthenticated(false);
      // Não resetamos isAuthStatusChecked aqui pois já foi verificado
    }
  });
  
  // Atualização de perfil
  const updateProfileMutation = useMutation<User, Error, ProfileUpdateData>({
    mutationFn: (data: ProfileUpdateData) => authService.updateProfile(data),
    onSuccess: (updatedUser) => {
      // Atualizar dados do usuário no cache
      queryClient.setQueryData(['currentUser'], updatedUser);
      
      // Atualizar dados não sensíveis no localStorage
      storeUserData({
        id: updatedUser.id,
        name: updatedUser.name,
        email: updatedUser.email,
        role: updatedUser.role || 'user',
        onboarding_completed: updatedUser.onboarding_completed
      });
    }
  });
  
  // Recuperação de senha
  const forgotPasswordMutation = useMutation<void, Error, ForgotPasswordData>({
    mutationFn: (data: ForgotPasswordData) => authService.forgotPassword(data)
  });
  
  // Reset de senha
  const resetPasswordMutation = useMutation<void, Error, ResetPasswordData>({
    mutationFn: (data: ResetPasswordData) => authService.resetPassword(data)
  });
  
  // Refresh token
  const refreshTokenMutation = useMutation<AuthResponse, Error, void>({
    mutationFn: () => authService.refreshToken(),
    onSuccess: () => {
      // Recarregar dados do usuário após refresh para garantir dados atualizados
      refetchUser();
    },
    onError: () => {
      // Em caso de erro no refresh, deslogar o usuário
      clearAuth();
      setIsAuthenticated(false);
      queryClient.removeQueries({ queryKey: ['currentUser'] });
    }
  });

  // Salvar preferências do usuário (onboarding)
  const savePreferencesMutation = useMutation<UserPreferences, Error, UserPreferences>({
    mutationFn: (data: UserPreferences) => authService.savePreferences(data),
    onSuccess: () => {
      // Após salvar preferências, recarregar dados do usuário
      refetchUser();
    }
  });
  
  // Efeito para lidar com erros na query do usuário
  useEffect(() => {
    if (userError && isAuthenticated) {
      clearAuth();
      setIsAuthenticated(false);
    }
  }, [userError, isAuthenticated]);
  
  return {
    // Estado
    user: user || null,
    isAuthenticated,
    isAuthStatusChecked,
    isLoading,
    error: loginMutation.error || registerMutation.error || userError,
    
    // Ações
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout: logoutMutation.mutateAsync,
    updateProfile: updateProfileMutation.mutateAsync,
    forgotPassword: forgotPasswordMutation.mutateAsync,
    resetPassword: resetPasswordMutation.mutateAsync,
    refreshToken: refreshTokenMutation.mutateAsync,
    savePreferences: savePreferencesMutation.mutateAsync,
    refetchUser,
    
    // Estados de carregamento
    isAuthenticating: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    isUpdatingProfile: updateProfileMutation.isPending,
    isForgotPasswordLoading: forgotPasswordMutation.isPending,
    isResetPasswordLoading: resetPasswordMutation.isPending,
    isRefreshingToken: refreshTokenMutation.isPending,
    isSavingPreferences: savePreferencesMutation.isPending
  };
}; 