import React from 'react';
import { Link } from 'react-router-dom';

/**
 * Página 404 - Not Found
 */
const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-4">
      <h1 className="text-6xl font-bold text-blue-600 mb-4">404</h1>
      <h2 className="text-3xl font-semibold text-gray-800 mb-6">Página não encontrada</h2>
      <p className="text-gray-600 text-center max-w-md mb-8">
        A página que você está procurando não existe ou foi removida.
      </p>
      <div className="flex space-x-4">
        <Link
          to="/"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Voltar para Home
        </Link>
        <Link
          to="/bible"
          className="bg-white text-blue-600 border border-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-blue-50 transition-colors"
        >
          Explorar a Bíblia
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage; 