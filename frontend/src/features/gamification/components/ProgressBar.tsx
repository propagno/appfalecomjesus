import React from 'react';

interface ProgressBarProps {
  progress: number;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ progress, className = '' }) => {
  // Garantir que o progresso está entre 0 e 100
  const safeProgress = Math.max(0, Math.min(100, progress));
  
  return (
    <div className={`w-full bg-gray-200 rounded-full h-2.5 ${className}`}>
      <div 
        className="bg-blue-600 h-2.5 rounded-full transition-all duration-300 ease-in-out" 
        style={{ width: `${safeProgress}%` }}
      ></div>
    </div>
  );
};

export default ProgressBar; 