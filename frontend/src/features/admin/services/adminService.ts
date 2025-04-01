import {
  AdminUser,
  DashboardMetrics,
  UserDetails,
  AdminActionLog,
  UserStatus,
  UserRole,
  TimeRange,
  AdminActionType,
  ChartData,
  SystemSettings,
  ReportData
} from '../types';

// Mock data
const mockCurrentAdminUser: AdminUser = {
  id: '1',
  name: 'Admin User',
  email: 'admin@falecomjesus.com',
  role: 'admin',
  lastLogin: new Date().toISOString()
};

const mockUsers: UserDetails[] = [
  {
    id: '1',
    name: 'Maria Silva',
    email: 'maria@exemplo.com',
    status: 'active',
    role: 'user',
    created_at: '2023-01-15T10:30:00Z',
    last_login: '2023-04-25T08:45:00Z',
    subscription: {
      plan: 'premium',
      start_date: '2023-02-10T00:00:00Z',
      end_date: '2024-02-10T00:00:00Z'
    },
    profile: {
      completed: true,
      study_preferences: ['daily', 'morning'],
      topics_of_interest: ['faith', 'family', 'wisdom']
    },
    engagement: {
      activity_level: 'high',
      study_count: 45,
      chat_count: 78,
      last_activity: '2023-04-24T16:30:00Z',
      login_streak: 12
    }
  },
  {
    id: '2',
    name: 'João Oliveira',
    email: 'joao@exemplo.com',
    status: 'active',
    role: 'user',
    created_at: '2023-02-20T14:15:00Z',
    last_login: '2023-04-23T19:20:00Z',
    subscription: {
      plan: 'free',
      start_date: '2023-02-20T00:00:00Z',
      end_date: null
    },
    profile: {
      completed: true,
      study_preferences: ['weekly', 'evening'],
      topics_of_interest: ['anxiety', 'purpose']
    },
    engagement: {
      activity_level: 'medium',
      study_count: 12,
      chat_count: 25,
      last_activity: '2023-04-23T19:45:00Z',
      login_streak: 3
    }
  },
  {
    id: '3',
    name: 'Ana Souza',
    email: 'ana@exemplo.com',
    status: 'suspended',
    role: 'user',
    created_at: '2023-03-05T09:40:00Z',
    last_login: '2023-04-10T11:25:00Z',
    subscription: {
      plan: 'premium',
      start_date: '2023-03-10T00:00:00Z',
      end_date: '2024-03-10T00:00:00Z'
    },
    profile: {
      completed: false,
      study_preferences: [],
      topics_of_interest: []
    },
    engagement: {
      activity_level: 'low',
      study_count: 5,
      chat_count: 3,
      last_activity: '2023-04-10T11:50:00Z',
      login_streak: 0
    }
  },
  {
    id: '4',
    name: 'Carlos Pereira',
    email: 'carlos@exemplo.com',
    status: 'active',
    role: 'editor',
    created_at: '2023-01-05T08:30:00Z',
    last_login: '2023-04-25T10:15:00Z',
    subscription: {
      plan: 'premium_annual',
      start_date: '2023-01-10T00:00:00Z',
      end_date: '2024-01-10T00:00:00Z'
    },
    profile: {
      completed: true,
      study_preferences: ['daily', 'morning', 'night'],
      topics_of_interest: ['wisdom', 'relationships', 'leadership']
    },
    engagement: {
      activity_level: 'high',
      study_count: 85,
      chat_count: 130,
      last_activity: '2023-04-25T10:30:00Z',
      login_streak: 25
    }
  },
  {
    id: '5',
    name: 'Paula Santos',
    email: 'paula@exemplo.com',
    status: 'disabled',
    role: 'user',
    created_at: '2023-03-15T16:20:00Z',
    last_login: '2023-03-30T12:10:00Z',
    subscription: {
      plan: 'free',
      start_date: '2023-03-15T00:00:00Z',
      end_date: null
    },
    profile: {
      completed: true,
      study_preferences: ['weekly', 'afternoon'],
      topics_of_interest: ['family', 'peace']
    },
    engagement: {
      activity_level: 'inactive',
      study_count: 2,
      chat_count: 5,
      last_activity: '2023-03-30T12:30:00Z',
      login_streak: 0
    }
  }
];

