import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthContext } from '../features/auth/contexts/AuthContext';

/**
 * Tipos válidos para o nível de experiência com a Bíblia
 */
type BibleExperienceLevel = "iniciante" | "intermediario" | "avancado";

/**
 * Tipos válidos para o horário preferido
 */
type PreferredTime = "manha" | "tarde" | "noite";

/**
 * Página de onboarding para coletar preferências do usuário
 */
const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { savePreferences, isSavingPreferences } = useAuthContext();
  
  const [step, setStep] = useState(1);
  const [preferences, setPreferences] = useState({
    objectives: [] as string[],
    bible_experience_level: 'iniciante' as BibleExperienceLevel,
    content_preferences: [] as string[],
    preferred_time: 'manha' as PreferredTime,
    onboarding_completed: true
  });

  const handleObjectiveSelect = (objective: string) => {
    setPreferences(prev => {
      const objectives = prev.objectives.includes(objective)
        ? prev.objectives.filter(o => o !== objective)
        : [...prev.objectives, objective];
      return { ...prev, objectives };
    });
  };

  const handleExperienceSelect = (level: BibleExperienceLevel) => {
    setPreferences(prev => ({ ...prev, bible_experience_level: level }));
  };

  const handleContentPreferenceSelect = (preference: string) => {
    setPreferences(prev => {
      const content_preferences = prev.content_preferences.includes(preference)
        ? prev.content_preferences.filter(p => p !== preference)
        : [...prev.content_preferences, preference];
      return { ...prev, content_preferences };
    });
  };

  const handleTimeSelect = (time: PreferredTime) => {
    setPreferences(prev => ({ ...prev, preferred_time: time }));
  };

  const nextStep = () => {
    setStep(prev => prev + 1);
  };

  const prevStep = () => {
    setStep(prev => prev - 1);
  };

  const handleSubmit = async () => {
    const success = await savePreferences(preferences);
    if (success) {
      navigate('/home');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Personalize sua jornada</h1>
      
      {/* Progresso */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          <span className={`font-semibold ${step >= 1 ? 'text-blue-600' : 'text-gray-400'}`}>Objetivos</span>
          <span className={`font-semibold ${step >= 2 ? 'text-blue-600' : 'text-gray-400'}`}>Experiência</span>
          <span className={`font-semibold ${step >= 3 ? 'text-blue-600' : 'text-gray-400'}`}>Preferências</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${(step / 3) * 100}%` }}></div>
        </div>
      </div>
      
      {/* Step 1: Objetivos */}
      {step === 1 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Quais são seus objetivos espirituais?</h2>
          <p className="text-gray-600 mb-6">Selecione os temas que deseja explorar:</p>
          
          <div className="grid grid-cols-2 gap-4 mb-6">
            {['Paz', 'Família', 'Ansiedade', 'Sabedoria', 'Perdão', 'Fé', 'Propósito', 'Gratidão'].map(objective => (
              <button
                key={objective}
                className={`p-4 rounded-lg ${
                  preferences.objectives.includes(objective)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
                onClick={() => handleObjectiveSelect(objective)}
              >
                {objective}
              </button>
            ))}
          </div>
          
          <div className="flex justify-end">
            <button
              className="bg-blue-600 text-white px-6 py-2 rounded-lg"
              onClick={nextStep}
              disabled={preferences.objectives.length === 0}
            >
              Próximo
            </button>
          </div>
        </div>
      )}
      
      {/* Step 2: Experiência */}
      {step === 2 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Qual é seu nível de conhecimento bíblico?</h2>
          <p className="text-gray-600 mb-6">Isso nos ajudará a personalizar o conteúdo para você:</p>
          
          <div className="grid grid-cols-1 gap-4 mb-6">
            {['Iniciante', 'Intermediário', 'Avançado'].map(level => (
              <button
                key={level}
                className={`p-4 rounded-lg ${
                  preferences.bible_experience_level === level
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
                onClick={() => handleExperienceSelect(level as BibleExperienceLevel)}
              >
                {level}
              </button>
            ))}
          </div>
          
          <div className="flex justify-between">
            <button
              className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg"
              onClick={prevStep}
            >
              Voltar
            </button>
            <button
              className="bg-blue-600 text-white px-6 py-2 rounded-lg"
              onClick={nextStep}
              disabled={!preferences.bible_experience_level}
            >
              Próximo
            </button>
          </div>
        </div>
      )}
      
      {/* Step 3: Preferências */}
      {step === 3 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Como você prefere consumir o conteúdo?</h2>
          <p className="text-gray-600 mb-6">Selecione seus formatos preferidos:</p>
          
          <div className="grid grid-cols-1 gap-4 mb-6">
            {['Textos curtos', 'Áudios explicativos', 'Vídeos', 'Reflexões interativas'].map(contentType => (
              <button
                key={contentType}
                className={`p-4 rounded-lg ${
                  preferences.content_preferences.includes(contentType)
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
                onClick={() => handleContentPreferenceSelect(contentType)}
              >
                {contentType}
              </button>
            ))}
          </div>
          
          <h2 className="text-xl font-semibold mb-4">Qual é o melhor horário para você estudar?</h2>
          <div className="grid grid-cols-3 gap-4 mb-6">
            {['Manhã', 'Tarde', 'Noite'].map(time => (
              <button
                key={time}
                className={`p-4 rounded-lg ${
                  preferences.preferred_time === time
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 hover:bg-gray-200'
                }`}
                onClick={() => handleTimeSelect(time as PreferredTime)}
              >
                {time}
              </button>
            ))}
          </div>
          
          <div className="flex justify-between">
            <button
              className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg"
              onClick={prevStep}
            >
              Voltar
            </button>
            <button
              className="bg-blue-600 text-white px-6 py-2 rounded-lg"
              onClick={handleSubmit}
              disabled={isSavingPreferences || preferences.content_preferences.length === 0 || !preferences.preferred_time}
            >
              {isSavingPreferences ? 'Salvando...' : 'Concluir'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default OnboardingPage; 