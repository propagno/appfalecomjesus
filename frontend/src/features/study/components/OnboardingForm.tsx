import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { OnboardingPreferences } from '../types';
import { useStudyContext } from '../contexts/StudyContext';

// Interface para os dados do formulário de onboarding
interface OnboardingFormData {
  objectives: string[];
  bible_experience_level: string;
  content_preferences: string[];
  preferred_time: string;
}

// Interface para as props do componente
interface OnboardingFormProps {
  onSubmit?: (preferences: OnboardingPreferences) => Promise<void>;
  isLoading?: boolean;
}

// Opções para os campos de seleção múltipla
const OBJECTIVES_OPTIONS = [
  { value: 'ansiedade', label: 'Lidar com ansiedade' },
  { value: 'paz', label: 'Encontrar paz interior' },
  { value: 'sabedoria', label: 'Crescer em sabedoria' },
  { value: 'familia', label: 'Melhorar relações familiares' },
  { value: 'fe', label: 'Fortalecer minha fé' },
  { value: 'proposito', label: 'Descobrir meu propósito' },
];

const EXPERIENCE_OPTIONS = [
  { id: 'iniciante', label: 'Iniciante (Primeiros passos na Bíblia)' },
  { id: 'intermediário', label: 'Intermediário (Conheço o básico)' },
  { id: 'avançado', label: 'Avançado (Estudo há muito tempo)' },
];

const CONTENT_OPTIONS = [
  { id: 'textos-curtos', label: 'Textos curtos' },
  { id: 'audio', label: 'Áudios explicativos' },
  { id: 'reflexao', label: 'Reflexões guiadas' },
  { id: 'perguntas', label: 'Perguntas para pensar' },
];

const TIME_OPTIONS = [
  { id: 'manhã', label: 'Manhã' },
  { id: 'tarde', label: 'Tarde' },
  { id: 'noite', label: 'Noite' },
  { id: 'flexível', label: 'Flexível' },
];

/**
 * Componente de formulário para onboarding e criação de plano personalizado
 */
