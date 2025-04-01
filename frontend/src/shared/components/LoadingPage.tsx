import React from 'react';

/**
 * Loading page component displayed during suspense or page transitions
 */
const LoadingPage = () => {
  return (
    <div className="flex items-center justify-center w-full h-screen bg-slate-50">
      <div className="flex flex-col items-center">
        <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-4 text-lg font-medium text-gray-700">Carregando...</p>
      </div>
    </div>
  );
};

export default LoadingPage; 