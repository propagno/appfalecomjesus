import React from 'react';
import { Route, Routes } from 'react-router-dom';

// Páginas de gamificação
import { GamificationProfilePage } from '../pages/GamificationProfilePage';

/**
 * Rotas para a funcionalidade de gamificação
 */
export const GamificationRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="perfil" element={<GamificationProfilePage />} />
    </Routes>
  );
}; 