import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../../auth/hooks/useAuth';
import useStudy from '../hooks/useStudy';
import OnboardingForm from '../components/OnboardingForm';
import { OnboardingPreferences } from '../types';
import authService from '../../auth/api/authService';
import { toast } from 'react-hot-toast';
import { UserPreferences } from '../../auth/types';

/**
 * Página de onboarding para coletar preferências e criar plano personalizado
 */
const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { user, refetchUser } = useAuth();
  const { submitOnboarding, confirmPersonalizedPlan } = useStudy();

  // Usar useEffect para verificar a autenticação ao montar o componente
  useEffect(() => {
    // Se não houver usuário, redireciona para login
    if (!user) {
      navigate('/login');
    }
    // Se o usuário já completou o onboarding, redireciona para home
    else if (user.onboarding_completed === true) {
      console.log('Usuário já completou onboarding, redirecionando para home');
      navigate('/home');
    }
  }, [user, navigate]);

  const handleSubmit = async (formData: OnboardingPreferences) => {
    try {
      console.log('Iniciando processo de onboarding com dados:', formData);
      
      // Submete as preferências para gerar o plano personalizado
      await submitOnboarding(formData);
      
      // Converte para o formato esperado pelo authService
      const authPreferences: UserPreferences = {
        objectives: formData.objectives,
        bible_experience_level: formData.bible_experience_level as "iniciante" | "intermediario" | "avancado",
        content_preferences: formData.content_preferences,
        preferred_time: formData.preferred_time as "manha" | "tarde" | "noite",
        onboarding_completed: true
      };
      
      console.log('Salvando preferências do usuário com onboarding_completed=true');
      
      // Atualiza as preferências do usuário no serviço de autenticação
      await authService.savePreferences(authPreferences);
      
      // Após a sugestão de plano ser gerada, confirme e redirecione
      confirmPersonalizedPlan();
      
      // Crucial: atualizar os dados do usuário no contexto de autenticação
      await refetchUser();
      
      toast.success("Plano personalizado criado com sucesso!");
      
      // Atualiza o localStorage para refletir que o onboarding foi concluído
      const userData = localStorage.getItem('user');
      if (userData) {
        const parsedUser = JSON.parse(userData);
        parsedUser.onboarding_completed = true;
        localStorage.setItem('user', JSON.stringify(parsedUser));
      }
      
      console.log('Onboarding concluído com sucesso, redirecionando para /home');
      navigate('/home');
    } catch (error) {
      console.error('Erro ao criar plano personalizado:', error);
      toast.error("Ocorreu um erro ao criar seu plano. Tente novamente.");
    }
  };

  // Não queremos mostrar nada durante o redirecionamento
  if (!user) {
    return null;
  }

  return (
    <motion.div
      className="min-h-screen bg-white flex flex-col items-center justify-center p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-primary">
          Vamos personalizar sua experiência
        </h1>
        <OnboardingForm onSubmit={handleSubmit} />
      </div>
    </motion.div>
  );
};

export default OnboardingPage; 