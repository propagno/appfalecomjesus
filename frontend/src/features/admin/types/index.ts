import React from 'react';

/**
 * Tipos de usuários no sistema
 */
export type UserRole = 'user' | 'editor' | 'admin' | 'super_admin';

/**
 * Status de um usuário
 */
export type UserStatus = 'active' | 'suspended' | 'disabled' | 'pending';

/**
 * Período de tempo para relatórios
 */
export type TimeRange = 'today' | 'last_7_days' | 'last_30_days' | 'last_quarter' | 'last_year';

/**
 * Tipo de ação de log do admin
 */
export type AdminActionType = 
  | 'login' 
  | 'logout' 
  | 'user_created' 
  | 'user_updated' 
  | 'user_deleted' 
  | 'settings_updated' 
  | 'report_generated'
  | 'maintenance_toggled'
  | 'backup_executed';

/**
 * Interface para usuário administrativo
 */
export interface AdminUser {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  lastLogin: string;
}

/**
 * Interface para usuário regular
 */
export interface UserDetails {
  id: string;
  name: string;
  email: string;
  status: UserStatus;
  role: UserRole;
  created_at: string;
  last_login: string | null;
  subscription: {
    plan: string;
    start_date: string;
    end_date: string | null;
  };
  profile: {
    completed: boolean;
    study_preferences: string[];
    topics_of_interest: string[];
  };
  engagement: {
    activity_level: 'high' | 'medium' | 'low' | 'inactive';
    study_count: number;
    chat_count: number;
    last_activity: string | null;
    login_streak: number;
  };
}

/**
 * Interface para o Dashboard
 */
export interface DashboardMetrics {
  userMetrics: {
    totalUsers: number;
    activeUsersToday: number;
    activeUsersWeek: number;
    activeUsersMonth: number;
    newUsersToday: number;
    newUsersWeek: number;
    newUsersMonth: number;
    conversionRate: number;
  };
  studyMetrics: {
    completedStudiesToday: number;
    completedStudiesWeek: number;
    completedStudiesMonth: number;
    averageStudyTime: number;
    popularTopics: Array<{ name: string; count: number }>;
  };
  chatMetrics: {
    totalConversationsToday: number;
    totalConversationsWeek: number;
    totalConversationsMonth: number;
    averageChatLength: number;
    commonQuestions: Array<{ question: string; count: number }>;
  };
  subscriptionMetrics: {
    freeUsers: number;
    premiumUsers: number;
    premiumMonthlyUsers: number;
    premiumAnnualUsers: number;
    conversionRate: number;
    averageRevenuePerUser: number;
    totalRevenue: number;
  };
  trends: {
    userGrowth: Array<{ date: string; value: number }>;
    studyGrowth: Array<{ date: string; value: number }>;
    conversionRateGrowth: Array<{ date: string; value: number }>;
  };
}

/**
 * Interface para dados de gráficos
 */
export interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
  }>;
}

/**
 * Interface para dados de tendências
 */
export interface TrendData {
  date: string;
  value: number;
}

/**
 * Interface para log de ações administrativas
 */
export interface AdminActionLog {
  id: string;
  user_id: string;
  user_email: string;
  action_type: AdminActionType;
  details: any; // Detalhes específicos da ação
  ip_address: string;
  created_at: string;
}

/**
 * Interface para permissões de administrador
 */
export interface AdminPermission {
  section: string;
  canView: boolean;
  canEdit: boolean;
  canDelete: boolean;
}

/**
 * Interface para configurações do sistema
 */
