import React, { createContext, useContext, useState, ReactNode, useEffect, useCallback } from 'react';
import { 
  UserPoints, 
  PointTransaction, 
  Level, 
  Achievement, 
  UserAchievement, 
  GamificationNotification,
  PointActionType,
  LEVELS,
  POINTS_BY_ACTION,
  GamificationContextType
} from '../types';
import { v4 as uuidv4 } from 'uuid';

// Mock data para desenvolvimento
const mockAchievements: Achievement[] = [
  {
    id: "1",
    code: "first_study",
    name: "Primeiro Estudo",
    description: "Completou o primeiro estudo bíblico",
    category: "study",
    icon_url: "/assets/achievements/first-study.png",
    points_reward: 50,
    difficulty: "easy",
    requirements: "Completar o primeiro estudo bíblico"
  },
  {
    id: "2",
    code: "bible_explorer",
    name: "Explorador da Palavra",
    description: "Leu 10 capítulos da Bíblia",
    category: "bible",
    icon_url: "/assets/achievements/bible-explorer.png",
    points_reward: 75,
    difficulty: "medium",
    requirements: "Ler 10 capítulos da Bíblia"
  },
  {
    id: "3",
    code: "dedicated_disciple",
    name: "Discípulo Dedicado",
    description: "Manteve uma sequência de 7 dias de estudos",
    category: "contribution",
    icon_url: "/assets/achievements/dedicated-disciple.png",
    points_reward: 100,
    difficulty: "medium",
    requirements: "Manter uma sequência de 7 dias de estudos"
  },
  {
    id: "4",
    code: "social_light",
    name: "Luz nas Redes",
    description: "Compartilhou 5 versículos nas redes sociais",
    category: "contribution",
    icon_url: "/assets/achievements/social-light.png",
    points_reward: 50,
    difficulty: "easy",
    requirements: "Compartilhar 5 versículos nas redes sociais"
  },
  {
    id: "5",
    code: "ai_apprentice",
    name: "Aprendiz da IA",
    description: "Fez 10 perguntas no chat espiritual",
    category: "chat",
    icon_url: "/assets/achievements/ai-apprentice.png",
    points_reward: 60,
    difficulty: "easy",
    requirements: "Fazer 10 perguntas no chat espiritual"
  }
];

const mockUserAchievements: UserAchievement[] = [
  {
    id: "ua1",
    user_id: "user123",
    achievement_id: "1",
    achievement: mockAchievements[0],
    earned_at: new Date(Date.now() - 1000 * 60 * 60 * 24 * 7).toISOString(), // 7 dias atrás
    seen: false
  },
  {
    id: "ua3",
    user_id: "user123",
    achievement_id: "3",
    achievement: mockAchievements[2],
    earned_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 horas atrás
    seen: false
  }
];

const mockPointTransactions: PointTransaction[] = [
  {
    id: "pt1",
    user_id: "user123",
    action: "daily_login",
    amount: 5,
    description: "Login diário",
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString() // 2 horas atrás
  },
  {
    id: "pt2",
    user_id: "user123",
    action: "study_completed",
    amount: 25,
    description: "Completou o estudo 'Encontrando Paz'",
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString() // 3 horas atrás
  },
  {
    id: "pt3",
    user_id: "user123",
    action: "achievement_unlocked",
    amount: 100,
    description: "Desbloqueou a conquista 'Discípulo Dedicado'",
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString() // 2 horas atrás
  },
  {
    id: "pt4",
    user_id: "user123",
    action: "reflection_added",
    amount: 15,
    description: "Adicionou uma reflexão ao estudo",
    created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString() // 30 minutos atrás
  },
  {
    id: "pt5",
    user_id: "user123",
    action: "streak_continued",
    amount: 5,
    description: "Manteve sequência de 7 dias",
    created_at: new Date().toISOString() // Agora
  }
];

