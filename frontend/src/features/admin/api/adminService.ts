import { adminApi } from '../../../shared/services/api';
import { API_URLS } from '../../../shared/constants/apiUrls';
import {
  SystemMetrics,
  AdminUserDetails,
  AdminUserListResponse,
  SystemLog,
  SystemLogListResponse,
  MaintenanceTask,
  SystemConfig,
  DashboardData,
  DashboardPeriod,
  UserFilterParams,
  LogFilterParams
} from '../types';

/**
 * Serviço para comunicação com o MS-Admin
 * Implementação do item 10.8.1 do plano de migração
 */
const adminService = {
  /**
   * Obtém dados do dashboard
   */
  async getDashboardData(period: DashboardPeriod): Promise<DashboardData> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/dashboard?period=${period}`);
    return data;
  },

  /**
   * Obtém métricas do sistema
   */
  async getSystemMetrics(): Promise<SystemMetrics> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/metrics`);
    return data;
  },

  /**
   * Lista usuários com paginação e filtros
   */
  async getUsers(params: UserFilterParams = {}): Promise<AdminUserListResponse> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/users`, { params });
    return data;
  },

  /**
   * Obtém detalhes de um usuário específico
   */
  async getUserDetails(userId: string): Promise<AdminUserDetails> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/users/${userId}`);
    return data;
  },

  /**
   * Bloqueia ou desbloqueia um usuário
   */
  async toggleUserBlock(userId: string, isBlocked: boolean): Promise<{ success: boolean }> {
    const { data } = await adminApi.patch(`${API_URLS.ADMIN}/users/${userId}/block`, { is_blocked: isBlocked });
    return data;
  },

  /**
   * Adiciona nota administrativa a um usuário
   */
  async addUserNote(userId: string, note: string): Promise<{ success: boolean }> {
    const { data } = await adminApi.post(`${API_URLS.ADMIN}/users/${userId}/notes`, { note });
    return data;
  },

  /**
   * Lista logs do sistema com paginação e filtros
   */
  async getLogs(params: LogFilterParams = {}): Promise<SystemLogListResponse> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/logs`, { params });
    return data;
  },

  /**
   * Obtém detalhes de um log específico
   */
  async getLogDetails(logId: string): Promise<SystemLog> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/logs/${logId}`);
    return data;
  },

  /**
   * Lista tarefas de manutenção
   */
  async getMaintenanceTasks(): Promise<MaintenanceTask[]> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/maintenance`);
    return data;
  },

  /**
   * Cria uma nova tarefa de manutenção
   */
  async createMaintenanceTask(task: Omit<MaintenanceTask, 'id' | 'created_by'>): Promise<MaintenanceTask> {
    const { data } = await adminApi.post(`${API_URLS.ADMIN}/maintenance`, task);
    return data;
  },

  /**
   * Atualiza status de uma tarefa de manutenção
   */
  async updateMaintenanceTaskStatus(taskId: string, status: string, error_message?: string): Promise<MaintenanceTask> {
    const { data } = await adminApi.patch(`${API_URLS.ADMIN}/maintenance/${taskId}`, { 
      status, 
      error_message 
    });
    return data;
  },

  /**
   * Lista configurações do sistema
   */
  async getSystemConfigs(): Promise<SystemConfig[]> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/configs`);
    return data;
  },

  /**
   * Atualiza uma configuração do sistema
   */
  async updateSystemConfig(configId: string, value: string): Promise<SystemConfig> {
    const { data } = await adminApi.patch(`${API_URLS.ADMIN}/configs/${configId}`, { value });
    return data;
  },

  /**
   * Adiciona uma nova configuração do sistema
   */
  async addSystemConfig(config: Omit<SystemConfig, 'id' | 'updated_at' | 'updated_by'>): Promise<SystemConfig> {
    const { data } = await adminApi.post(`${API_URLS.ADMIN}/configs`, config);
    return data;
  },

  /**
   * Realiza backup do banco de dados
   */
  async triggerBackup(): Promise<{ job_id: string; status: string; message: string }> {
    const { data } = await adminApi.post(`${API_URLS.ADMIN}/backup`);
    return data;
  },

  /**
   * Verifica o status de um backup em andamento
   */
  async checkBackupStatus(jobId: string): Promise<{ status: string; progress: number; download_url?: string }> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/backup/${jobId}`);
    return data;
  },

  /**
   * Lista backups disponíveis
   */
  async listBackups(): Promise<{ id: string; date: string; size: number; download_url: string }[]> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/backups`);
    return data;
  },

  /**
   * Gera relatório de uso
   */
  async generateReport(start_date: string, end_date: string, type: string): Promise<{ job_id: string; status: string }> {
    const { data } = await adminApi.post(`${API_URLS.ADMIN}/reports/generate`, {
      start_date,
      end_date,
      type
    });
    return data;
  },

  /**
   * Lista relatórios disponíveis
   */
  async listReports(): Promise<{ id: string; type: string; date_range: { start: string; end: string }; created_at: string; download_url: string }[]> {
    const { data } = await adminApi.get(`${API_URLS.ADMIN}/reports`);
    return data;
  }
};

export default adminService; 