import { AxiosResponse, AxiosRequestConfig, AxiosInstance } from 'axios';

// Extend AxiosRequestConfig to include our custom properties
declare module 'axios' {
  interface AxiosRequestConfig {
    _expectedArrayResponse?: boolean;
  }
}

// Interfaces para os tipos de retorno da API
export interface UserPoints {
  total_points: number;
  points: number;
  levelup?: boolean;
  history: Array<{
    id: number;
    points: number;
    reason: string;
    created_at: string;
  }>;
}

export interface Achievement {
  id: number;
  badge_name: string;
  description: string;
  category: string;
  icon_url?: string;
  earned_at: string;
}

export interface Certificate {
  id: string;
  badge_name: string;
  study_plan_id: string;
  completion_date: string;
  certificate_code: string;
  title?: string;
  description?: string;
  date?: string;
  imageUrl?: string;
  downloadUrl?: string;
}

// Interfaces para as APIs
export interface GamificationAPI {
  getUserPoints?: () => Promise<ApiResponse<any>>;
  getPoints: () => Promise<ApiResponse<any>>;
  getAchievements: () => Promise<ApiResponse<any>>;
  addPoints: (amount: number, source: string) => Promise<ApiResponse<any>>;
  checkAchievements: () => Promise<ApiResponse<any>>;
  getNotifications?: () => Promise<ApiResponse<any>>;
  registerAdReward?: (rewardType: string) => Promise<ApiResponse<any>>;
  getCertificates?: () => Promise<ApiResponse<any>>;
  checkCondition?: (achievementType: string, value: number) => Promise<ApiResponse<any>>;
  unlockByCondition?: (conditionType: string, value: number) => Promise<ApiResponse<any>>;
}

export interface AuthAPI {
  register: (name: string, email: string, password: string) => Promise<AxiosResponse<any>>;
  login: (email: string, password: string) => Promise<AxiosResponse<any>>;
  logout: () => Promise<AxiosResponse<any>>;
  getUser: () => Promise<AxiosResponse<any>>;
  me: () => Promise<AxiosResponse<any>>;
  refreshToken: () => Promise<AxiosResponse<any>>;
  getPreferences: () => Promise<AxiosResponse<any>>;
  updatePreferences: (preferences: any) => Promise<AxiosResponse<any>>;
  savePreferences: (preferences: any) => Promise<AxiosResponse<any>>;
  updateProfile: (profileData: any) => Promise<AxiosResponse<any>>;
  deleteAccount: () => Promise<AxiosResponse<any>>;
  getSettings: () => Promise<AxiosResponse<any>>;
  updateSettings: (settings: any) => Promise<AxiosResponse<any>>;
  forgotPassword?: (email: string) => Promise<AxiosResponse<any>>;
  resetPassword?: (token: string, password: string) => Promise<AxiosResponse<any>>;
}

export interface BibleAPI {
  getBooks: () => Promise<ApiResponse<any>>;
  getChapters: (bookId: string) => Promise<ApiResponse<any>>;
  getVerses: (chapterId: string) => Promise<ApiResponse<any>>;
  search: (query: string) => Promise<ApiResponse<any>>;
  addFavorite: (verseId: string) => Promise<ApiResponse<any>>;
  removeFavorite: (verseId: string) => Promise<ApiResponse<any>>;
  getFavorites: () => Promise<ApiResponse<any>>;
  toggleFavorite: (verseId: string) => Promise<ApiResponse<any>>;
}

export interface StudyAPI {
  getCurrentPlan: () => Promise<ApiResponse<any>>;
  getPlans: () => Promise<ApiResponse<any>>;
  getPlan: (planId: string) => Promise<ApiResponse<any>>;
  startPlan: (planId: string) => Promise<ApiResponse<any>>;
  getCurrentSection: () => Promise<ApiResponse<any>>;
  completeSection: (sectionId: string) => Promise<ApiResponse<any>>;
  updateProgress: (data: any) => Promise<ApiResponse<any>>;
  getReflections: () => Promise<ApiResponse<any>>;
  getReflection: (reflectionId: string) => Promise<ApiResponse<any>>;
  saveReflection: (data: any) => Promise<ApiResponse<any>>;
  initPlan: () => Promise<ApiResponse<any>>;
  getStudySession: (sessionId: string) => Promise<ApiResponse<any>>;
  getDailyDevotional: () => Promise<ApiResponse<any>>;
  toggleFavoriteDevotional: (devotionalId: string) => Promise<ApiResponse<any>>;
}