export interface SystemSettings {
  maintenanceMode: boolean;
  chatLimits: {
    freeLimit: number;
    premiumLimit: number;
  };
  studyLimits: {
    freeLimit: number;
    premiumLimit: number;
  };
  notificationSettings: {
    emailNotifications: boolean;
    pushNotifications: boolean;
    reminderFrequency: 'daily' | 'weekly' | 'monthly' | 'never';
  };
  securitySettings: {
    passwordExpiryDays: number;
    twoFactorAuthEnabled: boolean;
    sessionTimeoutMinutes: number;
  };
  backupSettings: {
    autoBackupEnabled: boolean;
    backupFrequency: 'daily' | 'weekly' | 'monthly';
    lastBackupDate: string;
  };
  apiSettings: {
    openaiApiKey: string;
    openaiModelVersion: string;
    bibleApiKey: string;
    maxTokensPerRequest: number;
  };
}

/**
 * Interface para dados de relatório
 */
export interface ReportData {
  id: string;
  name: string;
  created_at: string;
  type: string;
  parameters: Record<string, any>;
  downloadUrl: string;
  size: string;
  summary: Array<{
    label: string;
    value: string | number;
    change: number;
  }>;
  data: Array<{
    label: string;
    [key: string]: any;
  }>;
}

/**
 * Interface para o contexto de Administração
 */
export interface AdminContextType {
  // Estado
  currentUser: AdminUser | null;
  dashboard: DashboardMetrics | null;
  systemSettings: SystemSettings | null;
  users: UserDetails[];
  actionLogs: AdminActionLog[];
  isLoading: boolean;
  isLoadingUsers: boolean;
  error: string | null;
  
  // Ações - Usuários
  fetchUsers: (page?: number, limit?: number, query?: string, status?: UserStatus) => Promise<void>;
  getUserDetails: (userId: string) => Promise<UserDetails>;
  updateUserStatus: (userId: string, status: UserStatus) => Promise<void>;
  updateUserRole: (userId: string, role: UserRole) => Promise<void>;
  updateUser: (userData: {id: string, status?: UserStatus, role?: UserRole}) => Promise<void>;
  createUser: (userData: Partial<UserDetails>) => Promise<void>;
  deleteUser: (userId: string) => Promise<void>;
  
  // Ações - Dashboard
  fetchDashboardMetrics: (timeRange?: TimeRange) => Promise<void>;
  getChartData: (metric: string, timeRange: TimeRange) => Promise<ChartData>;
  getTopUsers: () => Promise<UserDetails[]>;
  
  // Ações - Configurações
  fetchSystemSettings: () => Promise<void>;
  updateSystemSettings: (settings: Partial<SystemSettings>) => Promise<void>;
  toggleMaintenanceMode: (enabled: boolean) => Promise<void>;
  
  // Ações - Logs
  fetchActionLogs: (timeRange?: TimeRange) => Promise<void>;
  clearLogs: (olderThan?: string) => Promise<void>;
  
  // Ações - Relatórios
  generateReport: (type: string, timeRange: TimeRange) => Promise<ReportData>;
  getReportList: () => Promise<ReportData[]>;
  downloadReport: (reportId: string) => Promise<void>;
}

/**
 * Tipos e interfaces para a integração com o MS-Admin
 * Implementação para o item 10.8 - Integração com MS-Admin
 */

// Interface para métricas do sistema
export interface SystemMetrics {
  total_users: number;
  active_users_today: number;
  active_users_week: number;
  active_users_month: number;
  total_premium_users: number;
  conversion_rate: number;
  total_studies_started: number;
  total_studies_completed: number;
  total_chat_messages: number;
  average_session_duration: number;
  server_uptime: number;
  server_health: {
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
  };
}

// Interface para detalhes do usuário para administração
export interface AdminUserDetails {
  id: string;
  name: string;
  email: string;
  created_at: string;
  last_login: string;
  is_premium: boolean;
  subscription?: string;
  subscription_status?: string;
  subscription_end_date?: string;
  usage_metrics: {
    total_logins: number;
    total_chat_messages: number;
    total_studies_started: number;
    total_studies_completed: number;
    total_ad_rewards: number;
  };
  is_blocked: boolean;
  is_verified?: boolean;
  notes?: string;
}

