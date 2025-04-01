import React, { useEffect, useState } from 'react';
import { X, Award, Share2, Twitter, Facebook, MessageCircle } from 'lucide-react';
import { useGamificationContext } from '../providers/GamificationProvider';
import { UserAchievement } from '../types';
import Confetti from 'react-confetti';
import useWindowSize from '../../../shared/hooks/useWindowSize';

/**
 * Modal que é exibido quando o usuário desbloqueia novas conquistas
 */
export const NewAchievementModal: React.FC = () => {
  const { state, dismissNewAchievement, shareAchievement } = useGamificationContext();
  const { newAchievements } = state;
  const [isVisible, setIsVisible] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const { width, height } = useWindowSize();

  // Efeito para exibir o modal quando houver novas conquistas
  useEffect(() => {
    if (newAchievements.length > 0) {
      setIsVisible(true);
      setCurrentIndex(0);
    }
  }, [newAchievements]);

  // Fechar o modal
  const handleClose = () => {
    setIsVisible(false);
    dismissNewAchievement(newAchievements[currentIndex].id);
  };

  // Avançar para a próxima conquista
  const handleNext = () => {
    if (currentIndex < newAchievements.length - 1) {
      setCurrentIndex(prev => prev + 1);
    } else {
      handleClose();
    }
  };

  // Compartilhar a conquista
  const handleShare = (platform: 'twitter' | 'facebook' | 'whatsapp') => {
    if (newAchievements[currentIndex]) {
      shareAchievement(newAchievements[currentIndex].id, platform);
    }
  };

  // Se não houver conquistas ou o modal estiver fechado, não renderizar
  if (!isVisible || !newAchievements.length) {
    return null;
  }

  const currentAchievement = newAchievements[currentIndex];

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Confetti animation */}
      <Confetti
        width={width}
        height={height}
        recycle={false}
        numberOfPieces={200}
        gravity={0.15}
      />
      
      {/* Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-60 backdrop-blur-sm" onClick={handleClose}></div>
      
      {/* Modal content */}
      <div className="bg-white rounded-xl shadow-xl overflow-hidden w-full max-w-md relative z-10 mx-4">
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
          <div className="flex items-center">
            <Award className="w-6 h-6 mr-2" />
            <h2 className="font-semibold text-lg">Nova Conquista!</h2>
          </div>
          <button 
            onClick={handleClose}
            className="text-white hover:bg-blue-700 rounded-full p-1"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        {/* Achievement details */}
        <div className="p-6 text-center">
          <div className="w-24 h-24 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Trophy icon_url={currentAchievement.achievement.icon_url} className="w-12 h-12 text-yellow-600" />
          </div>
          
          <h3 className="text-xl font-bold text-gray-800 mb-2">
            {currentAchievement.achievement.name}
          </h3>
          
          <p className="text-gray-600 mb-4">
            {currentAchievement.achievement.description}
          </p>
          
          {currentAchievement.achievement.category && (
            <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm mb-4">
              {currentAchievement.achievement.category}
            </span>
          )}
          
          <div className="mt-2 mb-4">
            <div className="text-sm text-gray-500">
              {newAchievements.length > 1 && (
                <span>{currentIndex + 1} de {newAchievements.length}</span>
              )}
            </div>
          </div>
          
          {/* Share buttons */}
          <div className="mt-6">
            <p className="text-sm text-gray-500 mb-2">Compartilhe sua conquista:</p>
            <div className="flex justify-center space-x-3">
              <button 
                onClick={() => handleShare('twitter')}
                className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600"
                title="Twitter"
              >
                <Twitter className="w-5 h-5" />
              </button>
              <button 
                onClick={() => handleShare('facebook')}
                className="p-2 bg-blue-700 text-white rounded-full hover:bg-blue-800"
                title="Facebook"
              >
                <Facebook className="w-5 h-5" />
              </button>
              <button 
                onClick={() => handleShare('whatsapp')}
                className="p-2 bg-green-500 text-white rounded-full hover:bg-green-600"
                title="WhatsApp"
              >
                <MessageCircle className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        
        {/* Footer actions */}
        <div className="bg-gray-50 p-4 border-t border-gray-200">
          {newAchievements.length > 1 && currentIndex < newAchievements.length - 1 ? (
            <button 
              onClick={handleNext}
              className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Próxima Conquista
            </button>
          ) : (
            <button 
              onClick={handleClose}
              className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Continuar
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// Componente auxiliar para renderizar o ícone
const Trophy: React.FC<{ icon_url: string; className?: string }> = ({ icon_url, className }) => {
  // Se tiver uma URL de ícone personalizado, usar ela
  if (icon_url) {
    return <img src={icon_url} className={className} alt="Ícone da conquista" />;
  }
  // Caso contrário, usar o ícone padrão
  return <Award className={className} />;
};

export default NewAchievementModal; 