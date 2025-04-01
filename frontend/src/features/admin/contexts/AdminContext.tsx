import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  AdminContextType,
  AdminUser,
  DashboardMetrics,
  SystemSettings,
  UserDetails,
  AdminActionLog,
  UserStatus,
  UserRole,
  TimeRange,
  AdminActionType,
  ChartData,
  ReportData,
} from '../types';
import { adminService } from '../services/adminService';

// Criação do contexto
export const AdminContext = createContext<AdminContextType>({
  // Estado
  currentUser: null,
  dashboard: null,
  systemSettings: null,
  users: [],
  actionLogs: [],
  isLoading: false,
  isLoadingUsers: false,
  error: null,

  // Ações - Usuários
  fetchUsers: async () => {},
  getUserDetails: async () => ({}) as UserDetails,
  updateUserStatus: async () => {},
  updateUserRole: async () => {},
  updateUser: async () => {},
  createUser: async () => {},
  deleteUser: async () => {},

  // Ações - Dashboard
  fetchDashboardMetrics: async () => {},
  getChartData: async () => ({}) as ChartData,
  getTopUsers: async () => [],

  // Ações - Configurações
  fetchSystemSettings: async () => {},
  updateSystemSettings: async () => {},
  toggleMaintenanceMode: async () => {},

  // Ações - Logs
  fetchActionLogs: async () => {},
  clearLogs: async () => {},

  // Ações - Relatórios
  generateReport: async () => ({}) as ReportData,
  getReportList: async () => [],
  downloadReport: async () => {},
});

interface AdminProviderProps {
  children: ReactNode;
}