const mockDashboardMetrics: DashboardMetrics = {
  userMetrics: {
    totalUsers: 5000,
    activeUsersToday: 1250,
    activeUsersWeek: 2800,
    activeUsersMonth: 3600,
    newUsersToday: 75,
    newUsersWeek: 420,
    newUsersMonth: 1100,
    conversionRate: 18.5
  },
  studyMetrics: {
    completedStudiesToday: 950,
    completedStudiesWeek: 5600,
    completedStudiesMonth: 22000,
    averageStudyTime: 15.3,
    popularTopics: [
      { name: 'Ansiedade', count: 1240 },
      { name: 'Família', count: 980 },
      { name: 'Sabedoria', count: 840 },
      { name: 'Fé', count: 720 },
      { name: 'Propósito', count: 680 }
    ]
  },
  chatMetrics: {
    totalConversationsToday: 2800,
    totalConversationsWeek: 18500,
    totalConversationsMonth: 75000,
    averageChatLength: 6.2,
    commonQuestions: [
      { question: 'Como lidar com a ansiedade?', count: 486 },
      { question: 'Como encontrar paz?', count: 345 },
      { question: 'Como fortalecer a família?', count: 298 },
      { question: 'O que a Bíblia diz sobre perdão?', count: 276 },
      { question: 'Como crescer na fé?', count: 250 }
    ]
  },
  subscriptionMetrics: {
    freeUsers: 4100,
    premiumUsers: 900,
    premiumMonthlyUsers: 650,
    premiumAnnualUsers: 250,
    conversionRate: 18.5,
    averageRevenuePerUser: 9.75,
    totalRevenue: 8775
  },
  trends: {
    userGrowth: [
      { date: '2023-04-01', value: 4500 },
      { date: '2023-04-05', value: 4600 },
      { date: '2023-04-10', value: 4700 },
      { date: '2023-04-15', value: 4800 },
      { date: '2023-04-20', value: 4900 },
      { date: '2023-04-25', value: 5000 }
    ],
    studyGrowth: [
      { date: '2023-04-01', value: 18000 },
      { date: '2023-04-05', value: 19000 },
      { date: '2023-04-10', value: 19800 },
      { date: '2023-04-15', value: 20500 },
      { date: '2023-04-20', value: 21200 },
      { date: '2023-04-25', value: 22000 }
    ],
    conversionRateGrowth: [
      { date: '2023-04-01', value: 16.8 },
      { date: '2023-04-05', value: 17.2 },
      { date: '2023-04-10', value: 17.5 },
      { date: '2023-04-15', value: 17.9 },
      { date: '2023-04-20', value: 18.2 },
      { date: '2023-04-25', value: 18.5 }
    ]
  }
};

const mockSystemSettings: SystemSettings = {
  maintenanceMode: false,
  chatLimits: {
    freeLimit: 5,
    premiumLimit: -1
  },
  studyLimits: {
    freeLimit: 10,
    premiumLimit: -1
  },
  notificationSettings: {
    emailNotifications: true,
    pushNotifications: true,
    reminderFrequency: 'daily'
  },
  securitySettings: {
    passwordExpiryDays: 90,
    twoFactorAuthEnabled: true,
    sessionTimeoutMinutes: 30
  },
  backupSettings: {
    autoBackupEnabled: true,
    backupFrequency: 'daily',
    lastBackupDate: '2023-04-24T02:00:00Z'
  },
  apiSettings: {
    openaiApiKey: '***************', // Mascarado por segurança
    openaiModelVersion: 'gpt-3.5-turbo',
    bibleApiKey: '***************', // Mascarado por segurança
    maxTokensPerRequest: 2000
  }
};

// Mock data para logs de ação
let mockActionLogs: AdminActionLog[] = [
  {
    id: '1',
    user_id: '1',
    user_email: 'admin@falecomjesus.com',
    action_type: 'login',
    details: { ip: '192.168.0.1', browser: 'Chrome', success: true },
    ip_address: '192.168.0.1',
    created_at: '2023-04-25T08:30:00Z'
  },
  {
    id: '2',
    user_id: '1',
    user_email: 'admin@falecomjesus.com',
    action_type: 'user_updated',
    details: { user_id: '3', status: 'suspended', previous_status: 'active' },
    ip_address: '192.168.1.1',
    created_at: '2023-04-25T10:30:00Z'
  },
  {
    id: '3',
    user_id: '1',
    user_email: 'admin@falecomjesus.com',
    action_type: 'settings_updated',
    details: { settings: 'maintenance_mode', value: false, previous_value: true },
    ip_address: '192.168.1.1',
    created_at: '2023-04-24T16:45:00Z'
  },
  {
    id: '4',
    user_id: '1',
    user_email: 'admin@falecomjesus.com',
    action_type: 'report_generated',
    details: { report_type: 'user_activity', period: 'last_30_days' },
    ip_address: '192.168.1.1',
    created_at: '2023-04-24T14:20:00Z'
  }
];

