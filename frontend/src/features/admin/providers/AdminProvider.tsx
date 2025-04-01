import React, { createContext, useContext, useState, ReactNode, useCallback, useEffect } from 'react';
import { useQueryClient } from 'react-query';
import { useToast } from '../../../shared/hooks/useToast';
import useAdminQuery from '../hooks/useAdminQuery';
import { AdminState } from '../types';

// Contexto do Admin
const AdminContext = createContext<AdminState | undefined>(undefined);

// Props para o AdminProvider
interface AdminProviderProps {
  children: ReactNode;
}

// Provider de Administração
export const AdminProvider: React.FC<AdminProviderProps> = ({ children }) => {
  const queryClient = useQueryClient();
  const toast = useToast();

  // Estado para controle de jobs em progresso
  const [activeBackupJobId, setActiveBackupJobId] = useState<string | null>(null);
  const [activeReportJobId, setActiveReportJobId] = useState<string | null>(null);
  const [isMaintenanceMode, setIsMaintenanceMode] = useState(false);

  // Estado para filtros aplicados
  const [activeUserFilters, setActiveUserFilters] = useState({});
  const [activeLogFilters, setActiveLogFilters] = useState({});

  // Queries para monitoramento de jobs
  const backupStatus = useAdminQuery.useBackupStatusQuery(activeBackupJobId || '');
  const { useSystemConfigsQuery } = useAdminQuery;
  const { data: systemConfigs } = useSystemConfigsQuery();

  // Verifica se o sistema está em modo de manutenção
  useEffect(() => {
    if (systemConfigs) {
      const maintenanceConfig = systemConfigs.find(config => 
        config.key === 'system.maintenance.enabled'
      );
      
      if (maintenanceConfig) {
        setIsMaintenanceMode(maintenanceConfig.value === 'true');
      }
    }
  }, [systemConfigs]);

  // Inicia um backup
  const startBackup = useCallback(async () => {
    try {
      const triggerBackupMutation = useAdminQuery.useTriggerBackupMutation();
      
      const result = await triggerBackupMutation.mutateAsync();
      setActiveBackupJobId(result.job_id);
      
      toast.info('O backup do sistema foi iniciado com sucesso.');
      
      return result.job_id;
    } catch (error) {
      toast.error('Não foi possível iniciar o backup do sistema.');
      return null;
    }
  }, [toast]);

  // Inicia geração de relatório
  const startReportGeneration = useCallback(async (start_date: string, end_date: string, type: string) => {
    try {
      const generateReportMutation = useAdminQuery.useGenerateReportMutation();
      
      const result = await generateReportMutation.mutateAsync({ start_date, end_date, type });
      setActiveReportJobId(result.job_id);
      
      toast.info('O relatório começou a ser gerado e estará disponível em breve.');
      
      return result.job_id;
    } catch (error) {
      toast.error('Não foi possível iniciar a geração do relatório.');
      return null;
    }
  }, [toast]);

  // Atualiza configuração do sistema
  const updateSystemConfig = useCallback(async (configId: string, value: string) => {
    try {
      const updateConfigMutation = useAdminQuery.useUpdateSystemConfigMutation();
      
      await updateConfigMutation.mutateAsync({ configId, value });
      
      toast.success('A configuração do sistema foi atualizada com sucesso.');
      
      return true;
    } catch (error) {
      toast.error('Não foi possível atualizar a configuração do sistema.');
      return false;
    }
  }, [toast]);

  // Alterna o modo de manutenção
  const toggleMaintenanceMode = useCallback(async (enabled: boolean) => {
    const success = await updateSystemConfig('system.maintenance.enabled', enabled ? 'true' : 'false');
    
    if (success) {
      setIsMaintenanceMode(enabled);
      
      toast.info(`O sistema agora está ${enabled ? 'em manutenção' : 'disponível'} para os usuários.`);
    }
    
    return success;
  }, [updateSystemConfig, toast]);

  // Atualiza todos os dados do admin
  const refreshAllData = useCallback(() => {
    useAdminQuery.refreshAdminData(queryClient);
    
    toast.success('Todos os dados do painel administrativo foram atualizados.');
  }, [queryClient, toast]);

  // Valores do contexto
  const contextValue: AdminState = {
    // Estado
    isMaintenanceMode,
    activeBackupJobId,
    activeReportJobId,
    activeUserFilters,
    activeLogFilters,
    
    // Setters
    setActiveUserFilters,
    setActiveLogFilters,
    
    // Ações
    startBackup,
    startReportGeneration,
    updateSystemConfig,
    toggleMaintenanceMode,
    refreshAllData
  };

  return (
    <AdminContext.Provider value={contextValue}>
      {children}
    </AdminContext.Provider>
  );
};

// Hook para usar o contexto
export const useAdmin = (): AdminState => {
  const context = useContext(AdminContext);
  
  if (context === undefined) {
    throw new Error('useAdmin must be used within an AdminProvider');
  }
  
  return context;
};

export default AdminProvider; 