import { useQuery, useMutation, useQueryClient } from 'react-query';
import adminService from '../api/adminService';
import { 
  MaintenanceTask, 
  SystemConfig, 
  LogFilterParams, 
  UserFilterParams, 
  DashboardPeriod 
} from '../types';

// Enum com as chaves para as queries do React Query
export enum AdminQueryKeys {
  DASHBOARD = 'admin-dashboard',
  METRICS = 'admin-metrics',
  USERS = 'admin-users',
  USER_DETAILS = 'admin-user-details',
  LOGS = 'admin-logs',
  LOG_DETAILS = 'admin-log-details',
  MAINTENANCE = 'admin-maintenance',
  CONFIGS = 'admin-configs',
  BACKUPS = 'admin-backups',
  REPORTS = 'admin-reports',
}

/**
 * Hook React Query para dados do Dashboard
 */
export const useDashboardQuery = (period: DashboardPeriod) => {
  return useQuery(
    [AdminQueryKeys.DASHBOARD, period],
    () => adminService.getDashboardData(period),
    {
      staleTime: 5 * 60 * 1000, // 5 minutos
      refetchOnWindowFocus: true,
    }
  );
};

/**
 * Hook React Query para métricas do sistema
 */
export const useSystemMetricsQuery = () => {
  return useQuery(
    AdminQueryKeys.METRICS,
    () => adminService.getSystemMetrics(),
    {
      staleTime: 3 * 60 * 1000, // 3 minutos
      refetchOnWindowFocus: true,
    }
  );
};

/**
 * Hook React Query para listar usuários
 */
export const useUsersQuery = (params: UserFilterParams = {}) => {
  return useQuery(
    [AdminQueryKeys.USERS, params],
    () => adminService.getUsers(params),
    {
      keepPreviousData: true,
      staleTime: 60 * 1000, // 1 minuto
    }
  );
};

/**
 * Hook React Query para detalhes de um usuário
 */
export const useUserDetailsQuery = (userId: string) => {
  return useQuery(
    [AdminQueryKeys.USER_DETAILS, userId],
    () => adminService.getUserDetails(userId),
    {
      enabled: !!userId,
      staleTime: 60 * 1000, // 1 minuto
    }
  );
};

/**
 * Hook React Query para bloquear/desbloquear usuário
 */
export const useToggleUserBlockMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ userId, isBlocked }: { userId: string; isBlocked: boolean }) => 
      adminService.toggleUserBlock(userId, isBlocked),
    {
      onSuccess: (_, { userId }) => {
        // Invalidar cache do usuário específico e da lista
        queryClient.invalidateQueries([AdminQueryKeys.USER_DETAILS, userId]);
        queryClient.invalidateQueries(AdminQueryKeys.USERS);
      }
    }
  );
};

/**
 * Hook React Query para adicionar nota a um usuário
 */
export const useAddUserNoteMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ userId, note }: { userId: string; note: string }) => 
      adminService.addUserNote(userId, note),
    {
      onSuccess: (_, { userId }) => {
        // Invalidar cache do usuário específico
        queryClient.invalidateQueries([AdminQueryKeys.USER_DETAILS, userId]);
      }
    }
  );
};

/**
 * Hook React Query para listar logs
 */
export const useLogsQuery = (params: LogFilterParams = {}) => {
  return useQuery(
    [AdminQueryKeys.LOGS, params],
    () => adminService.getLogs(params),
    {
      keepPreviousData: true,
      staleTime: 30 * 1000, // 30 segundos
    }
  );
};

/**
 * Hook React Query para detalhes de um log
 */
export const useLogDetailsQuery = (logId: string) => {
  return useQuery(
    [AdminQueryKeys.LOG_DETAILS, logId],
    () => adminService.getLogDetails(logId),
    {
      enabled: !!logId,
      staleTime: 5 * 60 * 1000, // 5 minutos
    }
  );
};

/**
 * Hook React Query para tarefas de manutenção
 */
export const useMaintenanceTasksQuery = () => {
  return useQuery(
    AdminQueryKeys.MAINTENANCE,
    () => adminService.getMaintenanceTasks(),
    {
      staleTime: 60 * 1000, // 1 minuto
      refetchInterval: 60 * 1000, // Refetch a cada minuto
    }
  );
};

/**
 * Hook React Query para criar tarefa de manutenção
 */
export const useCreateMaintenanceTaskMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    (task: Omit<MaintenanceTask, 'id' | 'created_by'>) => 
      adminService.createMaintenanceTask(task),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(AdminQueryKeys.MAINTENANCE);
      }
    }
  );
};