// Função utilitária para simular delay de rede
const mockNetworkDelay = () => new Promise(resolve => setTimeout(resolve, 1200));

// Mock data para relatórios
const mockReports: ReportData[] = [
  {
    id: '1',
    name: 'Relatório de Atividade de Usuários',
    created_at: '2023-04-22T10:30:00Z',
    type: 'user_activity',
    parameters: { timeRange: 'last_30_days' },
    downloadUrl: '/reports/user_activity_last_30days.csv',
    size: '2.4MB',
    summary: [
      { label: 'Total de Registros', value: 150, change: 15 },
      { label: 'Média por Dia', value: 9.2, change: 7 },
      { label: 'Crescimento', value: '18%', change: 28 },
      { label: 'Uso por Usuário', value: 4.1, change: 5 }
    ],
    data: [
      { label: 'João Silva', actions: 55, logins: 15, averageTime: '35min', lastActivity: '1 hora atrás' },
      { label: 'Maria Souza', actions: 42, logins: 10, averageTime: '28min', lastActivity: '3 horas atrás' },
    ]
  },
  {
    id: '2',
    name: 'Relatório de Uso de Conteúdo',
    created_at: '2023-04-20T14:15:00Z',
    type: 'content_usage',
    parameters: { timeRange: 'last_7_days' },
    downloadUrl: '/reports/content_usage_last_7days.csv',
    size: '1.8MB',
    summary: [
      { label: 'Total de Visualizações', value: 850, change: 12 },
      { label: 'Média por Dia', value: 121.4, change: 5 },
      { label: 'Conclusões', value: 320, change: 8 },
      { label: 'Taxa de Conclusão', value: '37.6%', change: -2 }
    ],
    data: [
      { label: 'Plano: Paz Interior', views: 320, averageTime: '18min', completions: 95 },
      { label: 'Plano: Fé em Ação', views: 240, averageTime: '15min', completions: 82 },
    ]
  },
  {
    id: '3',
    name: 'Relatório de Assinaturas',
    created_at: '2023-04-18T09:20:00Z',
    type: 'subscription',
    parameters: { timeRange: 'last_90_days' },
    downloadUrl: '/reports/subscription_last_90days.csv',
    size: '1.2MB',
    summary: [
      { label: 'Total de Assinantes', value: 950, change: 23 },
      { label: 'Novos Assinantes', value: 125, change: 15 },
      { label: 'Cancelamentos', value: 32, change: -5 },
      { label: 'Receita Total', value: 'R$ 28.500,00', change: 18 }
    ],
    data: [
      { label: 'Premium Anual', subscribers: 350, newSubscribers: 45, canceled: 8, revenue: 'R$ 21.000,00' },
      { label: 'Premium Mensal', subscribers: 600, newSubscribers: 80, canceled: 24, revenue: 'R$ 7.500,00' },
    ]
  },
  {
    id: '4',
    name: 'Relatório de Interações com Chat IA',
    created_at: '2023-04-15T16:40:00Z',
    type: 'chat_interactions',
    parameters: { timeRange: 'last_30_days' },
    downloadUrl: '/reports/chat_interactions_last_30days.csv',
    size: '3.5MB',
    summary: [
      { label: 'Total de Mensagens', value: 24500, change: 35 },
      { label: 'Média por Usuário', value: 8.2, change: 12 },
      { label: 'Novas Conversas', value: 3200, change: 28 },
      { label: 'Tempo Médio', value: '4.5min', change: -8 }
    ],
    data: [
      { label: 'Como lidar com ansiedade', count: 1240, averageResponseTime: '2.3s', userSatisfaction: '92%' },
      { label: 'Versículos sobre paz', count: 980, averageResponseTime: '1.8s', userSatisfaction: '95%' },
    ]
  },
  {
    id: '5',
    name: 'Relatório de Uso da Bíblia',
    created_at: '2023-04-12T11:10:00Z',
    type: 'bible_usage',
    parameters: { timeRange: 'last_7_days' },
    downloadUrl: '/reports/bible_usage_last_7days.csv',
    size: '1.5MB',
    summary: [
      { label: 'Total de Consultas', value: 8900, change: 18 },
      { label: 'Livros Populares', value: 5, change: 0 },
      { label: 'Temas Buscados', value: 350, change: 25 },
      { label: 'Versículos Salvos', value: 1240, change: 32 }
    ],
    data: [
      { label: 'Salmos', views: 1850, searches: 620, saved: 420 },
      { label: 'João', views: 1240, searches: 480, saved: 310 },
    ]
  }
];

