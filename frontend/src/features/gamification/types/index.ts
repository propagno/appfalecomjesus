/**
 * Representa os tipos de ações que geram pontos
 */
export type PointActionType = 
  | 'daily_login'          // Login diário
  | 'study_completed'      // Completar um estudo
  | 'study_started'        // Iniciar um estudo
  | 'reflection_added'     // Adicionar uma reflexão
  | 'verse_shared'         // Compartilhar um versículo
  | 'streak_continued'     // Sequência de dias mantida
  | 'achievement_unlocked' // Conquista desbloqueada
  | 'first_chat'           // Primeira conversa com IA
  | 'daily_devotional'     // Ver o devocional diário
  | 'watched_ad'          // Assistir a um anúncio
  | 'streak_milestone';   // Milestone de streak

/**
 * Representa uma transação de pontos
 */
export interface PointTransaction {
  id: string;
  user_id: string;
  action: PointActionType;
  amount: number;
  description: string;
  created_at: string;
}

/**
 * Representa o sumário de pontos do usuário
 */
export interface UserPoints {
  id: string;
  user_id: string;
  total_points: number;
  level: number;
  next_level_threshold: number;
  last_updated: string;
}

/**
 * Representa um nível de usuário
 */
export interface Level {
  level: number;
  name: string;
  min_points: number;
  max_points: number;
  icon_url?: string;
}

// Usamos o tipo Level para manter a consistência
export type UserLevel = Level;

/**
 * Representa a categoria de uma conquista
 */
export type AchievementCategory = 
  | 'study'          // Estudos bíblicos
  | 'devotional'     // Devocionais diários
  | 'streak'         // Sequências de uso
  | 'social'         // Compartilhamentos e interações
  | 'engagement'     // Engajamento com o app
  | 'chat'           // Interações com IA
  | 'bible'          // Uso da Bíblia
  | 'special';       // Eventos especiais

/**
 * Representa uma conquista
 */
export interface Achievement {
  id: string;
  code: string;
  name: string;
  description: string;
  icon_url: string;
  points_reward: number;
  category: 'study' | 'bible' | 'chat' | 'devotional' | 'engagement' | 'contribution';
  difficulty: 'easy' | 'medium' | 'hard' | 'legendary';
  requirements: string;
}

/**
 * Representa uma conquista obtida por um usuário
 */
export interface UserAchievement {
  id: string;
  user_id: string;
  achievement_id: string;
  achievement: Achievement;
  earned_at: string;
  seen: boolean;
}

/**
 * Representa uma notificação de gamificação para o usuário
 */
export interface GamificationNotification {
  id: string;
  user_id: string;
  type: 'achievement_unlocked' | 'level_up' | 'streak_milestone' | 'points_milestone';
  title: string;
  message: string;
  image_url?: string;
  is_read: boolean;
  created_at: string;
  data?: {
    achievement_id?: string;
    points?: number;
    level?: number;
    streak?: number;
  };
}

/**
 * Representa o contexto de gamificação global
 */
export interface GamificationContextType {
  // Estado
  userPoints: UserPoints | null;
  userLevel: Level | null;
  achievements: Achievement[];
  userAchievements: UserAchievement[];
  unlockedAchievements: UserAchievement[];
  pointTransactions: PointTransaction[];
  notifications: GamificationNotification[];
  isLoading: boolean;
  error: string | null;
  
  // Ações
  fetchUserPoints: () => Promise<void>;
  fetchAchievements: () => Promise<void>;
  fetchUserAchievements: () => Promise<void>;
  fetchPointTransactions: (limit?: number) => Promise<void>;
  fetchNotifications: () => Promise<void>;
  
  // Utilitários
  awardPoints: (action: PointActionType, customDescription?: string) => Promise<void>;
  markNotificationAsRead: (notificationId: string) => Promise<void>;
  markAllNotificationsAsRead: () => Promise<void>;
  dismissNotification: (notificationId: string) => Promise<void>;
  
  // Helpers
  getCurrentLevel: () => Level | null;
  getNextLevelProgress: () => number;
  hasNewNotifications: () => boolean;
  getUnreadNotificationsCount: () => number;
  addPoints: (amount: number, reason: string) => void;
  subtractPoints: (amount: number, reason: string) => void;
  refreshUserData: () => Promise<void>;
  dismissAchievementNotification: (achievementId: string) => void;
  
  // Integração com outras features
  handleLoginSuccess: () => void;
  handleStudyCompleted: (studyTitle: string) => void;
  handleStudyStarted: (studyTitle: string) => void;
  handleReflectionAdded: () => void;
  handleVerseShared: () => void;
}

/**
 * Estrutura de níveis do sistema
 */
