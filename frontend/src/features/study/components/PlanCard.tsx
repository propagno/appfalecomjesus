import React from 'react';
import { Link } from 'react-router-dom';
import { StudyPlan, UserStudyProgress } from '../types';

interface PlanCardProps {
  plan: StudyPlan;
  userProgress?: UserStudyProgress;
  onStartPlan: (planId: string) => void;
  onContinue: (planId: string) => void;
  className?: string;
}

/**
 * Componente de card para exibir um plano de estudo
 */
const PlanCard: React.FC<PlanCardProps> = ({
  plan,
  userProgress,
  onStartPlan,
  onContinue,
  className = ''
}) => {
  const hasStarted = !!userProgress;
  const progress = userProgress?.completion_percentage || 0;
  const isCompleted = progress === 100;
  
  // Calcula o rótulo do botão principal com base no estado do progresso
  const getButtonLabel = () => {
    if (isCompleted) return 'Ver Certificado';
    if (hasStarted) return 'Continuar';
    return 'Começar Agora';
  };
  
  // Manipulador para o botão principal
  const handleMainButtonClick = () => {
    if (hasStarted) {
      onContinue(plan.id);
    } else {
      onStartPlan(plan.id);
    }
  };
  
  // Formata a duração do plano para exibição
  const formatDuration = (days: number) => {
    if (days === 1) return '1 dia';
    return `${days} dias`;
  };
  
  // Determinar estilo do badge de dificuldade
  const getDifficultyBadgeColor = (difficulty?: string) => {
    switch (difficulty) {
      case 'iniciante':
        return 'bg-green-100 text-green-800';
      case 'intermediário':
        return 'bg-yellow-100 text-yellow-800';
      case 'avançado':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden flex flex-col ${className}`}>
      {/* Imagem do plano */}
      <div className="relative h-48 bg-gray-200">
        {plan.image_url ? (
          <img 
            src={plan.image_url} 
            alt={plan.title} 
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-blue-50">
            <svg className="w-16 h-16 text-blue-300" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
            </svg>
          </div>
        )}
        
        {/* Badges */}
        <div className="absolute top-2 right-2 flex flex-col gap-1">
          {plan.difficulty && (
            <span className={`text-xs px-2 py-1 rounded-full ${getDifficultyBadgeColor(plan.difficulty)}`}>
              {plan.difficulty}
            </span>
          )}
          
          {isCompleted && (
            <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
              Concluído
            </span>
          )}
        </div>
        
        {/* Categoria */}
        {plan.category && (
          <span className="absolute bottom-2 left-2 text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
            {plan.category}
          </span>
        )}
        
        {/* Progresso (se iniciado) */}
        {hasStarted && !isCompleted && (
          <div className="absolute bottom-0 left-0 right-0 h-1.5 bg-gray-200">
            <div 
              className="h-full bg-blue-500" 
              style={{ width: `${progress}%` }}
              aria-label={`${Math.round(progress)}% concluído`}
            />
          </div>
        )}
      </div>
      
      {/* Conteúdo do card */}
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-lg font-semibold text-gray-900 mb-1">{plan.title}</h3>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
          </svg>
          <span>{formatDuration(plan.duration_days)}</span>
        </div>
        
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
          {plan.description}
        </p>
        
        {/* Barra de progresso (somente se o usuário já começou o plano) */}
        {hasStarted && (
          <div className="mb-4">
            <div className="flex justify-between text-xs text-gray-600 mb-1">
              <span>Progresso</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className={`h-2.5 rounded-full ${isCompleted ? 'bg-green-600' : 'bg-blue-600'}`}
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}
        
        <div className="mt-auto flex items-center justify-between">
          {!hasStarted ? (
            /* Botão para iniciar o plano */
            <button
              onClick={handleMainButtonClick}
              className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium transition-colors"
            >
              {getButtonLabel()}
            </button>
          ) : isCompleted ? (
            /* Link para rever o plano concluído */
            <Link
              to={`/estudo/planos/${plan.id}`}
              className="w-full text-center py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-md text-sm font-medium transition-colors"
            >
              {getButtonLabel()}
            </Link>
          ) : (
            /* Botão para continuar o plano */
            <button
              onClick={handleMainButtonClick}
              className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium transition-colors"
            >
              {getButtonLabel()}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PlanCard; 