// Interface para listagem paginada de usuários
export interface AdminUserListResponse {
  users: AdminUserDetails[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Tipos de níveis de logs
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

// Interface para logs do sistema
export interface SystemLog {
  id: string;
  timestamp: string;
  service: string;
  level: LogLevel;
  message: string;
  details?: Record<string, any>;
  user_id?: string;
  request_id?: string;
  ip_address?: string;
}

// Interface para listagem paginada de logs
export interface SystemLogListResponse {
  logs: SystemLog[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Enum para status de tarefas de manutenção
export enum MaintenanceTaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// Interface para tarefas de manutenção
export interface MaintenanceTask {
  id: string;
  name: string;
  description: string;
  status: MaintenanceTaskStatus;
  scheduled_at: string;
  completed_at?: string;
  progress_percentage?: number;
  error_message?: string;
  created_by: string;
}

// Interface para configurações do sistema
export interface SystemConfig {
  id: string;
  key: string;
  value: string;
  description?: string;
  is_public: boolean;
  is_editable: boolean;
  updated_at: string;
  updated_by: string;
}

// Enum para tipos de dashboard
export enum DashboardPeriod {
  TODAY = 'today',
  YESTERDAY = 'yesterday',
  WEEK = 'last_week',
  MONTH = 'last_30_days',
  QUARTER = 'last_quarter',
  YEAR = 'last_year',
  ALL_TIME = 'all_time'
}

// Interface para dados do dashboard
export interface DashboardData {
  period: DashboardPeriod;
  metrics: SystemMetrics;
  growth: {
    users: number;
    premium_users: number;
    studies_started: number;
    chat_messages: number;
    conversion_rate: number;
  };
  chart_data: {
    users: { date: string; value: number }[];
    premium: { date: string; value: number }[];
    studies: { date: string; value: number }[];
    chat: { date: string; value: number }[];
    revenue: { date: string; value: number }[];
  };
}

// Interface para parâmetros de filtro de usuários
export interface UserFilterParams {
  query?: string;
  is_premium?: boolean;
  subscription_status?: string;
  start_date?: string;
  end_date?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  page?: number;
  per_page?: number;
}

// Interface para parâmetros de filtro de logs
export interface LogFilterParams {
  level?: LogLevel;
  service?: string;
  user_id?: string;
  start_date?: string;
  end_date?: string;
  query?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  page?: number;
  per_page?: number;
}

// Estado global do contexto de administração
export interface AdminState {
  // Estado
  dashboardData?: DashboardData | null;
  users?: AdminUserDetails[];
  selectedUser?: AdminUserDetails | null;
  logs?: SystemLog[];
  systemConfigs?: SystemConfig[];
  maintenanceTasks?: MaintenanceTask[];
  isLoading?: boolean;
  error?: any;
  currentPage?: number;
  totalPages?: number;
  totalItems?: number;
  
  // Estado adicional usado pelo provedor real
  isMaintenanceMode?: boolean;
  activeBackupJobId?: string | null;
  activeReportJobId?: string | null;
  activeUserFilters?: Record<string, any>;
  activeLogFilters?: Record<string, any>;
  
  // Setters
  setActiveUserFilters?: (filters: Record<string, any>) => void;
  setActiveLogFilters?: (filters: Record<string, any>) => void;
  
  // Ações
  startBackup?: () => Promise<string | null>;
  startReportGeneration?: (startDate: string, endDate: string, type: string) => Promise<string | null>;
  updateSystemConfig?: (configId: string, value: string) => Promise<boolean>;
  toggleMaintenanceMode?: (enabled: boolean) => Promise<boolean>;
  refreshAllData?: () => void;
  
  // Outras ações
  updateUser?: (userData: {id: string, status?: UserStatus, role?: UserRole}) => Promise<void>;
  deleteUser?: (userId: string) => Promise<void>;
} 