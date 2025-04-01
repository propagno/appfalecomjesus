import React from 'react';
import { Card } from '../../../components/ui/card';
import { PointTransaction } from '../types';
import { snakeCaseToTitleCase } from '../../../lib/utils';

// Função local para formatação de data e hora
const formatDateTime = (date: Date | string): string => {
  if (!date) return '';
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('pt-BR', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export interface PointTransactionListProps {
  transactions: PointTransaction[];
  isLoading?: boolean;
  limit?: number;
  className?: string;
  showViewMore?: boolean;
  onViewMore?: () => void;
}

const PointTransactionList: React.FC<PointTransactionListProps> = ({
  transactions,
  isLoading = false,
  limit,
  className = '',
  showViewMore = false,
  onViewMore,
}) => {
  // Filtrar por limite, se fornecido
  const displayTransactions = limit 
    ? transactions.slice(0, limit) 
    : transactions;
  
  if (isLoading) {
    return (
      <Card className="p-4 animate-pulse">
        {[1, 2, 3].map(i => (
          <div key={i} className="flex items-center py-3 border-b border-gray-100 last:border-0">
            <div className="w-10 h-10 rounded-full bg-gray-200"></div>
            <div className="ml-3 flex-grow">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2"></div>
            </div>
            <div className="h-5 bg-gray-200 rounded w-16"></div>
          </div>
        ))}
      </Card>
    );
  }
  
  if (displayTransactions.length === 0) {
    return (
      <Card className="p-6 text-center">
        <p className="text-gray-600">
          Ainda não há atividades registradas. Continue interagindo com o aplicativo!
        </p>
      </Card>
    );
  }

  // Helper para obter o ícone baseado no tipo de ação
  const getActionIcon = (action: string) => {
    switch (action) {
      case 'daily_login':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        );
      case 'study_completed':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        );
      case 'study_started':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        );
      case 'achievement_unlocked':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        );
      default:
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  return (
    <Card className={`p-0 overflow-hidden ${className}`}>
      {displayTransactions.map((transaction) => (
        <div 
          key={transaction.id} 
          className="flex items-center p-4 border-b border-gray-100 last:border-0 hover:bg-gray-50"
        >
          <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center mr-3">
            {getActionIcon(transaction.action)}
          </div>
          <div className="flex-grow">
            <p className="font-medium">{transaction.description}</p>
            <p className="text-xs text-gray-500">{formatDateTime(transaction.created_at)}</p>
          </div>
          <div className={`font-semibold ${transaction.amount >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {transaction.amount >= 0 ? '+' : ''}{transaction.amount}
          </div>
        </div>
      ))}
      
      {/* Botão "Ver mais" */}
      {showViewMore && transactions.length > (limit || 0) && (
        <div className="text-center mt-4">
          <button 
            onClick={onViewMore}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Ver mais atividades
          </button>
        </div>
      )}
    </Card>
  );
};

export default PointTransactionList; 