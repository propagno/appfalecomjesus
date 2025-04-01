import React from 'react';
import { cn } from '../../../lib/utils';

interface NotificationBadgeProps {
  count: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const NotificationBadge: React.FC<NotificationBadgeProps> = ({
  count,
  max = 99,
  size = 'md',
  className,
}) => {
  // Se não houver notificações, não renderiza nada
  if (count <= 0) return null;

  // Define o texto a ser exibido
  const displayText = count > max ? `${max}+` : count.toString();

  // Define as classes com base no tamanho
  const sizeClasses = {
    sm: 'h-4 min-w-4 text-[10px]',
    md: 'h-5 min-w-5 text-xs',
    lg: 'h-6 min-w-6 text-sm',
  };

  return (
    <div
      className={cn(
        'flex items-center justify-center rounded-full bg-red-500 text-white font-medium px-1',
        sizeClasses[size],
        className
      )}
    >
      {displayText}
    </div>
  );
};

export default NotificationBadge; 