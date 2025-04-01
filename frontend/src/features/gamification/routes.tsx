import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { GamificationProfilePage } from './pages/GamificationProfilePage';
import ProtectedRoute from '../../features/auth/components/ProtectedRoute';

const GamificationRoutes: React.FC = () => (
  <Routes>
    <Route 
      path="profile" 
      element={
        <ProtectedRoute>
          <GamificationProfilePage />
        </ProtectedRoute>
      } 
    />
  </Routes>
);

export default GamificationRoutes; 