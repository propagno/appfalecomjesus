import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { AdminLayout } from '../layouts/AdminLayout';
import { DashboardPage } from '../pages/DashboardPage';
import UserManagementPage from '../pages/UserManagementPage';
import SystemSettingsPage from '../pages/SystemSettingsPage';
import ActionLogsPage from '../pages/ActionLogsPage';
import ReportsPage from '../pages/ReportsPage';
import { AdminProvider } from '../contexts/AdminContext';
import ProtectedRoute from '../../auth/components/ProtectedRoute';

const AdminRoutes: React.FC = () => {
  return (
    <Routes>
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <AdminProvider>
              <Routes>
                <Route element={<AdminLayout />}>
                  <Route index element={<DashboardPage />} />
                  <Route path="users" element={<UserManagementPage />} />
                  <Route path="settings" element={<SystemSettingsPage />} />
                  <Route path="logs" element={<ActionLogsPage />} />
                  <Route path="reports" element={<ReportsPage />} />
                </Route>
              </Routes>
            </AdminProvider>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

export default AdminRoutes; 