export interface MonetizationAPI {
  getSubscription: () => Promise<AxiosResponse<any>>;
  registerAdReward: (data: any) => Promise<AxiosResponse<any>>;
  subscribe: (planType: string) => Promise<AxiosResponse<any>>;
  cancelSubscription: () => Promise<AxiosResponse<any>>;
}

export interface SupportAPI {
  sendMessage: (data: any) => Promise<AxiosResponse<any>>;
}

// Interface para respostas da API
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

// Interfaces para Reflexões
export interface Reflection {
  id: string;
  user_id: string;
  study_section_id: string;
  reflection_text: string;
  created_at: string;
}

export interface CreateReflectionDTO {
  study_section_id: string;
  reflection_text: string;
}

export interface UpdateReflectionDTO {
  reflection_text: string;
}

// Interface para Chat
export interface ChatMessage {
  id: string;
  message: string;
  response?: string;
  user_id?: string;
  sender: 'user' | 'ai';
  context?: {
    user_id: string;
    bible_experience?: string;
    preferred_topics?: string[];
  };
  references?: Array<{
    reference: string;
    text: string;
  }>;
  suggestions?: string[];
  remaining_messages?: number;
  metadata?: {
    model: string;
    processing_time: number;
    token_count?: number;
    error?: string;
  };
  created_at: string;
  is_favorite?: boolean;
  study_context?: {
    plan_id?: string;
    section_id?: string;
    verse_reference?: string;
  };
}

export interface ChatHistory {
  items: ChatMessage[];
  count: number;
}

export interface ChatMessageLimit {
  remaining_messages: number;
  limit: number;
  reset_in: number;
  can_watch_ad: boolean;
}

export interface ChatAPI {
  sendMessage: (message: string, context?: any) => Promise<ApiResponse<ChatMessage>>;
  getHistory: (userId: string) => Promise<ApiResponse<ChatHistory>>;
  getRemainingMessages: () => Promise<ApiResponse<ChatMessageLimit>>;
  watchAd: () => Promise<ApiResponse<ChatMessageLimit>>;
  getMessages: (options?: { limit?: number }) => Promise<ApiResponse<ChatMessage[]>>;
  getStats: () => Promise<ApiResponse<any>>;
  deleteMessage: (messageId: string) => Promise<ApiResponse<void>>;
  favoriteMessage: (messageId: string, isFavorite: boolean) => Promise<ApiResponse<void>>;
  clearHistory: () => Promise<ApiResponse<void>>;
  watchAdForReward: () => Promise<ApiResponse<any>>;
}

// Interface para Reflexões
export interface ReflectionsAPI {
  list: () => Promise<ApiResponse<Reflection[]>>;
  create: (reflectionData: CreateReflectionDTO) => Promise<ApiResponse<Reflection>>;
  update: (id: string, reflectionData: UpdateReflectionDTO) => Promise<ApiResponse<Reflection>>;
  delete: (id: string) => Promise<ApiResponse<void>>;
}

// Interface para Certificados
export interface CertificatesAPI {
  list: () => Promise<ApiResponse<Certificate[]>>;
  generate: (studyId: string) => Promise<ApiResponse<Certificate>>;
  download: (certificateId: string) => Promise<ApiResponse<Blob>>;
}

// Atualizar interface API principal
export interface API extends AxiosInstance {
  auth: AuthAPI;
  bible: BibleAPI;
  study: StudyAPI;
  gamification: GamificationAPI;
  monetization: MonetizationAPI;
  support: SupportAPI;
  chat: ChatAPI;
  reflections: ReflectionsAPI;
  certificates: CertificatesAPI;
  (config: AxiosRequestConfig): Promise<AxiosResponse>;
}

// Auth API interfaces
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  subscription: {
    type: 'free' | 'premium';
    status: 'active' | 'inactive' | 'cancelled';
    expires_at?: string;
  };
  bible_experience: 'iniciante' | 'intermediário' | 'avançado';
  preferred_topics: string[];
  created_at: string;
  updated_at: string;
}

export interface ChatContext {
  user_id: string;
  bible_experience: 'iniciante' | 'intermediário' | 'avançado';
  preferred_topics: string[];
} 