const OnboardingForm: React.FC<OnboardingFormProps> = ({ onSubmit, isLoading }) => {
  const navigate = useNavigate();
  const { submitOnboarding } = useStudyContext();
  const formSubmitHandler = onSubmit || submitOnboarding;
  const loading = isLoading !== undefined ? isLoading : false;
  
  // Estado do formulário multi-etapas
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<OnboardingFormData>({
    objectives: [],
    bible_experience_level: '',
    content_preferences: [],
    preferred_time: '',
  });
  
  // Estado de validação
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  // Manipuladores de eventos
  const handleObjectivesChange = (objective: string) => {
    setFormData(prev => {
      const newObjectives = prev.objectives.includes(objective)
        ? prev.objectives.filter(o => o !== objective)
        : [...prev.objectives, objective];
      
      return { ...prev, objectives: newObjectives };
    });
  };
  
  const handleExperienceChange = (level: string) => {
    setFormData(prev => ({ ...prev, bible_experience_level: level }));
  };
  
  const handleContentPreferenceChange = (preference: string) => {
    setFormData(prev => {
      const newPreferences = prev.content_preferences.includes(preference)
        ? prev.content_preferences.filter(p => p !== preference)
        : [...prev.content_preferences, preference];
      
      return { ...prev, content_preferences: newPreferences };
    });
  };
  
  const handleTimePreferenceChange = (time: string) => {
    setFormData(prev => ({ ...prev, preferred_time: time }));
  };
  
  // Validação por etapa
  const validateStep = (currentStep: number): boolean => {
    const newErrors: Record<string, string> = {};
    
    if (currentStep === 1) {
      if (formData.objectives.length === 0) {
        newErrors.objectives = 'Selecione pelo menos um objetivo';
      }
    } else if (currentStep === 2) {
      if (!formData.bible_experience_level) {
        newErrors.bible_experience_level = 'Selecione seu nível de experiência';
      }
    } else if (currentStep === 3) {
      if (formData.content_preferences.length === 0) {
        newErrors.content_preferences = 'Selecione pelo menos uma preferência de conteúdo';
      }
      if (!formData.preferred_time) {
        newErrors.preferred_time = 'Selecione um horário preferencial';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  // Avançar para próxima etapa
  const handleNextStep = () => {
    const isValid = validateStep(step);
    
    if (isValid) {
      setStep(prev => prev + 1);
    }
  };
  
  // Voltar para etapa anterior
  const handlePrevStep = () => {
    setStep(prev => prev - 1);
  };
  
  // Enviar dados ao completar o formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const isValid = validateStep(3);
    if (!isValid) return;
    
    try {
      // Converte os dados do formulário para as preferências esperadas pelo backend
      const preferences: OnboardingPreferences = {
        objectives: formData.objectives,
        bible_experience_level: formData.bible_experience_level,
        content_preferences: formData.content_preferences,
        preferred_time: formData.preferred_time
      };
      
      // Enviar preferências para o backend usando a função fornecida nas props ou pelo contexto
      await formSubmitHandler(preferences);
      
      // Navegação acontece no componente pai, se necessário
    } catch (error) {
      console.error('Erro ao enviar preferências:', error);
    }
  };
  
  // Renderização condicional baseada na etapa atual
  const renderStepContent = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Quais são seus objetivos?
              </h2>
              <p className="text-gray-600 mb-6">
                Selecione os temas que você gostaria de abordar no seu estudo bíblico.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {OBJECTIVES_OPTIONS.map(option => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => handleObjectivesChange(option.value)}
                    className={`flex items-center px-4 py-3 rounded-lg text-left text-sm transition-colors ${
                      formData.objectives.includes(option.value)
                        ? 'bg-blue-100 border-blue-500 border text-blue-700'
                        : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {formData.objectives.includes(option.value) && (
                      <svg className="w-4 h-4 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                    {option.label}
                  </button>
                ))}
              </div>
              
              {errors.objectives && (
                <p className="mt-2 text-sm text-red-600">{errors.objectives}</p>
              )}
            </div>
          </div>
        );
        
      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Qual seu nível de conhecimento bíblico?
              </h2>
              <p className="text-gray-600 mb-6">
                Isso nos ajudará a adaptar o conteúdo ao seu nível de familiaridade com a Bíblia.
              </p>
              
              <div className="space-y-3">
                {EXPERIENCE_OPTIONS.map(option => (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => handleExperienceChange(option.id)}
                    className={`flex items-center w-full px-4 py-3 rounded-lg text-left text-sm transition-colors ${
                      formData.bible_experience_level === option.id
                        ? 'bg-blue-100 border-blue-500 border text-blue-700'
                        : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {formData.bible_experience_level === option.id && (
                      <svg className="w-4 h-4 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                    {option.label}
                  </button>
                ))}
              </div>
              
              {errors.bible_experience_level && (
                <p className="mt-2 text-sm text-red-600">{errors.bible_experience_level}</p>
              )}
            </div>
          </div>
        );
        
      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Como prefere estudar?
              </h2>
              <p className="text-gray-600 mb-3">
                Selecione os formatos que mais combinam com seu estilo de aprendizado.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
                {CONTENT_OPTIONS.map(option => (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => handleContentPreferenceChange(option.id)}
                    className={`flex items-center px-4 py-3 rounded-lg text-left text-sm transition-colors ${
                      formData.content_preferences.includes(option.id)
                        ? 'bg-blue-100 border-blue-500 border text-blue-700'
                        : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {formData.content_preferences.includes(option.id) && (
                      <svg className="w-4 h-4 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                    {option.label}
                  </button>
                ))}
              </div>
              
              {errors.content_preferences && (
                <p className="mt-2 text-sm text-red-600">{errors.content_preferences}</p>
              )}
            </div>
            
            <div>
              <h3 className="font-medium text-gray-800 mb-3">
                Qual o melhor horário para seu estudo diário?
              </h3>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {TIME_OPTIONS.map(option => (
                  <button
                    key={option.id}
                    type="button"
                    onClick={() => handleTimePreferenceChange(option.id)}
                    className={`px-4 py-3 rounded-lg text-center text-sm transition-colors ${
                      formData.preferred_time === option.id
                        ? 'bg-blue-100 border-blue-500 border text-blue-700'
                        : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
              
              {errors.preferred_time && (
                <p className="mt-2 text-sm text-red-600">{errors.preferred_time}</p>
              )}
            </div>
          </div>
        );
        
      default:
        return null;
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      {/* Barra de progresso */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          {[1, 2, 3].map(stepNumber => (
            <span
              key={stepNumber}
              className={`text-xs font-medium ${
                stepNumber <= step ? 'text-blue-600' : 'text-gray-400'
              }`}
            >
              Etapa {stepNumber}
            </span>
          ))}
        </div>
        <div className="h-2 bg-gray-200 rounded-full">
          <div
            className="h-2 bg-blue-600 rounded-full transition-all duration-300"
            style={{ width: `${((step - 1) / 2) * 100}%` }}
          ></div>
        </div>
      </div>
      
      {/* Conteúdo do passo atual */}
      <form onSubmit={handleSubmit}>
        {renderStepContent()}
        
        {/* Botões de navegação */}
        <div className="flex justify-between mt-8">
          <button
            type="button"
            onClick={handlePrevStep}
            disabled={step === 1 || loading}
            className={`px-4 py-2 rounded-md text-sm font-medium ${
              step === 1
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            Voltar
          </button>
          
          {step < 3 ? (
            <button
              type="button"
              onClick={handleNextStep}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium transition-colors"
            >
              Continuar
            </button>
          ) : (
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium transition-colors flex items-center"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Criando plano...
                </>
              ) : (
                'Criar Plano Personalizado'
              )}
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default OnboardingForm; 