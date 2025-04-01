import React, { useState } from 'react';
import { useAdmin } from '../contexts/AdminContext';
import { SystemSettings } from '../types';

const SystemSettingsPage: React.FC = () => {
  const { systemSettings, isLoading, error, updateSystemSettings, toggleMaintenanceMode } =
    useAdmin();

  const [settings, setSettings] = useState<SystemSettings | null>(systemSettings);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  // Se as configurações do sistema forem carregadas após o componente ser montado
  React.useEffect(() => {
    if (systemSettings) {
      setSettings(systemSettings);
    }
  }, [systemSettings]);

  const handleChange = (section: keyof SystemSettings, field: string, value: any) => {
    if (!settings) return;

    // Clone the settings object
    const newSettings = JSON.parse(JSON.stringify(settings));
    // Update the specific field
    newSettings[section][field] = value;
    // Set the updated settings
    setSettings(newSettings);
  };

  const handleNestedChange = (
    section: keyof SystemSettings,
    nestedSection: string,
    field: string,
    value: any
  ) => {
    if (!settings) return;

    // Clone the settings object
    const newSettings = JSON.parse(JSON.stringify(settings));
    
    // Handle the case where field is empty (direct assignment)
    if (field === '') {
      newSettings[section][nestedSection] = value;
    } else {
      // Update the nested field
      newSettings[section][nestedSection][field] = value;
    }
    
    // Set the updated settings
    setSettings(newSettings);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!settings) return;

    setIsSaving(true);
    setSaveMessage('');

    try {
      await updateSystemSettings(settings);
      setSaveMessage('Configurações salvas com sucesso!');
      setTimeout(() => setSaveMessage(''), 3000);
    } catch (err) {
      setSaveMessage('Erro ao salvar configurações. Tente novamente.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleMaintenanceToggle = async () => {
    if (!settings) return;

    setIsSaving(true);
    try {
      await toggleMaintenanceMode(!settings.maintenanceMode);
      setSettings({
        ...settings,
        maintenanceMode: !settings.maintenanceMode,
      });
      setSaveMessage(
        `Modo de manutenção ${settings.maintenanceMode ? 'desativado' : 'ativado'} com sucesso!`
      );
      setTimeout(() => setSaveMessage(''), 3000);
    } catch (err) {
      setSaveMessage('Erro ao alterar modo de manutenção.');
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-100 text-red-800 rounded-md">
        <h3 className="font-bold">Erro ao carregar configurações</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!settings) {
    return (
      <div className="p-4">
        <p>Carregando configurações...</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Configurações do Sistema</h1>
        <div className="flex space-x-4">
          <button
            onClick={handleMaintenanceToggle}
            disabled={isSaving}
            className={`px-4 py-2 rounded-lg ${
              settings.maintenanceMode
                ? 'bg-yellow-500 hover:bg-yellow-600 text-white'
                : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
            }`}
          >
            {settings.maintenanceMode ? 'Desativar Modo Manutenção' : 'Ativar Modo Manutenção'}
          </button>
        </div>
      </div>

      {saveMessage && (
        <div
          className={`mb-4 p-3 rounded-md ${saveMessage.includes('sucesso') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
        >
          {saveMessage}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Limites de Uso */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Limites de Uso</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium mb-2">Limites de Chat</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Plano Free</label>
                  <input
                    type="number"
                    value={settings.chatLimits.freeLimit}
                    onChange={e =>
                      handleNestedChange('chatLimits', 'freeLimit', '', parseInt(e.target.value))
                    }
                    className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Plano Premium</label>
                  <input
                    type="number"
                    value={settings.chatLimits.premiumLimit}
                    onChange={e =>
                      handleNestedChange('chatLimits', 'premiumLimit', '', parseInt(e.target.value))
                    }
                    className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-medium mb-2">Limites de Estudo</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Plano Free</label>
                  <input
                    type="number"
                    value={settings.studyLimits.freeLimit}
                    onChange={e =>
                      handleNestedChange('studyLimits', 'freeLimit', '', parseInt(e.target.value))
                    }
                    className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Plano Premium</label>
                  <input
                    type="number"
                    value={settings.studyLimits.premiumLimit}
                    onChange={e =>
                      handleNestedChange(
                        'studyLimits',
                        'premiumLimit',
                        '',
                        parseInt(e.target.value)
                      )
                    }
                    className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Notificações */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Configurações de Notificações</h2>

          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="emailNotifications"
                checked={settings.notificationSettings.emailNotifications}
                onChange={e =>
                  handleNestedChange(
                    'notificationSettings',
                    'emailNotifications',
                    '',
                    e.target.checked
                  )
                }
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="emailNotifications" className="text-sm font-medium text-gray-700">
                Ativar notificações por e-mail
              </label>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="pushNotifications"
                checked={settings.notificationSettings.pushNotifications}
                onChange={e =>
                  handleNestedChange(
                    'notificationSettings',
                    'pushNotifications',
                    '',
                    e.target.checked
                  )
                }
                className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="pushNotifications" className="text-sm font-medium text-gray-700">
                Ativar notificações push
              </label>
            </div>

            <div>
              <label
                htmlFor="reminderFrequency"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Frequência de lembretes
              </label>
              <select
                id="reminderFrequency"
                value={settings.notificationSettings.reminderFrequency}
                onChange={e =>
                  handleNestedChange(
                    'notificationSettings',
                    'reminderFrequency',
                    '',
                    e.target.value
                  )
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="daily">Diário</option>
                <option value="weekly">Semanal</option>
                <option value="monthly">Mensal</option>
                <option value="never">Nunca</option>
              </select>
            </div>
          </div>
        </div>

        {/* Configurações de API */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Configurações de API</h2>

          <div className="space-y-4">
            <div>
              <label
                htmlFor="openaiApiKey"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Chave da API OpenAI (oculta por segurança)
              </label>
              <input
                type="password"
                id="openaiApiKey"
                placeholder="●●●●●●●●●●●●●●●●●●●●"
                value={settings.apiSettings.openaiApiKey}
                onChange={e =>
                  handleNestedChange('apiSettings', 'openaiApiKey', '', e.target.value)
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label
                htmlFor="openaiModelVersion"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Versão do modelo OpenAI
              </label>
              <select
                id="openaiModelVersion"
                value={settings.apiSettings.openaiModelVersion}
                onChange={e =>
                  handleNestedChange('apiSettings', 'openaiModelVersion', '', e.target.value)
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="gpt-3.5-turbo">GPT-3.5-Turbo</option>
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-4-turbo">GPT-4-Turbo</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="maxTokensPerRequest"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Máximo de tokens por requisição
              </label>
              <input
                type="number"
                id="maxTokensPerRequest"
                value={settings.apiSettings.maxTokensPerRequest}
                onChange={e =>
                  handleNestedChange(
                    'apiSettings',
                    'maxTokensPerRequest',
                    '',
                    parseInt(e.target.value)
                  )
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Botões de Ação */}
        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={() => setSettings(systemSettings)}
            disabled={isSaving}
            className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isSaving}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center"
          >
            {isSaving ? (
              <>
                <svg
                  className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Salvando...
              </>
            ) : (
              'Salvar Configurações'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SystemSettingsPage;
