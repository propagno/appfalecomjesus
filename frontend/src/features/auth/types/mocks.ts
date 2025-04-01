import { User, AuthResponse, AuthTokens, UserPreferences } from './index';

/**
 * Usuário mock para desenvolvimento
 */
export const MOCK_USER: User = {
  id: 'user_1',
  name: 'Usuário de Teste',
  email: 'usuario@teste.com',
  avatar_url: 'https://i.pravatar.cc/150?u=usuario@teste.com',
  role: 'user',
  created_at: new Date('2023-01-15').toISOString(),
  updated_at: new Date('2023-04-20').toISOString(),
  onboarding_completed: true,
  subscription: {
    plan_type: 'Free',
    status: 'active'
  }
};

/**
 * Tokens mock para desenvolvimento
 */
export const MOCK_TOKENS: AuthTokens = {
  access_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEiLCJuYW1lIjoiVXN1w6FyaW8gZGUgVGVzdGUiLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MjUxNjIzOTAyMn0.MOCK_SIGNATURE',
  refresh_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzEiLCJuYW1lIjoiVXN1w6FyaW8gZGUgVGVzdGUiLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MjUxNjIzOTAyMn0.MOCK_REFRESH_SIGNATURE',
  expires_in: 86400 // 24 horas em segundos
};

/**
 * Resposta de autenticação mock para desenvolvimento
 */
export const MOCK_AUTH_RESPONSE: AuthResponse = {
  user: MOCK_USER,
  tokens: MOCK_TOKENS
};

/**
 * Preferências do usuário mock para desenvolvimento
 */
export const MOCK_USER_PREFERENCES: UserPreferences = {
  objectives: ['ansiedade', 'paz', 'sabedoria'],
  bible_experience_level: 'intermediario',
  content_preferences: ['audio', 'texto'],
  preferred_time: 'manha',
  onboarding_completed: true
}; 