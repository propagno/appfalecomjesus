import { useState, useEffect } from 'react';

/**
 * Hook para obter e monitorar as dimensões da janela do navegador
 * @returns Objeto contendo a largura e altura atual da janela
 */
const useWindowSize = () => {
  // Estado para armazenar as dimensões
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
  });

  useEffect(() => {
    // Função para atualizar o estado com as novas dimensões
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    };

    // Adicionar event listener para redimensionamento
    window.addEventListener('resize', handleResize);
    
    // Certificar que as dimensões iniciais estão corretas
    handleResize();
    
    // Cleanup: remover event listener quando o componente for desmontado
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
};

export default useWindowSize; 