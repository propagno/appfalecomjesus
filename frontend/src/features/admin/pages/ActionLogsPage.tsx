import React, { useState, useEffect } from 'react';
import { useAdmin } from '../contexts/AdminContext';
import { AdminActionLog, TimeRange } from '../types';

const ActionLogsPage: React.FC = () => {
  const { actionLogs, isLoading, error, fetchActionLogs } = useAdmin();

  const [timeRange, setTimeRange] = useState<TimeRange>('last_7_days');
  const [filteredLogs, setFilteredLogs] = useState<AdminActionLog[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const logsPerPage = 20;

  useEffect(() => {
    fetchActionLogs(timeRange);
  }, [fetchActionLogs, timeRange]);

  useEffect(() => {
    if (actionLogs) {
      const filtered = actionLogs.filter(
        log =>
          log.action_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
          log.user_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
          log.details.toString().toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredLogs(filtered);
      setCurrentPage(1); // Reset to first page when filtering
    }
  }, [actionLogs, searchTerm]);

  // Pagination logic
  const indexOfLastLog = currentPage * logsPerPage;
  const indexOfFirstLog = indexOfLastLog - logsPerPage;
  const currentLogs = filteredLogs.slice(indexOfFirstLog, indexOfLastLog);
  const totalPages = Math.ceil(filteredLogs.length / logsPerPage);

  const paginate = (pageNumber: number) => setCurrentPage(pageNumber);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-100 border-red-400';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100 border-yellow-400';
      case 'info':
        return 'text-blue-600 bg-blue-100 border-blue-400';
      default:
        return 'text-gray-600 bg-gray-100 border-gray-400';
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
        <h3 className="font-bold">Erro ao carregar logs</h3>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Logs de Ações do Sistema</h1>
        <p className="text-gray-600">Monitoramento e auditoria de atividades no sistema.</p>
      </div>

      <div className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="w-full md:w-1/3">
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
          </select>
        </div>

        <div className="w-full md:w-2/3">
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
            Buscar logs
          </label>
          <input
            type="text"
            id="search"
            placeholder="Buscar por tipo de ação, usuário ou detalhes..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {filteredLogs.length === 0 ? (
        <div className="bg-white p-6 rounded-lg shadow text-center">
          <p className="text-gray-500">Nenhum log encontrado para os critérios selecionados.</p>
        </div>
      ) : (
        <>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Data/Hora
                    </th>
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
                      Ação
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Severidade
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Detalhes
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {currentLogs.map(log => (
                    <tr key={log.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(log.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {log.user_email || log.user_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {log.action_type}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 text-xs rounded-full border ${getSeverityColor(log.details?.severity || 'info')}`}
                        >
                          {log.details?.severity || 'info'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        <div className="max-w-xs truncate">
                          {typeof log.details === 'object'
                            ? JSON.stringify(log.details)
                            : log.details}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 mt-4 rounded-lg shadow">
              <div className="flex flex-1 justify-between sm:hidden">
                <button
                  onClick={() => paginate(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                    currentPage === 1
                      ? 'bg-gray-100 text-gray-400'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Anterior
                </button>
                <button
                  onClick={() => paginate(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className={`relative ml-3 inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                    currentPage === totalPages
                      ? 'bg-gray-100 text-gray-400'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Próximo
                </button>
              </div>
              <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-gray-700">
                    Mostrando <span className="font-medium">{indexOfFirstLog + 1}</span> a{' '}
                    <span className="font-medium">
                      {Math.min(indexOfLastLog, filteredLogs.length)}
                    </span>{' '}
                    de <span className="font-medium">{filteredLogs.length}</span> resultados
                  </p>
                </div>
                <div>
                  <nav
                    className="isolate inline-flex -space-x-px rounded-md shadow-sm"
                    aria-label="Pagination"
                  >
                    <button
                      onClick={() => paginate(Math.max(1, currentPage - 1))}
                      disabled={currentPage === 1}
                      className={`relative inline-flex items-center rounded-l-md px-2 py-2 border ${
                        currentPage === 1
                          ? 'bg-gray-100 text-gray-400'
                          : 'bg-white text-gray-500 hover:bg-gray-50'
                      }`}
                    >
                      <span className="sr-only">Anterior</span>
                      <svg
                        className="h-5 w-5"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        aria-hidden="true"
                      >
                        <path
                          fillRule="evenodd"
                          d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>

                    {Array.from({ length: totalPages }, (_, i) => i + 1).map(number => (
                      <button
                        key={number}
                        onClick={() => paginate(number)}
                        className={`relative inline-flex items-center px-4 py-2 border ${
                          currentPage === number
                            ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                            : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                        }`}
                      >
                        {number}
                      </button>
                    ))}

                    <button
                      onClick={() => paginate(Math.min(totalPages, currentPage + 1))}
                      disabled={currentPage === totalPages}
                      className={`relative inline-flex items-center rounded-r-md px-2 py-2 border ${
                        currentPage === totalPages
                          ? 'bg-gray-100 text-gray-400'
                          : 'bg-white text-gray-500 hover:bg-gray-50'
                      }`}
                    >
                      <span className="sr-only">Próximo</span>
                      <svg
                        className="h-5 w-5"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        aria-hidden="true"
                      >
                        <path
                          fillRule="evenodd"
                          d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {/* Informações de Ajuda */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-lg font-medium text-blue-800 mb-2">Informações sobre Logs de Ações</h3>
        <ul className="list-disc pl-5 text-sm text-blue-700 space-y-1">
          <li>Os logs são armazenados por até 90 dias para fins de auditoria.</li>
          <li>Logs com severidade "critical" requerem atenção imediata da equipe.</li>
          <li>É possível exportar os logs filtrados para análise posterior.</li>
          <li>Para detalhes completos de um log específico, clique na linha correspondente.</li>
        </ul>
      </div>
    </div>
  );
};

export default ActionLogsPage;
