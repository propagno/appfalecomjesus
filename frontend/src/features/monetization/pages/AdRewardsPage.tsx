import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useMonetization } from '../hooks/useMonetization';
import AdRewardCard from '../components/AdRewardCard';
import { RewardType } from '../types';

const AdRewardsPage: React.FC = () => {
  const { isPremium } = useMonetization();
  const navigate = useNavigate();
  
  // Redirecionar usuários premium que não precisam de recompensas
  React.useEffect(() => {
    if (isPremium) {
      navigate('/monetization');
    }
  }, [isPremium, navigate]);
  
  if (isPremium) {
    return null; // Evitar flash antes do redirecionamento
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-blue-700 mb-2">Recompensas por Anúncios</h1>
          <p className="text-gray-600">
            Assista anúncios para desbloquear benefícios adicionais e continuar sua jornada espiritual.
          </p>
        </header>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Como Funciona</h2>
          <p className="mb-4">
            Usuários do plano gratuito podem assistir anúncios para ganhar benefícios temporários:
          </p>
          <ul className="list-disc pl-5 mb-4 space-y-2 text-gray-700">
            <li>Ganhe mensagens adicionais no chat com IA para apoio espiritual</li>
            <li>Desbloqueie acesso a estudos por dias extras</li>
            <li>Todas as recompensas são válidas por 24 horas</li>
          </ul>
        </div>
        
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Recompensas Disponíveis</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <AdRewardCard
            rewardType={RewardType.CHAT_MESSAGES}
            title="Mais mensagens no Chat IA"
            description="Assista um anúncio para ganhar 5 mensagens adicionais no chat IA. Use-as quando precisar de mais apoio espiritual."
            buttonText="Assistir anúncio"
          />
          
          <AdRewardCard
            rewardType={RewardType.STUDY_ACCESS}
            title="Mais dias de estudo"
            description="Assista um anúncio para ganhar 1 dia adicional de estudo. Continue avançando em sua jornada espiritual."
            buttonText="Assistir anúncio"
          />
        </div>
        
        <div className="mt-8 p-4 bg-blue-50 rounded-md text-center">
          <p className="text-gray-700 mb-3">
            Quer acesso ilimitado a todos os recursos sem anúncios?
          </p>
          <a 
            href="/monetization" 
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
          >
            Conheça nossos planos
          </a>
        </div>
      </div>
    </div>
  );
};

export default AdRewardsPage; 