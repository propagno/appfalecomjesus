import React from 'react';
import { useMonetizationContext } from '../contexts/MonetizationContext';
import { useMonetizationQuery } from '../hooks/useMonetizationQuery';
import { PaymentTransaction } from '../types';
import { Button } from '../../../shared/components/ui/Button';

/**
 * Componente que exibe o histórico de transações do usuário
 */
const TransactionsHistory: React.FC = () => {
  const { useTransactionsHistoryQuery } = useMonetizationQuery();
  const { data: transactions, isLoading, error } = useTransactionsHistoryQuery();
  
  // Formatar data
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };
  
  // Formatar valor
  const formatAmount = (amount: number, currency: string) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: currency || 'BRL',
    }).format(amount);
  };
  
  // Obter cor do status
  const getStatusColor = (status: PaymentTransaction['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'refunded':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  // Traduzir status
  const translateStatus = (status: PaymentTransaction['status']) => {
    switch (status) {
      case 'completed':
        return 'Concluído';
      case 'pending':
        return 'Pendente';
      case 'failed':
        return 'Falhou';
      case 'refunded':
        return 'Reembolsado';
      default:
        return status;
    }
  };
  
  if (isLoading) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-6">Histórico de Transações</h2>
        <div className="flex justify-center py-10">
          <div className="animate-spin h-8 w-8 border-4 border-indigo-500 rounded-full border-t-transparent"></div>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-6">Histórico de Transações</h2>
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded">
          <p>Erro ao carregar transações. Por favor, tente novamente mais tarde.</p>
          <Button 
            variant="outline" 
            className="mt-2"
            onClick={() => window.location.reload()}
          >
            Tentar Novamente
          </Button>
        </div>
      </div>
    );
  }
  
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-6">Histórico de Transações</h2>
      
      {transactions && transactions.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrição
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(transaction.transaction_date)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {transaction.description}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                    {formatAmount(transaction.amount, transaction.currency)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(transaction.status)}`}>
                      {translateStatus(transaction.status)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-10 text-gray-500">
          <p>Nenhuma transação encontrada.</p>
        </div>
      )}
    </div>
  );
};

export default TransactionsHistory; 