/**
 * Exportações centralizadas do módulo de gamificação
 * Implementação para o item 10.6 - Integração com MS-Gamification
 */

// Providers e Context
export { default as GamificationProvider, useGamificationContext } from './providers/GamificationProvider';

// Hooks
export { default as useGamificationQuery, GamificationQueryKeys } from './hooks/useGamificationQuery';

// API Services
export { default as gamificationService } from './api/gamificationService';

// Pages
export { default as GamificationPage } from './pages/GamificationPage';

// Types
export * from './types'; 