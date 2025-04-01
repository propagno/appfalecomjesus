import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../../auth/hooks/useAuth';
import useStudy from '../hooks/useStudy';
import OnboardingForm from '../components/OnboardingForm';
import { OnboardingPreferences } from '../types';

/**
 * Página de onboarding para coletar preferências e criar plano personalizado
 */
const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { submitOnboarding, confirmPersonalizedPlan } = useStudy();

  const handleSubmit = async (formData: OnboardingPreferences) => {
    try {
      await submitOnboarding(formData);
      // Após a sugestão de plano ser gerada, confirme e redirecione
      confirmPersonalizedPlan();
      navigate('/home');
    } catch (error) {
      console.error('Erro ao criar plano personalizado:', error);
    }
  };

  // Se não houver usuário, redireciona para login
  if (!user) {
    navigate('/login');
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