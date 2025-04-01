import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStudyContext } from '../contexts/StudyContext';
import PlanCard from '../components/PlanCard';

/**
 * Página que lista todos os planos de estudo disponíveis com filtros e paginação
 */
const StudyPlansPage: React.FC = () => {
  const navigate = useNavigate();
  const { 
    plans, 
    totalPlans, 
    userProgress, 
    isLoading, 
    filters, 
    handleFilterChange,
    handlePageChange,
    fetchPlans,
    startPlan
  } = useStudyContext();

  // Carregar planos ao montar o componente
  useEffect(() => {
    fetchPlans();
  }, [fetchPlans]);

  // Categorias disponíveis para filtro
  const categories = [
    { id: '', name: 'Todos' },
    { id: 'ansiedade', name: 'Ansiedade' },
    { id: 'familia', name: 'Família' },
    { id: 'paz', name: 'Paz Interior' },
    { id: 'proposito', name: 'Propósito' },
    { id: 'sabedoria', name: 'Sabedoria' }
  ];

  // Níveis de dificuldade disponíveis para filtro
  const difficulties = [
    { id: '', name: 'Todas' },
    { id: 'iniciante', name: 'Iniciante' },
    { id: 'intermediário', name: 'Intermediário' },
    { id: 'avançado', name: 'Avançado' }
  ];

  // Manipuladores de eventos
  const handleStartPlan = (planId: string) => {
    startPlan(planId);
  };

  const handleContinuePlan = (planId: string) => {
    navigate(`/estudo/planos/${planId}`);
  };

  const handleCreatePersonalizedPlan = () => {
    navigate('/estudo/onboarding');
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFilterChange({ search: e.target.value });
  };

  const handleCategoryChange = (categoryId: string) => {
    handleFilterChange({ category: categoryId });
  };

  const handleDifficultyChange = (difficultyId: string) => {
    handleFilterChange({ difficulty: difficultyId });
  };

  const handleClearFilters = () => {
    handleFilterChange({
      search: '',
      category: '',
      difficulty: '',
      page: 1
    });
  };

  // Auxiliar para encontrar o progresso do usuário para um plano
  const findUserProgress = (planId: string) => {
    return userProgress.find(progress => progress.study_plan_id === planId);
  };

  // Cálculo de páginas para paginação
  const totalPages = Math.ceil(totalPlans / (filters.per_page || 10));

  // Renderização do cabeçalho e filtros
  const renderHeader = () => (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Planos de Estudo</h1>
        <button
          onClick={handleCreatePersonalizedPlan}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Criar Plano Personalizado
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm p-4 border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Campo de busca */}
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Buscar
            </label>
            <input
              type="text"
              id="search"
              placeholder="Digite um tema ou título..."
              value={filters.search || ''}
              onChange={handleSearchChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          
          {/* Filtro de categoria */}
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Categoria
            </label>
            <select
              id="category"
              value={filters.category || ''}
              onChange={(e) => handleCategoryChange(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md bg-white"
            >
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* Filtro de dificuldade */}
          <div>
            <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-1">
              Nível
            </label>
            <select
              id="difficulty"
              value={filters.difficulty || ''}
              onChange={(e) => handleDifficultyChange(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md bg-white"
            >
              {difficulties.map(difficulty => (
                <option key={difficulty.id} value={difficulty.id}>
                  {difficulty.name}
                </option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Botão de limpar filtros */}
        {(filters.search || filters.category || filters.difficulty) && (
          <div className="mt-4 flex justify-end">
            <button
              onClick={handleClearFilters}
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Limpar filtros
            </button>
          </div>
        )}
      </div>
    </div>
  );

  // Renderização da lista de planos
  const renderPlans = () => {
    if (isLoading) {
      return (
        <div className="flex justify-center py-10">
          <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      );
    }
    
    if (plans.length === 0) {
      return (
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714a2.25 2.25 0 0 0 .659 1.591L18.75 14.5M4.5 10.157a24 24 0 0 0 6.75 1.453m12-6.75H6.75m0 0v10.5a2.25 2.25 0 0 0 2.25 2.25h8.5a2.25 2.25 0 0 0 2.25-2.25V4.5h-9.5z" />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900">Nenhum plano encontrado</h3>
          <p className="mt-1 text-sm text-gray-500">
            Tente ajustar os filtros ou crie um plano personalizado.
          </p>
          <div className="mt-6">
            <button
              onClick={handleCreatePersonalizedPlan}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
            >
              Criar Plano Personalizado
            </button>
          </div>
        </div>
      );
    }
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {plans.map(plan => (
          <PlanCard
            key={plan.id}
            plan={plan}
            userProgress={findUserProgress(plan.id)}
            onStartPlan={handleStartPlan}
            onContinue={handleContinuePlan}
          />
        ))}
      </div>
    );
  };

  // Renderização da paginação
  const renderPagination = () => {
    if (totalPages <= 1) return null;
    
    return (
      <div className="mt-8 flex justify-center">
        <nav className="flex items-center" aria-label="Paginação">
          <button
            onClick={() => handlePageChange(Math.max(1, (filters.page || 1) - 1))}
            disabled={(filters.page || 1) === 1}
            className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
          >
            Anterior
          </button>
          
          {[...Array(totalPages)].map((_, index) => (
            <button
              key={index}
              onClick={() => handlePageChange(index + 1)}
              className={`relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium ${
                (filters.page || 1) === index + 1
                  ? 'bg-blue-50 text-blue-600 z-10'
                  : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              {index + 1}
            </button>
          ))}
          
          <button
            onClick={() => handlePageChange(Math.min(totalPages, (filters.page || 1) + 1))}
            disabled={(filters.page || 1) === totalPages}
            className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400"
          >
            Próxima
          </button>
        </nav>
      </div>
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {renderHeader()}
      {renderPlans()}
      {renderPagination()}
    </div>
  );
};

export default StudyPlansPage; 