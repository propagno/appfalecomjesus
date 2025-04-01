import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import PlansPage from './pages/PlansPage';
import AdRewardsPage from './pages/AdRewardsPage';
import { MonetizationProvider } from './';

/**
 * Rotas para a funcionalidade de monetização
 */
const MonetizationRoutes: React.FC = () => {
  return (
    <MonetizationProvider>
      <Routes>
        <Route path="plans" element={<PlansPage />} />
        <Route path="rewards" element={<AdRewardsPage />} />
        <Route path="*" element={<Navigate to="plans" replace />} />
      </Routes>
    </MonetizationProvider>
  );
};

export default MonetizationRoutes; 