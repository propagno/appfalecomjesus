// Re-export types from modules
import type { AdReward as GamificationAdReward } from './gamification';
// Removed MonetizationAdReward import since monetization.ts was deleted

// Export types directly to avoid ambiguity
export { 
  GamificationAdReward
  // Removed MonetizationAdReward
};

// Export all existing modules except those with conflicts
export * from './error';
export * from './bible';
export * from './chat';
export * from './study';

// Export all from gamification except AdReward
export type {
  UserPoints,
  Achievement,
  Certificate
} from './gamification';

// Export User as AuthUser from auth to avoid conflict
export type { User as AuthUser } from './auth';

// Removed monetization type exports since the file was deleted

// Explicitly export from API without User to avoid conflict
// Commenting out API exports to avoid ambiguity
// export * from './api'; 