// Chart data generator
const generateChartData = (metric: string, period: TimeRange): ChartData => {
  // Simulação de dados para diferentes métricas e períodos
  const labels: string[] = [];
  const data: number[] = [];
  
  // Gerar labels de acordo com o período
  const today = new Date();
  let startDate = new Date();
  let labelFormat = '';
  let dataPoints = 0;
  
  switch (period) {
    case 'today':
      startDate = new Date(today.setHours(0, 0, 0, 0));
      dataPoints = 24; // Hours in a day
      labelFormat = 'HH:00';
      break;
    case 'last_7_days':
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 6);
      dataPoints = 7; // Days
      labelFormat = 'DD/MM';
      break;
    case 'last_30_days':
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 29);
      dataPoints = 30; // Days
      labelFormat = 'DD/MM';
      break;
    case 'last_quarter':
      startDate = new Date(today);
      startDate.setMonth(today.getMonth() - 3);
      dataPoints = 12; // Weeks
      labelFormat = 'Week WW';
      break;
    case 'last_year':
      startDate = new Date(today);
      startDate.setFullYear(today.getFullYear() - 1);
      dataPoints = 12; // Months
      labelFormat = 'MMM';
      break;
    default:
      startDate = new Date(today);
      startDate.setDate(today.getDate() - 6);
      dataPoints = 7; // Default to last 7 days
      labelFormat = 'DD/MM';
  }
  
  // Gerar labels
  for (let i = 0; i < dataPoints; i++) {
    let label = '';
    switch (period) {
      case 'today':
        label = `${i}:00`;
        break;
      case 'last_7_days':
      case 'last_30_days':
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        label = `${date.getDate()}/${date.getMonth() + 1}`;
        break;
      case 'last_quarter':
        label = `Semana ${i + 1}`;
        break;
      case 'last_year':
        const monthDate = new Date(startDate);
        monthDate.setMonth(startDate.getMonth() + i);
        label = monthDate.toLocaleString('pt-BR', { month: 'short' });
        break;
      default:
        const defaultDate = new Date(startDate);
        defaultDate.setDate(startDate.getDate() + i);
        label = `${defaultDate.getDate()}/${defaultDate.getMonth() + 1}`;
    }
    labels.push(label);
  }
  
  // Gerar dados de exemplo com base na métrica
  let baseValue = 0;
  let variance = 0;
  let trend = 0;
  
  switch (metric) {
    case 'active_users':
      baseValue = 1000;
      variance = 200;
      trend = 10;
      break;
    case 'new_users':
      baseValue = 100;
      variance = 30;
      trend = 2;
      break;
    case 'study_completions':
      baseValue = 500;
      variance = 100;
      trend = 5;
      break;
    case 'chat_usage':
      baseValue = 2000;
      variance = 400;
      trend = 15;
      break;
    case 'premium_conversions':
      baseValue = 50;
      variance = 10;
      trend = 1;
      break;
    case 'revenue':
      baseValue = 5000;
      variance = 1000;
      trend = 50;
      break;
    default:
      baseValue = 500;
      variance = 100;
      trend = 5;
  }
  
  // Gerar dados com tendência crescente e variância aleatória
  for (let i = 0; i < dataPoints; i++) {
    const randomVariance = Math.floor(Math.random() * variance * 2) - variance;
    const trendValue = trend * i;
    const value = Math.max(0, baseValue + trendValue + randomVariance);
    data.push(value);
  }
  
  return {
    labels,
    datasets: [
      {
        label: metric,
        data
      }
    ]
  };
};

