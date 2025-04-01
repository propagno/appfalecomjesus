/**
 * Representa um usuário autenticado no sistema
 */
export interface User {
  id: string;
  name: string;
  email: string;
  avatar_url?: string;
  role?: string;
  created_at: string;
  updated_at: string;
  onboarding_completed: boolean;
  subscription?: {
    plan_type: 'Free' | 'Premium';
    status: 'active' | 'inactive' | 'canceled';
    expiration_date?: string;
  };
}

/**
 * Estado atual da autenticação
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Credenciais para login
 */
export interface LoginCredentials {
  email: string;
  password: string;
  remember_me?: boolean;
}

/**
 * Dados para registro de novo usuário
 */
export interface RegisterData {
  name: string;
  email: string;
  password: string;
  password_confirmation: string;
}

/**
 * Dados para solicitação de recuperação de senha
 */
export interface ForgotPasswordData {
  email: string;
}

/**
 * Dados para redefinição de senha
 */
export interface ResetPasswordData {
  token: string;
  email: string;
  password: string;
  password_confirmation: string;
}

/**
 * Dados para atualização de perfil
 */
export interface ProfileUpdateData {
  name?: string;
  email?: string;
  password?: string;
  password_confirmation?: string;
  current_password?: string;
  avatar?: File;
}

/**
 * Resposta da API contendo tokens
 */
export interface AuthTokens {
  access_token: string;
  refresh_token?: string;
  expires_in: number;
  token_type?: string;
}

/**
 * Dados do usuário com tokens de autenticação
 */
export interface AuthResponse {
  user?: User;
  tokens?: AuthTokens;
  // Campos para compatibilidade com implementação existente
  access_token?: string;
  token_type?: string;
  expires_in?: number;
  // Campos para compatibilidade com resposta de registro
  user_id?: string;
  message?: string;
}

export interface UserPreferences {
  objectives: string[];
  bible_experience_level: 'iniciante' | 'intermediario' | 'avancado';
  content_preferences: string[];
  preferred_time: 'manha' | 'tarde' | 'noite';
  onboarding_completed: boolean;
}

export type AuthError = {
  message: string;
  status?: number;
  errors?: Record<string, string[]>;
}; 