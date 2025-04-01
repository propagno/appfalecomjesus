/**
 * Utilitários para autenticação e gerenciamento de JWT
 */
import { authApi } from '../services/api';

// Constantes
const USER_DATA_KEY = 'user_data'; // Chave para armazenar dados não sensíveis do usuário

// Tipos
interface JwtPayload {
  exp?: number;
  sub?: string;
  role?: string;
}

interface UserData {
  id: string;
  name: string;
  email: string;
  role?: string;
  onboarding_completed?: boolean;
  is_premium?: boolean;
}

let refreshTokenTimer: number | null = null;

/**
 * Verifica se o usuário está autenticado
 * Observação: Apenas verifica dados do usuário local, a verificação real
 * ocorre no servidor via cookie HttpOnly.
 */
export function isAuthenticated(): boolean {
  const userData = getUserData();
  return userData !== null;
}

/**
 * Armazena dados não sensíveis do usuário 
 */
export function storeUserData(userData: UserData): void {
  if (!userData) return;
  
  localStorage.setItem(USER_DATA_KEY, JSON.stringify(userData));
}

/**
 * Recupera os dados do usuário do armazenamento local
 */
export function getUserData(): UserData | null {
  try {
    const userData = localStorage.getItem(USER_DATA_KEY);
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error('Erro ao recuperar dados do usuário:', error);
    return null;
  }
}

/**
 * Recupera o ID do usuário logado
 */
export function getUserId(): string | null {
  const userData = getUserData();
  return userData?.id || null;
}

/**
 * Verifica se o usuário tem determinada role
 */
export function hasRole(role: string | string[]): boolean {
  const userData = getUserData();
  
  if (!userData || !userData.role) return false;
  
  if (Array.isArray(role)) {
    return role.includes(userData.role);
  }
  
  return userData.role === role;
}

/**
 * Verifica se o usuário é admin
 */
export function isAdmin(): boolean {
  return hasRole(['admin', 'super_admin']);
}

/**
 * Remove todos os dados de autenticação local
 */
export function clearAuth(): void {
  localStorage.removeItem(USER_DATA_KEY);
  stopTokenRefreshMonitor();
}

/**
 * Renova o token de acesso usando o refresh token
 */
export async function refreshToken(): Promise<boolean> {
  try {
    const response = await authApi.post('/refresh-token', {}, {
      withCredentials: true
    });
    
    // Se a resposta foi bem-sucedida, o servidor já configurou os novos cookies
    return response.status === 200;
  } catch (error) {
    console.error('Falha ao renovar token:', error);
    return false;
  }
}

/**
 * Inicia o monitoramento para renovação automática do token
 */
export function startTokenRefreshMonitor(
  onSuccess?: () => void,
  onFailure?: () => void
): void {
  // Para o monitor existente se houver
  stopTokenRefreshMonitor();
  
  // Verificação a cada 5 minutos
  refreshTokenTimer = window.setInterval(async () => {
    try {
      // Como não temos acesso ao token (HttpOnly cookie), verificamos 
      // com uma chamada ao endpoint de verificação
      const response = await authApi.get('/verify-token', { 
        withCredentials: true 
      });
      
      if (response.status === 200) {
        const needsRefresh = response.data?.needsRefresh === true;
        
        if (needsRefresh) {
          const success = await refreshToken();
          
          if (success && onSuccess) {
            onSuccess();
          } else if (!success && onFailure) {
            onFailure();
            clearAuth();
          }
        }
      }
    } catch (error) {
      console.error('Erro na verificação do token:', error);
      // Tentar refresh automaticamente em caso de erro 401
      if ((error as any)?.response?.status === 401) {
        try {
          const success = await refreshToken();
          if (success && onSuccess) {
            onSuccess();
          } else if (!success && onFailure) {
            onFailure();
            clearAuth();
          }
        } catch (refreshError) {
          console.error('Falha no refresh de token:', refreshError);
          if (onFailure) {
            onFailure();
          }
          clearAuth();
        }
      } else {
        if (onFailure) {
          onFailure();
        }
        clearAuth();
      }
    }
  }, 5 * 60 * 1000); // 5 minutos
}

/**
 * Para o monitoramento de renovação do token
 */
export function stopTokenRefreshMonitor(): void {
  if (refreshTokenTimer !== null) {
    window.clearInterval(refreshTokenTimer);
    refreshTokenTimer = null;
  }
}

/**
 * Verifica se o email é válido
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Verifica se a senha atende aos requisitos de segurança
 */
export function isValidPassword(password: string): boolean {
  return password.length >= 8;
}

/**
 * Obtém a mensagem de erro para senha inválida
 */
export function getPasswordValidationError(password: string): string | null {
  if (!password) return 'A senha é obrigatória';
  if (password.length < 8) return 'A senha deve ter pelo menos 8 caracteres';
  return null;
}

/**
 * Calcula o tempo de expiração com base na resposta da API de autenticação
 */
export function calculateTokenExpiry(expiresIn: number): number {
  // expiresIn é o tempo em segundos até a expiração
  return Date.now() + (expiresIn * 1000);
}

/**
 * Decodifica um JWT sem validação (apenas para leitura do payload)
 * @param token JWT a ser decodificado
 * @returns Payload do JWT ou null se inválido
 */
export function decodeJWT(token: string): any | null {
  try {
    // Split the token into parts
    const parts = token.split('.');
    
    if (parts.length !== 3) {
      return null;
    }
    
    // Decode the payload (second part)
    const payload = parts[1];
    const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    
    return JSON.parse(decodedPayload);
  } catch (error) {
    console.error('Erro ao decodificar JWT:', error);
    return null;
  }
}

/**
 * Hook para proteger rotas que requerem autenticação
 * (Usado em conjunto com React Router)
 */
export function requireAuth(): boolean {
  return isAuthenticated();
}

/**
 * Hook para proteger rotas que requerem role específica
 * (Usado em conjunto com React Router)
 */
export function requireRole(role: string | string[]): boolean {
  return isAuthenticated() && hasRole(role);
}

export default {
  isAuthenticated,
  storeUserData,
  getUserData,
  getUserId,
  hasRole,
  isAdmin,
  clearAuth,
  isValidEmail,
  isValidPassword,
  getPasswordValidationError,
  requireAuth,
  requireRole,
  calculateTokenExpiry,
  startTokenRefreshMonitor,
  stopTokenRefreshMonitor,
  decodeJWT,
}; 