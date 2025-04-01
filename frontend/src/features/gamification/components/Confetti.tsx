import React, { useEffect, useState } from 'react';
import ReactConfetti from 'react-confetti';

interface ConfettiProps {
  duration?: number; // Duração em milissegundos
  recycle?: boolean; // Se os confetes devem ser reciclados ou terminarem após uma volta
  colors?: string[]; // Cores dos confetes
  numberOfPieces?: number; // Quantidade de confetes
}

const Confetti: React.FC<ConfettiProps> = ({
  duration = 3000,
  recycle = false,
  colors = ['#FFD700', '#FFA500', '#4169E1', '#32CD32', '#9370DB', '#FF6347'],
  numberOfPieces = 200,
}) => {
  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 });
  const [visible, setVisible] = useState(true);

  // Calcula o tamanho da janela
  useEffect(() => {
    const updateWindowSize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Executar imediatamente
    updateWindowSize();
    
    // Adicionar listener para redimensionamento
    window.addEventListener('resize', updateWindowSize);
    
    // Remover após o tempo especificado
    if (!recycle && duration > 0) {
      const timer = setTimeout(() => {
        setVisible(false);
      }, duration);
      
      return () => {
        clearTimeout(timer);
        window.removeEventListener('resize', updateWindowSize);
      };
    }
    
    return () => window.removeEventListener('resize', updateWindowSize);
  }, [duration, recycle]);

  if (!visible) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      <ReactConfetti
        width={windowSize.width}
        height={windowSize.height}
        recycle={recycle}
        numberOfPieces={numberOfPieces}
        colors={colors}
      />
    </div>
  );
};

export default Confetti; 