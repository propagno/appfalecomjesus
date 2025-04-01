import React, { useState } from 'react';
import { useAdmin } from '../contexts/AdminContext';
import { TimeRange, ReportData } from '../types';

const ReportsPage: React.FC = () => {
  const { generateReport, isLoading, error } = useAdmin();

  const [timeRange, setTimeRange] = useState<TimeRange>('last_30_days');
  const [reportType, setReportType] = useState<string>('user_activity');
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // Função para extrair uma mensagem de erro utilizável
  const getErrorMessage = (err: unknown): string => {
    if (typeof err === 'string') return err;
    if (err && typeof err === 'object') {
      if ('message' in err && typeof err.message === 'string') {
        return err.message;
      }
      if ('details' in err && err.details && typeof err.details === 'object' && 'detail' in err.details) {
        return String(err.details.detail);
      }
    }
    return 'Erro ao carregar dados do relatório';
  };

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    try {
      const data = await generateReport(reportType, timeRange);
      setReportData(data);
    } catch (err) {
      console.error('Erro ao gerar relatório:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportCSV = () => {
    if (!reportData) return;

    // Criar cabeçalhos baseados no tipo de relatório
    let headers: string[] = [];
    let rows: any[] = [];

    if (reportType === 'user_activity') {
      headers = ['Usuário', 'Ações', 'Logins', 'Tempo Médio', 'Última Atividade'];
      rows = reportData.data.map(item => [
        item.label,
        item.actions,
        item.logins,
        item.averageTime,
        item.lastActivity,
      ]);
    } else if (reportType === 'content_usage') {
      headers = ['Conteúdo', 'Visualizações', 'Tempo Médio', 'Conclusões'];
      rows = reportData.data.map(item => [
        item.label,
        item.views,
        item.averageTime,
        item.completions,
      ]);
    } else if (reportType === 'subscription') {
      headers = ['Plano', 'Assinantes', 'Novos', 'Cancelados', 'Receita'];
      rows = reportData.data.map(item => [
        item.label,
        item.subscribers,
        item.newSubscribers,
        item.canceled,
        item.revenue,
      ]);
    }

    // Converter para CSV
    const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');

    // Download do arquivo
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `relatorio-${reportType}-${timeRange}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
        <h3 className="font-bold">Erro ao carregar dados</h3>
        <p>{getErrorMessage(error)}</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Relatórios Gerenciais</h1>
        <p className="text-gray-600">Gere relatórios personalizados para análise de dados.</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label htmlFor="reportType" className="block text-sm font-medium text-gray-700 mb-1">
              Tipo de Relatório
            </label>
            <select
              id="reportType"
              value={reportType}
              onChange={e => setReportType(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="user_activity">Atividade dos Usuários</option>
              <option value="content_usage">Uso de Conteúdo</option>
              <option value="subscription">Assinaturas e Receita</option>
              <option value="chat_interactions">Interações com Chat IA</option>
              <option value="bible_usage">Uso da Bíblia</option>
            </select>
          </div>

          <div>
            <label htmlFor="timeRange" className="block text-sm font-medium text-gray-700 mb-1">
              Período
            </label>
            <select
              id="timeRange"
              value={timeRange}
              onChange={e => setTimeRange(e.target.value as TimeRange)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="today">Hoje</option>
              <option value="yesterday">Ontem</option>
              <option value="last_7_days">Últimos 7 dias</option>
              <option value="last_30_days">Últimos 30 dias</option>
              <option value="last_90_days">Últimos 90 dias</option>
              <option value="last_12_months">Últimos 12 meses</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleGenerateReport}
              disabled={isGenerating}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex justify-center items-center"
            >
              {isGenerating ? (
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
                  Gerando...
                </>
              ) : (
                'Gerar Relatório'
              )}
            </button>
          </div>
        </div>
      </div>

      {reportData && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="p-6 border-b border-gray-200 flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-800">
              {reportType === 'user_activity' && 'Relatório de Atividade dos Usuários'}
              {reportType === 'content_usage' && 'Relatório de Uso de Conteúdo'}
              {reportType === 'subscription' && 'Relatório de Assinaturas e Receita'}
              {reportType === 'chat_interactions' && 'Relatório de Interações com Chat IA'}
              {reportType === 'bible_usage' && 'Relatório de Uso da Bíblia'}
            </h2>
            <button
              onClick={handleExportCSV}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 flex items-center"
            >
              <svg
                className="w-4 h-4 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              Exportar CSV
            </button>
          </div>

          <div className="p-6">
            {/* Resumo do relatório */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
              {reportData.summary.map((item, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-500">{item.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{item.value}</p>
                  <div className="flex items-center mt-1">
                    <span
                      className={`text-sm ${item.change >= 0 ? 'text-green-600' : 'text-red-600'}`}
                    >
                      {item.change >= 0 ? '+' : ''}
                      {item.change}%
                    </span>
                    <span className="text-xs text-gray-500 ml-2">vs. período anterior</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Tabela de dados */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    {reportType === 'user_activity' && (
                      <>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Usuário
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Ações
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Logins
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Tempo Médio
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Última Atividade
                        </th>
                      </>
                    )}

                    {reportType === 'content_usage' && (
                      <>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Conteúdo
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Visualizações
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Tempo Médio
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Conclusões
                        </th>
                      </>
                    )}

                    {reportType === 'subscription' && (
                      <>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Plano
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Assinantes
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Novos
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Cancelados
                        </th>
                        <th
                          scope="col"
                          className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          Receita
                        </th>
                      </>
                    )}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {reportData.data.map((item, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      {reportType === 'user_activity' && (
                        <>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {item.label}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.actions}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.logins}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.averageTime}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.lastActivity}
                          </td>
                        </>
                      )}

                      {reportType === 'content_usage' && (
                        <>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {item.label}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.views}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.averageTime}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.completions}
                          </td>
                        </>
                      )}

                      {reportType === 'subscription' && (
                        <>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {item.label}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.subscribers}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.newSubscribers}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.canceled}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {item.revenue}
                          </td>
                        </>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {!reportData && !isGenerating && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum relatório gerado</h3>
          <p className="mt-1 text-sm text-gray-500">
            Selecione um tipo de relatório e período, e clique em "Gerar Relatório".
          </p>
        </div>
      )}

      {/* Informações de Ajuda */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-lg font-medium text-blue-800 mb-2">Sobre os Relatórios</h3>
        <ul className="list-disc pl-5 text-sm text-blue-700 space-y-1">
          <li>
            Os relatórios podem levar alguns segundos para serem gerados, dependendo do volume de
            dados.
          </li>
          <li>É possível exportar os relatórios em formato CSV para análise mais detalhada.</li>
          <li>
            Os relatórios comparativos consideram o período anterior ao selecionado para cálculo de
            variação percentual.
          </li>
          <li>Dados históricos estão disponíveis por até 12 meses.</li>
        </ul>
      </div>
    </div>
  );
};

export default ReportsPage;
