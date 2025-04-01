/**
 * Exportações centralizadas para o módulo de Bíblia
 */

// Providers
export { default as BibleProvider, useBibleContext } from './providers/BibleProvider';

// Hooks
export { default as useBibleQuery, BibleQueryKeys } from './hooks/useBibleQuery';

// API Services
export { default as bibleService } from './api/bibleService';

// Componentes
export { default as BiblePage } from './pages/BiblePage';

// Tipos
export * from './types'; 