// Exportação dos tipos
export * from './types';

// Exportação do serviço API
export { default as adminService } from './api/adminService';

// Exportação dos hooks
export { default as useAdminQuery } from './hooks/useAdminQuery';
export { useAdmin } from './providers/AdminProvider';

// Exportação do Provider
export { default as AdminProvider } from './providers/AdminProvider';

// Exportação dos componentes
export { default as DashboardMetrics } from './components/DashboardMetrics';
export { default as UsersList } from './components/UsersList';

// Exportação das páginas
export { default as AdminDashboardPage } from './pages/AdminDashboardPage'; 