import React from 'react';
import { useAuthContext } from '../features/auth/contexts/AuthContext';

/**
 * Página inicial que exibe o resumo da jornada espiritual do usuário
 */
const HomePage: React.FC = () => {
  const { user } = useAuthContext();

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Bem-vindo, {user?.name}</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Card de Plano Atual */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Seu Plano Atual</h2>
          <p className="text-gray-600 mb-4">Continue sua jornada espiritual</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Continuar Estudando
          </button>
        </div>
        
        {/* Card da Bíblia */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Bíblia</h2>
          <p className="text-gray-600 mb-4">Explore a palavra de Deus</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Abrir Bíblia
          </button>
        </div>
        
        {/* Card do Chat */}
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Chat com IA</h2>
          <p className="text-gray-600 mb-4">Converse sobre temas espirituais</p>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Iniciar Conversa
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 