import React, { useState, useEffect } from 'react';
import { SystemSettings } from '../../types';
import { useAdmin } from '../../contexts/AdminContext';

interface SystemSettingsFormProps {
  settings: SystemSettings;
  onSave: (settings: SystemSettings) => Promise<void>;
  isLoading: boolean;
}

export const SystemSettingsForm: React.FC<SystemSettingsFormProps> = ({
  settings,
  onSave,
  isLoading
}) => {
  const [formData, setFormData] = useState<SystemSettings>(settings);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);

  // Atualizar o estado do formulário quando as configurações mudam
  useEffect(() => {
    setFormData(settings);
  }, [settings]);

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    // Lidar com inputs aninhados (objetos dentro de objetos)
    if (name.includes('.')) {
      const [parentKey, childKey] = name.split('.');
      
      if (parentKey === 'chatLimits' && formData.chatLimits) {
        setFormData({
          ...formData,
          chatLimits: {
            ...formData.chatLimits,
            [childKey]: type === 'number' ? Number(value) : value
          }
        });
      } else if (parentKey === 'studyLimits' && formData.studyLimits) {
        setFormData({
          ...formData,
          studyLimits: {
            ...formData.studyLimits,
            [childKey]: type === 'number' ? Number(value) : value
          }
        });
      } else if (parentKey === 'notificationSettings' && formData.notificationSettings) {
        setFormData({
          ...formData,
          notificationSettings: {
            ...formData.notificationSettings,
            [childKey]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
          }
        });
      } else if (parentKey === 'securitySettings' && formData.securitySettings) {
        setFormData({
          ...formData,
          securitySettings: {
            ...formData.securitySettings,
            [childKey]: type === 'checkbox' 
              ? (e.target as HTMLInputElement).checked 
              : type === 'number' ? Number(value) : value
          }
        });
      } else if (parentKey === 'backupSettings' && formData.backupSettings) {
        setFormData({
          ...formData,
          backupSettings: {
            ...formData.backupSettings,
            [childKey]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
          }
        });
      } else if (parentKey === 'apiSettings' && formData.apiSettings) {
        setFormData({
          ...formData,
          apiSettings: {
            ...formData.apiSettings,
            [childKey]: type === 'number' ? Number(value) : value
          }
        });
      }
    } else {
      // Lidar com inputs simples
      setFormData({
        ...formData,
        [name]: type === 'checkbox' 
          ? (e.target as HTMLInputElement).checked 
          : type === 'number' ? Number(value) : value
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setSaveSuccess(false);
    setSaveError(null);
    
    try {
      await onSave(formData);
      setSaveSuccess(true);
      
      // Limpar a mensagem de sucesso após 3 segundos
      setTimeout(() => {
        setSaveSuccess(false);
      }, 3000);
    } catch (error) {
      setSaveError('Erro ao salvar configurações. Tente novamente.');
      console.error('Error saving settings:', error);
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        <div className="h-12 bg-gray-100 rounded"></div>
        <div className="h-12 bg-gray-100 rounded"></div>
        <div className="h-12 bg-gray-100 rounded"></div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Seção: Modo de Manutenção */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-3">Sistema</h3>
        
        <div className="flex items-center mb-4">
          <input
            type="checkbox"
            id="maintenanceMode"
            name="maintenanceMode"
            checked={formData.maintenanceMode}
            onChange={handleInputChange}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label htmlFor="maintenanceMode" className="ml-2 block text-sm text-gray-900">
            Modo de Manutenção
          </label>
        </div>
        
        <p className="text-sm text-gray-500">
          Quando ativado, os usuários verão uma página de manutenção e não poderão acessar o sistema.
        </p>
      </div>

      {/* Seção: Limites */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-3">Limites do Plano Free</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="chatLimits.freeLimit" className="block text-sm font-medium text-gray-700 mb-1">
              Mensagens por dia (Chat IA)
            </label>
            <input
              type="number"
              id="chatLimits.freeLimit"
              name="chatLimits.freeLimit"
              value={formData.chatLimits.freeLimit}
              onChange={handleInputChange}
              min="0"
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          
          <div>
            <label htmlFor="studyLimits.freeLimit" className="block text-sm font-medium text-gray-700 mb-1">
              Dias de estudo por mês
            </label>
            <input
              type="number"
              id="studyLimits.freeLimit"
              name="studyLimits.freeLimit"
              value={formData.studyLimits.freeLimit}
              onChange={handleInputChange}
              min="0"
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      {/* Seção: Notificações */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-3">Configurações de Notificações</h3>
        
        <div className="space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              id="notificationSettings.emailNotifications"
              name="notificationSettings.emailNotifications"
              checked={formData.notificationSettings.emailNotifications}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="notificationSettings.emailNotifications" className="ml-2 block text-sm text-gray-900">
              Permitir notificações por e-mail
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              id="notificationSettings.pushNotifications"
              name="notificationSettings.pushNotifications"
              checked={formData.notificationSettings.pushNotifications}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="notificationSettings.pushNotifications" className="ml-2 block text-sm text-gray-900">
              Permitir notificações push
            </label>
          </div>
          
          <div>
            <label htmlFor="notificationSettings.reminderFrequency" className="block text-sm font-medium text-gray-700 mb-1">
              Frequência de lembretes
            </label>
            <select
              id="notificationSettings.reminderFrequency"
              name="notificationSettings.reminderFrequency"
              value={formData.notificationSettings.reminderFrequency}
              onChange={handleInputChange}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="daily">Diária</option>
              <option value="weekly">Semanal</option>
              <option value="monthly">Mensal</option>
              <option value="never">Nunca</option>
            </select>
          </div>
        </div>
      </div>

      {/* Seção: APIs */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-medium mb-3">Configurações de APIs</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="apiSettings.openaiModelVersion" className="block text-sm font-medium text-gray-700 mb-1">
              Versão do Modelo OpenAI
            </label>
            <select
              id="apiSettings.openaiModelVersion"
              name="apiSettings.openaiModelVersion"
              value={formData.apiSettings.openaiModelVersion}
              onChange={handleInputChange}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-4-turbo">GPT-4 Turbo</option>
            </select>
          </div>
          
          <div>
            <label htmlFor="apiSettings.maxTokensPerRequest" className="block text-sm font-medium text-gray-700 mb-1">
              Máximo de tokens por requisição
            </label>
            <input
              type="number"
              id="apiSettings.maxTokensPerRequest"
              name="apiSettings.maxTokensPerRequest"
              value={formData.apiSettings.maxTokensPerRequest}
              onChange={handleInputChange}
              min="100"
              max="32000"
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      {/* Botões de Ação */}
      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={() => setFormData(settings)}
          className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Cancelar
        </button>
        
        <button
          type="submit"
          disabled={isSaving}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isSaving ? 'Salvando...' : 'Salvar Alterações'}
        </button>
      </div>

      {/* Mensagens de feedback */}
      {saveSuccess && (
        <div className="bg-green-50 p-4 rounded-md">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-green-800">
                Configurações salvas com sucesso!
              </p>
            </div>
          </div>
        </div>
      )}

      {saveError && (
        <div className="bg-red-50 p-4 rounded-md">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-red-800">
                {saveError}
              </p>
            </div>
          </div>
        </div>
      )}
    </form>
  );
}; 