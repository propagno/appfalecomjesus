/**
 * Barrel file to export monetization feature components, hooks, services and pages
 */

// API e Serviços
export { default as monetizationService } from './api/monetizationService';

// Hooks
export { default as useMonetizationQuery } from './hooks/useMonetizationQuery';

// Providers
export { default as MonetizationProvider } from './providers/MonetizationProvider';

// Context
export { useMonetizationContext } from './contexts/MonetizationContext';

// Componentes
export { default as PlanCard } from './components/PlanCard';
export { default as AdRewardModal } from './components/AdRewardModal';
export { default as TransactionsHistory } from './components/TransactionsHistory';

// Páginas
export { default as PlansPage } from './pages/PlansPage';

// Rotas
export { default as MonetizationRoutes } from './routes';

// Tipos
export * from './types'; 