import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import PlansPage from './PlansPage';
import MonetizationPage from './MonetizationPage';
import AdRewardsPage from './AdRewardsPage';

/**
 * Router para a área de monetização
 */
const MonetizationRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<MonetizationPage />} />
      <Route path="/plans" element={<PlansPage />} />
      <Route path="/rewards" element={<AdRewardsPage />} />
      <Route path="*" element={<Navigate to="/monetization" />} />
    </Routes>
  );
};

export default MonetizationRouter; 