const mockNotifications: GamificationNotification[] = [
  {
    id: "notif1",
    user_id: "user123",
    type: "achievement_unlocked",
    title: "Nova Conquista!",
    message: "Você desbloqueou a conquista 'Discípulo Dedicado'",
    image_url: "/assets/achievements/dedicated-disciple.png",
    is_read: false,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), // 2 horas atrás
    data: {
      achievement_id: "3"
    }
  },
  {
    id: "notif2",
    user_id: "user123",
    type: "level_up",
    title: "Subiu de Nível!",
    message: "Você avançou para o nível 3: 'Dedicado'",
    is_read: true,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), // 1 dia atrás
    data: {
      level: 3,
      points: 320
    }
  }
];

// Mock user points para desenvolvimento
const mockUserPoints: UserPoints = {
  id: "up1",
  user_id: "user123",
  total_points: 345,
  level: 3,
  next_level_threshold: 600,
  last_updated: new Date().toISOString()
};

// Contexto inicial
const GamificationContext = createContext<GamificationContextType>({
  userPoints: null,
  userLevel: null,
  achievements: [],
  userAchievements: [],
  unlockedAchievements: [],
  pointTransactions: [],
  notifications: [],
  isLoading: false,
  error: null,
  
  fetchUserPoints: async () => {},
  fetchAchievements: async () => {},
  fetchUserAchievements: async () => {},
  fetchPointTransactions: async () => {},
  fetchNotifications: async () => {},
  
  awardPoints: async () => {},
  markNotificationAsRead: async () => {},
  markAllNotificationsAsRead: async () => {},
  dismissNotification: async () => {},
  
  getCurrentLevel: () => null,
  getNextLevelProgress: () => 0,
  hasNewNotifications: () => false,
  getUnreadNotificationsCount: () => 0,
  addPoints: () => {},
  subtractPoints: () => {},
  refreshUserData: async () => {},
  dismissAchievementNotification: () => {},
  
  handleLoginSuccess: () => {},
  handleStudyCompleted: () => {},
  handleStudyStarted: () => {},
  handleReflectionAdded: () => {},
  handleVerseShared: () => {},
});

interface GamificationProviderProps {
  children: ReactNode;
}

