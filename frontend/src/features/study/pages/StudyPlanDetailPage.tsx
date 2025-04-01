import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useStudyContext } from '../contexts/StudyContext';
import { StudyPlan, StudySection, UserStudyProgress } from '../types';
import ReflectionForm from '../components/ReflectionForm';

/**
 * Página de visualização detalhada de um plano de estudo
 */
const StudyPlanDetailPage: React.FC = () => {
  const { planId } = useParams<{ planId: string }>();
  const navigate = useNavigate();
  const { 
    fetchPlanDetails, 
    startPlan, 
    updateProgress, 
    isLoading, 
    userProgress 
  } = useStudyContext();
  
  // Estados locais
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [sections, setSections] = useState<StudySection[]>([]);
  const [activeSectionId, setActiveSectionId] = useState<string | null>(null);
  const [progress, setProgress] = useState<UserStudyProgress | null>(null);
  
  // Buscar detalhes do plano quando a página carregar
  useEffect(() => {
    if (!planId) return;
    
    const loadPlanDetails = async () => {
      const planData = await fetchPlanDetails(planId);
      if (planData) {
        setPlan(planData);
        
        // Simular busca de seções
        // Em um cenário real, isso viria do backend
        const mockSections: StudySection[] = [
          {
            id: '1',
            study_plan_id: planId,
            title: 'Introdução ao Tema',
            position: 1,
            duration_minutes: 15
          },
          {
            id: '2',
            study_plan_id: planId,
            title: 'Estudo Bíblico Principal',
            position: 2,
            duration_minutes: 20
          },
          {
            id: '3',
            study_plan_id: planId,
            title: 'Aplicação Prática',
            position: 3,
            duration_minutes: 15
          },
          {
            id: '4',
            study_plan_id: planId,
            title: 'Reflexão e Oração',
            position: 4,
            duration_minutes: 10
          }
        ];
        
        setSections(mockSections);
        
        // Se não houver seção ativa, definir a primeira
        if (!activeSectionId && mockSections.length > 0) {
          setActiveSectionId(mockSections[0].id);
        }
      }
    };
    
    loadPlanDetails();
  }, [planId, fetchPlanDetails, activeSectionId]);
  
  // Buscar progresso do usuário para este plano
  useEffect(() => {
    if (!planId || !userProgress) return;
    
    const planProgress = userProgress.find(p => p.study_plan_id === planId);
    setProgress(planProgress || null);
    
    // Se já tem progresso, ativar a seção atual
    if (planProgress?.current_section_id) {
      setActiveSectionId(planProgress.current_section_id);
    }
  }, [planId, userProgress]);
  
  // Calcular se o usuário já iniciou este plano
  const hasStarted = !!progress;
  
  // Iniciar o plano se ainda não iniciado
  const handleStartPlan = async () => {
    if (!planId) return;
    
    await startPlan(planId);
    // O progresso será atualizado via userProgress no hook acima
  };
  
  // Selecionar uma seção específica
  const handleSelectSection = (sectionId: string) => {
    setActiveSectionId(sectionId);
  };
  
  // Marcar seção como concluída
  const handleCompleteSection = async () => {
    if (!planId || !activeSectionId) return;
    
    // Calcular nova porcentagem de conclusão
    const totalSections = sections.length;
    const currentPosition = sections.find(s => s.id === activeSectionId)?.position || 1;
    const nextPosition = Math.min(currentPosition + 1, totalSections);
    const nextSection = sections.find(s => s.position === nextPosition);
    const completionPercentage = (nextPosition / totalSections) * 100;
    
    // Atualizar progresso no backend
    await updateProgress(planId, activeSectionId, completionPercentage);
    
    // Se houver próxima seção, navegar para ela
    if (nextSection && nextSection.id !== activeSectionId) {
      setActiveSectionId(nextSection.id);
    }
  };
  
  // Salvar uma reflexão
  const handleSaveReflection = async (sectionId: string, reflectionText: string) => {
    console.log('Reflexão salva para seção', sectionId, ':', reflectionText);
    // Em um cenário real, aqui chamaríamos uma função do contexto
  };
  
  // Voltar para a tela de planos
  const handleBackToPlans = () => {
    navigate('/estudo/planos');
  };
  
  // Renderizar conteúdo da seção ativa
  const renderSectionContent = () => {
    if (!activeSectionId) return null;
    
    const section = sections.find(s => s.id === activeSectionId);
    if (!section) return null;
    
    // Conteúdo simulado para esta seção
    // Em um cenário real, isso viria do backend
    const content = [
      {
        type: 'text',
        content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies ultricies, nunc nisl aliquam nunc, vitae aliquam nunc.'
      },
      {
        type: 'verse',
        reference: 'João 3:16',
        content: 'Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.'
      },
      {
        type: 'text',
        content: 'Phasellus in magna eu massa ultricies pharetra. Fusce sit amet turpis eget magna pharetra ultrices. Cras ut ante id dui facilisis elementum.'
      }
    ];
    
    return (
      <div className="space-y-6">
        <h2 className="text-xl font-semibold text-gray-900">
          {section.title}
          <span className="text-sm font-normal text-gray-500 ml-2">
            ({section.duration_minutes} minutos)
          </span>
        </h2>
        
        {content.map((item, index) => (
          <div key={index} className="space-y-4">
            {item.type === 'verse' ? (
              <div className="p-4 bg-blue-50 border-l-4 border-blue-400 rounded">
                <p className="text-blue-800 italic">"{item.content}"</p>
                <p className="text-sm text-blue-600 mt-2 font-medium">{item.reference}</p>
              </div>
            ) : (
              <p className="text-gray-700">{item.content}</p>
            )}
          </div>
        ))}
        
        <div className="pt-6 mt-6 border-t border-gray-200">
          <ReflectionForm
            sectionId={section.id}
            sectionTitle={section.title}
            onSave={handleSaveReflection}
            isLoading={false}
          />
        </div>
      </div>
    );
  };
  
  // Renderização enquanto carrega
  if (isLoading || !plan) {
    return (
      <div className="container mx-auto px-4 py-10 flex justify-center">
        <svg className="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Cabeçalho */}
      <div className="mb-8">
        <button 
          onClick={handleBackToPlans}
          className="flex items-center text-blue-600 hover:text-blue-800 mb-2"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Voltar para planos
        </button>
        
        <h1 className="text-2xl font-bold text-gray-900 mb-1">{plan.title}</h1>
        
        <div className="flex items-center text-sm text-gray-500 mb-2">
          <span className="flex items-center mr-4">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
            </svg>
            {plan.duration_days} dias
          </span>
          
          <span className="mr-4 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
            </svg>
            {plan.difficulty}
          </span>
          
          <span className="px-2 py-0.5 rounded-full text-xs bg-blue-100 text-blue-800">
            {plan.category}
          </span>
        </div>
        
        <p className="text-gray-600 mb-4">{plan.description}</p>
        
        {!hasStarted && (
          <button
            onClick={handleStartPlan}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md"
          >
            Começar este plano
          </button>
        )}
        
        {hasStarted && progress && (
          <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
            <div 
              className="h-2.5 rounded-full bg-blue-600"
              style={{ width: `${progress.completion_percentage}%` }}
              aria-label={`${Math.round(progress.completion_percentage)}% concluído`}
            />
          </div>
        )}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Menu de seções */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <h2 className="font-medium text-gray-900 mb-4">Seções do Plano</h2>
            
            <div className="space-y-2">
              {sections.map((section) => {
                const isActive = section.id === activeSectionId;
                const isCompleted = progress?.completion_percentage &&
                  (section.position / sections.length) * 100 <= progress.completion_percentage;
                
                return (
                  <button
                    key={section.id}
                    onClick={() => handleSelectSection(section.id)}
                    disabled={!hasStarted}
                    className={`
                      flex items-center w-full p-3 rounded-md text-left transition-colors
                      ${!hasStarted 
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                        : isActive
                          ? 'bg-blue-100 text-blue-800'
                          : isCompleted
                            ? 'bg-green-50 text-green-800'
                            : 'bg-white hover:bg-gray-50 text-gray-700'}
                    `}
                  >
                    <div className="flex-shrink-0 mr-3">
                      {isCompleted ? (
                        <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <div className={`w-5 h-5 rounded-full flex items-center justify-center ${
                          isActive 
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-200 text-gray-500'
                        }`}>
                          {section.position}
                        </div>
                      )}
                    </div>
                    <div className="flex-1">
                      <span className="block font-medium">
                        {section.title}
                      </span>
                      <span className="block text-xs">
                        {section.duration_minutes} minutos
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
        
        {/* Conteúdo da seção */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            {!hasStarted ? (
              <div className="text-center py-10">
                <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <h3 className="mt-2 text-lg font-medium text-gray-900">Plano não iniciado</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Inicie o plano para acessar o conteúdo das seções.
                </p>
                <div className="mt-6">
                  <button
                    onClick={handleStartPlan}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none"
                  >
                    Começar agora
                  </button>
                </div>
              </div>
            ) : (
              <>
                {renderSectionContent()}
                
                <div className="mt-8 flex justify-between">
                  <button
                    onClick={handleBackToPlans}
                    className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                  >
                    Voltar para planos
                  </button>
                  
                  <button
                    onClick={handleCompleteSection}
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md"
                  >
                    Próxima seção
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudyPlanDetailPage; 