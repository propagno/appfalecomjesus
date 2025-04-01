/**
 * Formata uma data ISO ou objeto Date para o formato brasileiro (dd/mm/yyyy)
 * @param date Data em formato ISO string ou objeto Date
 * @returns Data formatada (dd/mm/yyyy)
 */
export const formatDate = (date: string | Date): string => {
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }).format(dateObj);
  } catch (error) {
    console.error('Erro ao formatar data:', error);
    return 'Data inválida';
  }
};

/**
 * Formata uma data ISO ou objeto Date com horário no formato brasileiro
 * @param date Data em formato ISO string ou objeto Date
 * @returns Data e hora formatada (dd/mm/yyyy HH:MM)
 */
export const formatDateTime = (date: string | Date): string => {
  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(dateObj);
  } catch (error) {
    console.error('Erro ao formatar data e hora:', error);
    return 'Data inválida';
  }
}; 