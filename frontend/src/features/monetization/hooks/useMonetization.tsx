import { useContext } from 'react';
import { MonetizationContext } from '../contexts/MonetizationContext';
import { PlanType, AdRewardType } from '../types';

export const useMonetization = () => {
  const context = useContext(MonetizationContext);

  if (!context) {
    throw new Error('useMonetization must be used within a MonetizationProvider');
  }

  // Retornar o contexto completo
  return context;
}; 