export const AdminProvider: React.FC<AdminProviderProps> = ({ children }) => {
  // Estados
  const [currentUser, setCurrentUser] = useState<AdminUser | null>(null);
  const [dashboard, setDashboard] = useState<DashboardMetrics | null>(null);
  const [systemSettings, setSystemSettings] = useState<SystemSettings | null>(null);
  const [users, setUsers] = useState<UserDetails[]>([]);
  const [actionLogs, setActionLogs] = useState<AdminActionLog[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isLoadingUsers, setIsLoadingUsers] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Efeito para carregar usuário admin atual ao montar
  useEffect(() => {
    const loadInitialData = async () => {
      setIsLoading(true);
      try {
        const currentAdminUser = await adminService.getCurrentAdminUser();
        setCurrentUser(currentAdminUser);
      } catch (error) {
        setError('Erro ao carregar dados de administrador');
        console.error('Erro ao carregar dados de administrador:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadInitialData();
  }, []);

  // Ações - Usuários
  const fetchUsers = async (
    page: number = 1,
    limit: number = 10,
    query?: string,
    status?: UserStatus
  ): Promise<void> => {
    setIsLoadingUsers(true);
    setError(null);

    try {
      const fetchedUsers = await adminService.getUsers(page, limit, query, status);
      setUsers(fetchedUsers);
    } catch (error) {
      setError('Erro ao buscar usuários');
      console.error('Erro ao buscar usuários:', error);
    } finally {
      setIsLoadingUsers(false);
    }
  };

  const getUserDetails = async (userId: string): Promise<UserDetails> => {
    setIsLoading(true);
    setError(null);

    try {
      const userDetails = await adminService.getUserDetails(userId);
      return userDetails;
    } catch (error) {
      setError('Erro ao buscar detalhes do usuário');
      console.error('Erro ao buscar detalhes do usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateUserStatus = async (userId: string, status: UserStatus): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      await adminService.updateUserStatus(userId, status);

      // Atualizar o estado local
      setUsers(prevUsers =>
        prevUsers.map(user => (user.id === userId ? { ...user, status } : user))
      );
    } catch (error) {
      setError('Erro ao atualizar status do usuário');
      console.error('Erro ao atualizar status do usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateUserRole = async (userId: string, role: UserRole): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      await adminService.updateUserRole(userId, role);
    } catch (error) {
      setError('Erro ao atualizar função do usuário');
      console.error('Erro ao atualizar função do usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const updateUser = async (userData: {
    id: string;
    status?: UserStatus;
    role?: UserRole;
  }): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      if (userData.status) {
        await updateUserStatus(userData.id, userData.status);
      }

      if (userData.role) {
        await updateUserRole(userData.id, userData.role);
      }

      // Atualizar o estado local
      setUsers(prevUsers =>
        prevUsers.map(user =>
          user.id === userData.id
            ? {
                ...user,
                ...(userData.status && { status: userData.status }),
                ...(userData.role && { role: userData.role }),
              }
            : user
        )
      );
    } catch (error) {
      setError('Erro ao atualizar usuário');
      console.error('Erro ao atualizar usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const createUser = async (userData: Partial<UserDetails>): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const newUser = await adminService.createUser(userData);
      setUsers(prevUsers => [...prevUsers, newUser]);
    } catch (error) {
      setError('Erro ao criar usuário');
      console.error('Erro ao criar usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const deleteUser = async (userId: string): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      await adminService.deleteUser(userId);
      setUsers(prevUsers => prevUsers.filter(user => user.id !== userId));
    } catch (error) {
      setError('Erro ao excluir usuário');
      console.error('Erro ao excluir usuário:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Ações - Dashboard
  const fetchDashboardMetrics = async (timeRange?: TimeRange): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const metrics = await adminService.getDashboardMetrics(timeRange);
      setDashboard(metrics);
    } catch (error) {
      setError('Erro ao buscar métricas do dashboard');
      console.error('Erro ao buscar métricas do dashboard:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getChartData = async (metric: string, timeRange: TimeRange): Promise<ChartData> => {
    setIsLoading(true);
    setError(null);

    try {
      const chartData = await adminService.getChartData(metric, timeRange);
      return chartData;
    } catch (error) {
      setError('Erro ao buscar dados do gráfico');
      console.error('Erro ao buscar dados do gráfico:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const getTopUsers = async (): Promise<UserDetails[]> => {
    setIsLoading(true);
    setError(null);

    try {
      const topUsers = await adminService.getTopUsers();
      return topUsers;
    } catch (error) {
      setError('Erro ao buscar usuários mais ativos');
      console.error('Erro ao buscar usuários mais ativos:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Ações - Configurações
  const fetchSystemSettings = async (): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const settings = await adminService.getSystemSettings();
      setSystemSettings(settings);
    } catch (error) {
      setError('Erro ao buscar configurações do sistema');
      console.error('Erro ao buscar configurações do sistema:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateSystemSettings = async (settings: Partial<SystemSettings>): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const updatedSettings = await adminService.updateSystemSettings(settings);
      setSystemSettings(updatedSettings);
    } catch (error) {
      setError('Erro ao atualizar configurações do sistema');
      console.error('Erro ao atualizar configurações do sistema:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMaintenanceMode = async (enabled: boolean): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const updatedSettings = await adminService.toggleMaintenanceMode(enabled);
      setSystemSettings(updatedSettings);
    } catch (error) {
      setError('Erro ao alternar modo de manutenção');
      console.error('Erro ao alternar modo de manutenção:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Ações - Logs
  const fetchActionLogs = async (timeRange: TimeRange = 'last_7_days') => {
    try {
      setIsLoading(true);
      setError(null);
      const logs = await adminService.getActionLogs(1, 100);
      setActionLogs(logs);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar logs');
      console.error('Erro ao carregar logs:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const clearLogs = async (olderThan?: string) => {
    try {
      setIsLoading(true);
      setError(null);
      await adminService.clearLogs(olderThan);
      await fetchActionLogs();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao limpar logs');
      console.error('Erro ao limpar logs:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Ações - Relatórios
  const generateReport = async (type: string, timeRange: TimeRange): Promise<ReportData> => {
    setIsLoading(true);
    setError(null);

    try {
      const reportData = await adminService.generateReport(type, timeRange);
      return reportData;
    } catch (error) {
      setError('Erro ao gerar relatório');
      console.error('Erro ao gerar relatório:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const getReportList = async (): Promise<ReportData[]> => {
    setIsLoading(true);
    setError(null);

    try {
      const reports = await adminService.getReportList();
      return reports;
    } catch (error) {
      setError('Erro ao buscar lista de relatórios');
      console.error('Erro ao buscar lista de relatórios:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const downloadReport = async (reportId: string): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      await adminService.downloadReport(reportId);
    } catch (error) {
      setError('Erro ao baixar relatório');
      console.error('Erro ao baixar relatório:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Valor do contexto
  const contextValue: AdminContextType = {
    currentUser,
    dashboard,
    systemSettings,
    users,
    actionLogs,
    isLoading,
    isLoadingUsers,
    error,

    // Users
    fetchUsers,
    getUserDetails,
    updateUserStatus,
    updateUserRole,
    updateUser,
    createUser,
    deleteUser,

    // Dashboard
    fetchDashboardMetrics,
    getChartData,
    getTopUsers,

    // Settings
    fetchSystemSettings,
    updateSystemSettings,
    toggleMaintenanceMode,

    // Logs
    fetchActionLogs,
    clearLogs,

    // Reports
    generateReport,
    getReportList,
    downloadReport,
  };

  return <AdminContext.Provider value={contextValue}>{children}</AdminContext.Provider>;
};

// Hook personalizado para acessar o contexto
export const useAdmin = () => {
  const context = useContext(AdminContext);

  if (!context) {
    throw new Error('useAdmin deve ser usado dentro de um AdminProvider');
  }

  return context;
};
