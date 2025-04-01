import React from 'react';

interface DashboardMetricsCardProps {
  title: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  icon?: React.ReactNode;
  isLoading?: boolean;
  onClick?: () => void;
}

export const DashboardMetricsCard: React.FC<DashboardMetricsCardProps> = ({
  title,
  value,
  change,
  trend = 'neutral',
  icon,
  isLoading = false,
  onClick
}) => {
  return (
    <div 
      className={`
        bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 
        ${onClick ? 'cursor-pointer hover:shadow-lg transition-shadow' : ''}
      `}
      onClick={onClick}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</h3>
        {icon && <span className="text-blue-600 dark:text-blue-400">{icon}</span>}
      </div>
      
      {isLoading ? (
        <div className="animate-pulse h-6 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
      ) : (
        <div className="flex items-end">
          <p className="text-2xl font-bold text-gray-900 dark:text-white mr-2">{value}</p>
          
          {change !== undefined && (
            <div className={`
              flex items-center text-sm
              ${trend === 'up' ? 'text-green-500' : ''}
              ${trend === 'down' ? 'text-red-500' : ''}
              ${trend === 'neutral' ? 'text-gray-500' : ''}
            `}>
              {trend === 'up' && <span className="mr-1">↑</span>}
              {trend === 'down' && <span className="mr-1">↓</span>}
              {change}%
            </div>
          )}
        </div>
      )}
    </div>
  );
}; 