export const GamificationProvider: React.FC<GamificationProviderProps> = ({ children }) => {
  // Estados
  const [userPoints, setUserPoints] = useState<UserPoints | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [userAchievements, setUserAchievements] = useState<UserAchievement[]>([]);
  const [unlockedAchievements, setUnlockedAchievements] = useState<UserAchievement[]>([]);
  const [pointTransactions, setPointTransactions] = useState<PointTransaction[]>([]);
  const [notifications, setNotifications] = useState<GamificationNotification[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Inicialização - Carregando dados do localStorage para desenvolvimento
  useEffect(() => {
    const loadMockData = async () => {
      try {
        setIsLoading(true);
        
        // Simulação da carga de dados
        await new Promise(resolve => setTimeout(resolve, 500));
        
        setUserPoints(mockUserPoints);
        setAchievements(mockAchievements);
        setUserAchievements(mockUserAchievements);
        setPointTransactions(mockPointTransactions);
        setNotifications(mockNotifications);
        
        setIsLoading(false);
      } catch (error) {
        setError('Erro ao carregar dados de gamificação');
        setIsLoading(false);
      }
    };
    
    loadMockData();
  }, []);
  
  // Métodos para buscar dados do backend (simulados para desenvolvimento)
  const fetchUserPoints = async () => {
    try {
      setIsLoading(true);
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setUserPoints(mockUserPoints);
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao buscar pontos do usuário');
      setIsLoading(false);
    }
  };
  
  const fetchAchievements = async () => {
    try {
      setIsLoading(true);
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setAchievements(mockAchievements);
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao buscar conquistas');
      setIsLoading(false);
    }
  };
  
  const fetchUserAchievements = async () => {
    try {
      setIsLoading(true);
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setUserAchievements(mockUserAchievements);
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao buscar conquistas do usuário');
      setIsLoading(false);
    }
  };
  
  const fetchPointTransactions = async (limit?: number) => {
    try {
      setIsLoading(true);
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      const transactions = limit 
        ? mockPointTransactions.slice(0, limit) 
        : mockPointTransactions;
      
      setPointTransactions(transactions);
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao buscar transações de pontos');
      setIsLoading(false);
    }
  };
  
  const fetchNotifications = async () => {
    try {
      setIsLoading(true);
      // Simulação de API
      await new Promise(resolve => setTimeout(resolve, 300));
      
      setNotifications(mockNotifications);
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao buscar notificações');
      setIsLoading(false);
    }
  };
  
  // Utilitários para manipulação de pontos
  const awardPoints = async (action: PointActionType, customDescription?: string) => {
    if (!userPoints) return;
    
    try {
      // Pegar a pontuação configurada para esta ação
      const points = POINTS_BY_ACTION[action] || 0;
      if (points === 0) return;
      
      // Descrição padrão baseada na ação
      const defaultDescriptions: Record<PointActionType, string> = {
        daily_login: "Login diário",
        study_completed: "Estudo concluído",
        study_started: "Novo estudo iniciado",
        reflection_added: "Reflexão adicionada",
        verse_shared: "Versículo compartilhado",
        streak_continued: "Sequência de dias mantida",
        achievement_unlocked: "Nova conquista desbloqueada",
        first_chat: "Primeira conversa com IA",
        daily_devotional: "Devocional diário",
        watched_ad: "Anúncio assistido",
        streak_milestone: "Marco de sequência atingido"
      };
      
      const description = customDescription || defaultDescriptions[action];
      
      // Criar a transação
      const transaction: PointTransaction = {
        id: uuidv4(),
        user_id: userPoints.user_id,
        action,
        amount: points,
        description,
        created_at: new Date().toISOString()
      };
      
      // Atualizar os pontos do usuário
      const newTotal = userPoints.total_points + points;
      
      // Verificar se o usuário subiu de nível
      const currentLevel = getCurrentLevel();
      
      // Atualizar estados
      setUserPoints({
        ...userPoints,
        total_points: newTotal,
        last_updated: new Date().toISOString()
      });
      
      setPointTransactions(prev => [transaction, ...prev]);
      
      // Verificar se o usuário subiu de nível
      const newLevel = LEVELS.find(level => 
        newTotal >= level.min_points && newTotal <= level.max_points
      );
      
      if (currentLevel && newLevel && newLevel.level > currentLevel.level) {
        // Criar notificação de level up
        const levelUpNotification: GamificationNotification = {
          id: uuidv4(),
          user_id: userPoints.user_id,
          type: "level_up",
          title: "Subiu de Nível!",
          message: `Você avançou para o nível ${newLevel.level}: '${newLevel.name}'`,
          is_read: false,
          created_at: new Date().toISOString(),
          data: {
            level: newLevel.level,
            points: newTotal
          }
        };
        
        setNotifications(prev => [levelUpNotification, ...prev]);
      }
      
      // Para desenvolvimento, simular salvamento no localStorage
      localStorage.setItem('userPoints', JSON.stringify({
        ...userPoints,
        total_points: newTotal,
        last_updated: new Date().toISOString()
      }));
      
    } catch (error) {
      setError('Erro ao adicionar pontos');
    }
  };
  
  // Manipulação simplificada de pontos
  const addPoints = (amount: number, reason: string) => {
    if (!userPoints) return;
    
    try {
      // Criar a transação
      const transaction: PointTransaction = {
        id: uuidv4(),
        user_id: userPoints.user_id,
        action: 'achievement_unlocked' as PointActionType, // Ação genérica
        amount,
        description: reason,
        created_at: new Date().toISOString()
      };
      
      // Atualizar os pontos do usuário
      const newTotal = userPoints.total_points + amount;
      
      // Atualizar estados
      setUserPoints({
        ...userPoints,
        total_points: newTotal,
        last_updated: new Date().toISOString()
      });
      
      setPointTransactions(prev => [transaction, ...prev]);
      
    } catch (error) {
      setError('Erro ao adicionar pontos');
    }
  };
  
  const subtractPoints = (amount: number, reason: string) => {
    if (!userPoints) return;
    
    try {
      // Não permitir pontos negativos
      if (userPoints.total_points < amount) {
        setError('Pontos insuficientes');
        return;
      }
      
      // Criar a transação
      const transaction: PointTransaction = {
        id: uuidv4(),
        user_id: userPoints.user_id,
        action: 'achievement_unlocked' as PointActionType, // Ação genérica
        amount: -amount,
        description: reason,
        created_at: new Date().toISOString()
      };
      
      // Atualizar os pontos do usuário
      const newTotal = userPoints.total_points - amount;
      
      // Atualizar estados
      setUserPoints({
        ...userPoints,
        total_points: newTotal,
        last_updated: new Date().toISOString()
      });
      
      setPointTransactions(prev => [transaction, ...prev]);
      
    } catch (error) {
      setError('Erro ao subtrair pontos');
    }
  };
  
  // Manipulação de notificações
  const markNotificationAsRead = async (notificationId: string) => {
    try {
      setNotifications(prev => 
        prev.map(notification => 
          notification.id === notificationId 
            ? { ...notification, is_read: true } 
            : notification
        )
      );
    } catch (error) {
      setError('Erro ao marcar notificação como lida');
    }
  };
  
  const markAllNotificationsAsRead = async () => {
    try {
      setNotifications(prev => 
        prev.map(notification => ({ ...notification, is_read: true }))
      );
    } catch (error) {
      setError('Erro ao marcar todas notificações como lidas');
    }
  };
  
  const dismissNotification = async (notificationId: string) => {
    try {
      setNotifications(prev => 
        prev.filter(notification => notification.id !== notificationId)
      );
    } catch (error) {
      setError('Erro ao descartar notificação');
    }
  };
  
  const dismissAchievementNotification = (achievementId: string) => {
    try {
      setNotifications(prev => 
        prev.filter(notification => 
          !(notification.type === 'achievement_unlocked' && 
            notification.data?.achievement_id === achievementId)
        )
      );
    } catch (error) {
      setError('Erro ao descartar notificação de conquista');
    }
  };
  
  // Utilitários
  const getCurrentLevel = useCallback((): Level | null => {
    if (!userPoints) return null;
    
    const currentLevel = LEVELS.find(level => 
      userPoints.total_points >= level.min_points && 
      userPoints.total_points <= level.max_points
    );
    
    return currentLevel || null;
  }, [userPoints]);
  
  const getNextLevelProgress = useCallback((): number => {
    if (!userPoints) return 0;
    
    const currentLevel = getCurrentLevel();
    if (!currentLevel) return 0;
    
    // Se estiver no último nível
    if (currentLevel.level === LEVELS[LEVELS.length - 1].level) {
      return 100; // 100% de progresso
    }
    
    const nextLevel = LEVELS.find(level => level.level === currentLevel.level + 1);
    if (!nextLevel) return 0;
    
    const pointsInCurrentLevel = userPoints.total_points - currentLevel.min_points;
    const levelRange = nextLevel.min_points - currentLevel.min_points;
    
    const progress = (pointsInCurrentLevel / levelRange) * 100;
    return Math.min(Math.max(progress, 0), 100); // Garantir entre 0 e 100
  }, [userPoints, getCurrentLevel]);
  
  const hasNewNotifications = useCallback((): boolean => {
    return notifications.some(notification => !notification.is_read);
  }, [notifications]);
  
  const getUnreadNotificationsCount = useCallback((): number => {
    return notifications.filter(notification => !notification.is_read).length;
  }, [notifications]);
  
  // Refresh dos dados do usuário
  const refreshUserData = async () => {
    try {
      setIsLoading(true);
      
      // Simulação de múltiplas chamadas
      await Promise.all([
        fetchUserPoints(),
        fetchAchievements(),
        fetchUserAchievements(),
        fetchPointTransactions(10), // Últimas 10 transações
        fetchNotifications()
      ]);
      
      setIsLoading(false);
    } catch (error) {
      setError('Erro ao atualizar dados do usuário');
      setIsLoading(false);
    }
  };
  
  // Handlers de eventos de outras features
  const handleLoginSuccess = () => {
    awardPoints('daily_login');
  };
  
  const handleStudyCompleted = (studyTitle: string) => {
    awardPoints('study_completed', `Completou o estudo: ${studyTitle}`);
    
    // Verificar conquistas relacionadas a estudos
    const studyCompletedAchievements = mockAchievements.filter(
      achievement => achievement.category === "study" && 
      achievement.requirements.includes("Completar o primeiro estudo bíblico")
    );
    
    // Verificar se alguma conquista deve ser desbloqueada
    studyCompletedAchievements.forEach(achievement => {
      // Contar quantos estudos completados já temos nas transações
      const studiesCompleted = pointTransactions.filter(
        transaction => transaction.action === 'study_completed'
      ).length + 1; // +1 porque acabamos de completar mais um
      
      // Se atingiu a condição e ainda não tem a conquista
      if (
        studiesCompleted >= 1 &&
        !userAchievements.some(ua => ua.achievement_id === achievement.id)
      ) {
        // Desbloquear conquista
        const newAchievement: UserAchievement = {
          id: uuidv4(),
          user_id: userPoints?.user_id || 'user123',
          achievement_id: achievement.id,
          achievement,
          earned_at: new Date().toISOString(),
          seen: false
        };
        
        // Adicionar à lista de conquistas do usuário
        setUserAchievements(prev => [...prev, newAchievement]);
        
        // Adicionar aos desbloqueados recentemente
        setUnlockedAchievements(prev => [...prev, newAchievement]);
        
        // Criar notificação
        const achievementNotification: GamificationNotification = {
          id: uuidv4(),
          user_id: userPoints?.user_id || 'user123',
          type: 'achievement_unlocked',
          title: 'Nova Conquista!',
          message: `Você desbloqueou: ${achievement.name}`,
          image_url: achievement.icon_url,
          is_read: false,
          created_at: new Date().toISOString(),
          data: {
            achievement_id: achievement.id
          }
        };
        
        setNotifications(prev => [achievementNotification, ...prev]);
        
        // Dar pontos pela conquista
        addPoints(achievement.points_reward, `Desbloqueou: ${achievement.name}`);
      }
    });
  };
  
  const handleStudyStarted = (studyTitle: string) => {
    awardPoints('study_started', `Iniciou o estudo: ${studyTitle}`);
  };
  
  const handleReflectionAdded = () => {
    awardPoints('reflection_added');
  };
  
  const handleVerseShared = () => {
    awardPoints('verse_shared');
  };
  
  return (
    <GamificationContext.Provider value={{
      userPoints,
      userLevel: getCurrentLevel(),
      achievements,
      userAchievements,
      unlockedAchievements,
      pointTransactions,
      notifications,
      isLoading,
      error,
      
      fetchUserPoints,
      fetchAchievements,
      fetchUserAchievements,
      fetchPointTransactions,
      fetchNotifications,
      
      awardPoints,
      markNotificationAsRead,
      markAllNotificationsAsRead,
      dismissNotification,
      
      getCurrentLevel,
      getNextLevelProgress,
      hasNewNotifications,
      getUnreadNotificationsCount,
      addPoints,
      subtractPoints,
      refreshUserData,
      dismissAchievementNotification,
      
      handleLoginSuccess,
      handleStudyCompleted,
      handleStudyStarted,
      handleReflectionAdded,
      handleVerseShared,
    }}>
      {children}
    </GamificationContext.Provider>
  );
};

export const useGamification = () => useContext(GamificationContext); 