export const LEVELS: Level[] = [
  { level: 1, name: 'Iniciante', min_points: 0, max_points: 99 },
  { level: 2, name: 'Estudante', min_points: 100, max_points: 299 },
  { level: 3, name: 'Dedicado', min_points: 300, max_points: 599 },
  { level: 4, name: 'Discípulo', min_points: 600, max_points: 999 },
  { level: 5, name: 'Aprendiz Fiel', min_points: 1000, max_points: 1499 },
  { level: 6, name: 'Servo Comprometido', min_points: 1500, max_points: 2499 },
  { level: 7, name: 'Peregrino', min_points: 2500, max_points: 3999 },
  { level: 8, name: 'Seguidor', min_points: 4000, max_points: 5999 },
  { level: 9, name: 'Discípulo Fiel', min_points: 6000, max_points: 8499 },
  { level: 10, name: 'Mensageiro', min_points: 8500, max_points: 11999 },
  { level: 11, name: 'Evangelista', min_points: 12000, max_points: 16999 },
  { level: 12, name: 'Semeador da Palavra', min_points: 17000, max_points: 24999 },
  { level: 13, name: 'Mestre da Palavra', min_points: 25000, max_points: 34999 },
  { level: 14, name: 'Embaixador do Reino', min_points: 35000, max_points: 49999 },
  { level: 15, name: 'Testemunha Fiel', min_points: 50000, max_points: 99999 },
  { level: 16, name: 'Luz do Mundo', min_points: 100000, max_points: Number.MAX_SAFE_INTEGER },
];

/**
 * Pontos ganhos por cada tipo de ação
 */
export const POINTS_BY_ACTION: Record<PointActionType, number> = {
  daily_login: 5,
  study_completed: 25,
  study_started: 10,
  reflection_added: 15,
  verse_shared: 10,
  streak_continued: 5,
  achievement_unlocked: 50,
  first_chat: 10,
  daily_devotional: 5,
  watched_ad: 3,
  streak_milestone: 50,
};

/**
 * Tipos de atividades que podem gerar pontos
 */
export enum ActivityType {
  DAILY_LOGIN = 'daily_login',
  COMPLETE_STUDY = 'complete_study',
  COMPLETE_DEVOTIONAL = 'complete_devotional',
  SHARE_CONTENT = 'share_content',
  CHAT_INTERACTION = 'chat_interaction',
  BIBLE_READING = 'bible_reading',
  AD_WATCHED = 'ad_watched',
  INVITE_FRIEND = 'invite_friend',
  PROFILE_COMPLETED = 'profile_completed',
  FEEDBACK_PROVIDED = 'feedback_provided'
}

/**
 * Dados para registrar uma nova recompensa
 */
export interface RewardData {
  activity_type: ActivityType;
  related_entity_id?: string;
  additional_info?: Record<string, any>;
}

/**
 * Resposta ao registrar uma recompensa
 */
export interface RewardResponse {
  points_earned: number;
  current_points: number;
  level: number;
  achievements_unlocked: Achievement[];
}

/**
 * Item da tabela de classificação
 */
export interface LeaderboardItem {
  position: number;
  user_id: string;
  user_name: string;
  avatar_url?: string;
  points: number;
  level: number;
  achievements_count: number;
  is_current_user: boolean;
}

/**
 * Resposta da API para listagem de conquistas do usuário
 */
export interface UserAchievementsResponse {
  achievements: UserAchievement[];
  total: number;
  earned: number;
  pending: number;
}

/**
 * Resposta da API para a tabela de classificação
 */
export interface LeaderboardResponse {
  items: LeaderboardItem[];
  total_users: number;
  current_user_position?: number;
}

/**
 * Representa o estado da gamificação
 */
export interface GamificationState {
  userPoints: UserPoints | null;
  userLevel: Level | null;
  achievements: Achievement[];
  userAchievements: UserAchievement[];
  unlockedAchievements: UserAchievement[];
  pointTransactions: PointTransaction[];
  notifications: GamificationNotification[];
  isLoading: boolean;
  error: string | null;
}

/**
 * Representa o payload para registrar uma atividade
 */
export interface RegisterActivityPayload {
  activity_type: PointActionType;
  description?: string;
  metadata?: {
    study_id?: string;
    study_title?: string;
    verse_id?: string;
    verse_text?: string;
    chat_message_count?: number;
    streak_days?: number;
  };
}

/**
 * Representa a resposta de conclusão de uma atividade
 */
export interface ActivityCompletionResponse {
  success: boolean;
  points_awarded: number;
  new_achievements: UserAchievement[];
  level_up?: {
    new_level: number;
    level_name: string;
  };
  error?: string;
} 