/**
 * Hook React Query para atualizar status de tarefa de manutenção
 */
export const useUpdateMaintenanceTaskStatusMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ taskId, status, error_message }: { taskId: string; status: string; error_message?: string }) => 
      adminService.updateMaintenanceTaskStatus(taskId, status, error_message),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(AdminQueryKeys.MAINTENANCE);
      }
    }
  );
};

/**
 * Hook React Query para configurações do sistema
 */
export const useSystemConfigsQuery = () => {
  return useQuery(
    AdminQueryKeys.CONFIGS,
    () => adminService.getSystemConfigs(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutos
    }
  );
};

/**
 * Hook React Query para atualizar configuração
 */
export const useUpdateSystemConfigMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ configId, value }: { configId: string; value: string }) => 
      adminService.updateSystemConfig(configId, value),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(AdminQueryKeys.CONFIGS);
      }
    }
  );
};

/**
 * Hook React Query para adicionar configuração
 */
export const useAddSystemConfigMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    (config: Omit<SystemConfig, 'id' | 'updated_at' | 'updated_by'>) => 
      adminService.addSystemConfig(config),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(AdminQueryKeys.CONFIGS);
      }
    }
  );
};

/**
 * Hook React Query para iniciar backup
 */
export const useTriggerBackupMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    () => adminService.triggerBackup(),
    {
      onSuccess: () => {
        // Aguarda 5 segundos e então recarrega a lista de backups
        setTimeout(() => {
          queryClient.invalidateQueries(AdminQueryKeys.BACKUPS);
        }, 5000);
      }
    }
  );
};

/**
 * Hook React Query para verificar status do backup
 */
export const useBackupStatusQuery = (jobId: string) => {
  return useQuery(
    ['backup-status', jobId],
    () => adminService.checkBackupStatus(jobId),
    {
      enabled: !!jobId,
      refetchInterval: (data) => {
        // Refetch a cada 2 segundos até completar
        return data?.status === 'completed' ? false : 2000;
      }
    }
  );
};

/**
 * Hook React Query para listar backups
 */
export const useBackupsListQuery = () => {
  return useQuery(
    AdminQueryKeys.BACKUPS,
    () => adminService.listBackups(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutos
    }
  );
};

/**
 * Hook React Query para gerar relatório
 */
export const useGenerateReportMutation = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ start_date, end_date, type }: { start_date: string; end_date: string; type: string }) => 
      adminService.generateReport(start_date, end_date, type),
    {
      onSuccess: () => {
        // Aguarda 5 segundos e então recarrega a lista de relatórios
        setTimeout(() => {
          queryClient.invalidateQueries(AdminQueryKeys.REPORTS);
        }, 5000);
      }
    }
  );
};

/**
 * Hook React Query para listar relatórios
 */
export const useReportsListQuery = () => {
  return useQuery(
    AdminQueryKeys.REPORTS,
    () => adminService.listReports(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutos
    }
  );
};

/**
 * Função para atualizar todos os dados do painel administrativo
 */
export const refreshAdminData = (queryClient: ReturnType<typeof useQueryClient>) => {
  queryClient.invalidateQueries(AdminQueryKeys.DASHBOARD);
  queryClient.invalidateQueries(AdminQueryKeys.METRICS);
  queryClient.invalidateQueries(AdminQueryKeys.USERS);
  queryClient.invalidateQueries(AdminQueryKeys.LOGS);
  queryClient.invalidateQueries(AdminQueryKeys.MAINTENANCE);
  queryClient.invalidateQueries(AdminQueryKeys.CONFIGS);
  queryClient.invalidateQueries(AdminQueryKeys.BACKUPS);
  queryClient.invalidateQueries(AdminQueryKeys.REPORTS);
};

const useAdminQuery = {
  // Queries
  useDashboardQuery,
  useSystemMetricsQuery,
  useUsersQuery,
  useUserDetailsQuery,
  useLogsQuery,
  useLogDetailsQuery,
  useMaintenanceTasksQuery,
  useSystemConfigsQuery,
  useBackupStatusQuery,
  useBackupsListQuery,
  useReportsListQuery,

  // Mutations
  useToggleUserBlockMutation,
  useAddUserNoteMutation,
  useCreateMaintenanceTaskMutation,
  useUpdateMaintenanceTaskStatusMutation,
  useUpdateSystemConfigMutation,
  useAddSystemConfigMutation,
  useTriggerBackupMutation,
  useGenerateReportMutation,

  // Utils
  refreshAdminData
};

export default useAdminQuery; 