// Service Implementation
export const adminService = {
  // Current Admin User
  getCurrentAdminUser: async (): Promise<AdminUser> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockCurrentAdminUser;
  },
  
  // User Management
  getUsers: async (page: number = 1, limit: number = 10, query?: string, status?: UserStatus): Promise<UserDetails[]> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    let filteredUsers = [...mockUsers];
    
    // Aplicar filtro de status
    if (status) {
      filteredUsers = filteredUsers.filter(user => user.status === status);
    }
    
    // Aplicar filtro de busca
    if (query) {
      const lowerQuery = query.toLowerCase();
      filteredUsers = filteredUsers.filter(user =>
        user.name.toLowerCase().includes(lowerQuery) ||
        user.email.toLowerCase().includes(lowerQuery)
      );
    }
    
    // Aplicar paginação
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    
    return filteredUsers.slice(startIndex, endIndex);
  },
  
  getUserDetails: async (userId: string): Promise<UserDetails> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 600));
    
    const user = mockUsers.find(user => user.id === userId);
    
    if (!user) {
      throw new Error(`Usuário não encontrado: ${userId}`);
    }
    
    return user;
  },
  
  updateUserStatus: async (userId: string, status: UserStatus): Promise<void> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 700));
    
    const userIndex = mockUsers.findIndex(user => user.id === userId);
    
    if (userIndex === -1) {
      throw new Error(`Usuário não encontrado: ${userId}`);
    }
    
    // Em um ambiente real, isso faria uma chamada de API
    mockUsers[userIndex].status = status;
  },
  
  updateUserRole: async (userId: string, role: UserRole): Promise<void> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 700));
    
    const userIndex = mockUsers.findIndex(user => user.id === userId);
    
    if (userIndex === -1) {
      throw new Error(`Usuário não encontrado: ${userId}`);
    }
    
    // Em um ambiente real, isso faria uma chamada de API
    mockUsers[userIndex].role = role;
  },
  
  createUser: async (userData: Partial<UserDetails>): Promise<UserDetails> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 900));
    
    // Gerar ID único
    const newId = (mockUsers.length + 1).toString();
    
    // Criar novo usuário com valores padrão
    const newUser: UserDetails = {
      id: newId,
      name: userData.name || 'Novo Usuário',
      email: userData.email || `user${newId}@exemplo.com`,
      status: userData.status || 'active',
      role: userData.role || 'user',
      created_at: new Date().toISOString(),
      last_login: null,
      subscription: {
        plan: 'free',
        start_date: new Date().toISOString(),
        end_date: null
      },
      profile: {
        completed: false,
        study_preferences: [],
        topics_of_interest: []
      },
      engagement: {
        activity_level: 'low',
        study_count: 0,
        chat_count: 0,
        last_activity: null,
        login_streak: 0
      },
      ...userData
    };
    
    // Em um ambiente real, isso faria uma chamada de API
    mockUsers.push(newUser);
    
    return newUser;
  },
  
  deleteUser: async (userId: string): Promise<void> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const userIndex = mockUsers.findIndex(user => user.id === userId);
    
    if (userIndex === -1) {
      throw new Error(`Usuário não encontrado: ${userId}`);
    }
    
    // Em um ambiente real, isso faria uma chamada de API
    mockUsers.splice(userIndex, 1);
  },
  
  // Dashboard
  getDashboardMetrics: async (timeRange?: TimeRange): Promise<DashboardMetrics> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Em um ambiente real, isso faria uma chamada de API com o timeRange
    return mockDashboardMetrics;
  },
  
  getChartData: async (metric: string, timeRange: TimeRange): Promise<ChartData> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Gerar dados de gráfico
    return generateChartData(metric, timeRange);
  },
  
  getTopUsers: async (): Promise<UserDetails[]> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 700));
    
    // Ordenar por nível de atividade e retornar os 5 principais
    return [...mockUsers]
      .sort((a, b) => {
        const activityLevelScore = (level: string) => {
          switch (level) {
            case 'high': return 4;
            case 'medium': return 3;
            case 'low': return 2;
            case 'inactive': return 1;
            default: return 0;
          }
        };
        
        return activityLevelScore(b.engagement.activity_level) - activityLevelScore(a.engagement.activity_level);
      })
      .slice(0, 5);
  },
  
  // System Settings
  getSystemSettings: async (): Promise<SystemSettings> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return mockSystemSettings;
  },
  
  updateSystemSettings: async (settings: Partial<SystemSettings>): Promise<SystemSettings> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Em um ambiente real, isso faria uma chamada de API
    Object.assign(mockSystemSettings, settings);
    
    return mockSystemSettings;
  },
  
  toggleMaintenanceMode: async (enabled: boolean): Promise<SystemSettings> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Em um ambiente real, isso faria uma chamada de API
    mockSystemSettings.maintenanceMode = enabled;
    
    return mockSystemSettings;
  },
  
  // Logs
  getActionLogs: async (
    page: number = 1, 
    limit: number = 20, 
    actionType?: AdminActionType
  ): Promise<AdminActionLog[]> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    let filteredLogs = [...mockActionLogs];
    
    // Aplicar filtro de tipo de ação
    if (actionType) {
      filteredLogs = filteredLogs.filter(log => log.action_type === actionType);
    }
    
    // Ordenar por data mais recente
    filteredLogs = filteredLogs.sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );
    
    // Aplicar paginação
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    
    return filteredLogs.slice(startIndex, endIndex);
  },
  
  clearLogs: async (olderThan?: string): Promise<void> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 700));
    
    // Em um ambiente real, isso faria uma chamada de API
    if (olderThan) {
      const date = new Date(olderThan);
      mockActionLogs = mockActionLogs.filter(log => 
        new Date(log.created_at) >= date
      );
    } else {
      mockActionLogs = [];
    }
  },
  
  // Reports
  generateReport: async (
    type: string,
    timeRange: TimeRange
  ): Promise<ReportData> => {
    await mockNetworkDelay();
    
    // Mock data para relatórios
    const mockReportData: ReportData = {
      id: `report-${Date.now()}`,
      name: `Relatório de ${type === 'user_activity' ? 'Atividade de Usuários' : 
             type === 'content_usage' ? 'Uso de Conteúdo' : 
             type === 'subscription' ? 'Assinaturas' : 'Atividade'}`,
      created_at: new Date().toISOString(),
      type,
      parameters: { timeRange },
      downloadUrl: '#',
      size: '1.2MB',
      summary: [
        { label: 'Total de Registros', value: 125, change: 12 },
        { label: 'Média por Dia', value: 8.3, change: 5 },
        { label: 'Crescimento', value: '15%', change: 23 },
        { label: 'Uso por Usuário', value: 3.7, change: -2 }
      ],
      data: (() => {
        switch (type) {
          case 'user_activity':
            return [
              { label: 'João Silva', actions: 45, logins: 12, averageTime: '32min', lastActivity: '2 horas atrás' },
              { label: 'Maria Souza', actions: 38, logins: 8, averageTime: '25min', lastActivity: '5 horas atrás' },
              { label: 'Pedro Santos', actions: 32, logins: 5, averageTime: '18min', lastActivity: '1 dia atrás' },
              { label: 'Ana Oliveira', actions: 29, logins: 7, averageTime: '22min', lastActivity: '3 horas atrás' },
              { label: 'Carlos Pereira', actions: 25, logins: 4, averageTime: '15min', lastActivity: '2 dias atrás' },
            ];
          case 'content_usage':
            return [
              { label: 'Plano: Paz Interior', views: 245, averageTime: '15min', completions: 78 },
              { label: 'Plano: Fé em Ação', views: 189, averageTime: '12min', completions: 65 },
              { label: 'Plano: Luz no Caminho', views: 156, averageTime: '18min', completions: 42 },
              { label: 'Plano: Serenidade', views: 134, averageTime: '10min', completions: 38 },
              { label: 'Plano: Gratidão Diária', views: 112, averageTime: '8min', completions: 27 },
            ];
          case 'subscription':
            return [
              { label: 'Premium Anual', subscribers: 189, newSubscribers: 12, canceled: 3, revenue: 'R$ 18.900,00' },
              { label: 'Premium Mensal', subscribers: 256, newSubscribers: 28, canceled: 15, revenue: 'R$ 5.120,00' },
              { label: 'Free', subscribers: 1254, newSubscribers: 89, canceled: 5, revenue: 'R$ 0,00' },
            ];
          default:
            return [];
        }
      })()
    };
    
    return mockReportData;
  },
  
  getReportList: async (): Promise<ReportData[]> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return mockReports;
  },
  
  downloadReport: async (reportId: string): Promise<void> => {
    // Simular delay de rede
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const report = mockReports.find(r => r.id === reportId);
    
    if (!report) {
      throw new Error(`Relatório não encontrado: ${reportId}`);
    }
    
    // Em um ambiente real, isso iniciaria o download do arquivo
    console.log(`Downloading report: ${report.downloadUrl}`);
    
    // Simular um download bem-sucedido
    return;
  }
}; 