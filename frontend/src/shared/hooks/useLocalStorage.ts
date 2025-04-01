import { useState, useEffect } from 'react';

/**
 * Hook para gerenciar estado em localStorage, com suporte a
 * tipagem e valor padrão para casos onde a chave não existe
 * 
 * @param key Chave para armazenamento no localStorage
 * @param initialValue Valor padrão caso a chave não exista
 * @returns [valor, função para atualizar valor]
 */
export function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((val: T) => T)) => void] {
  // Função para obter valor inicial do localStorage
  const readValue = (): T => {
    // Verificar se estamos no cliente
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      // Obter do localStorage pela chave
      const item = window.localStorage.getItem(key);
      // Analisar o valor armazenado ou retornar initialValue
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch (error) {
      console.warn(`Erro ao ler localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  // Estado para armazenar nosso valor
  const [storedValue, setStoredValue] = useState<T>(readValue);

  // Função para retornar um valor novo ao localStorage
  const setValue = (value: T | ((val: T) => T)) => {
    try {
      // Permitir valor ser uma função para ser similar a useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      
      // Salvar estado
      setStoredValue(valueToStore);
      
      // Salvar para localStorage
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
        
        // Disparar evento para outros componentes que usam o mesmo valor
        window.dispatchEvent(new Event('local-storage'));
      }
    } catch (error) {
      console.warn(`Erro ao salvar localStorage key "${key}":`, error);
    }
  };

  // Escutar por mudanças em outras abas/janelas
  useEffect(() => {
    // Sincronizar o valor quando é alterado em outra janela
    const handleStorageChange = () => {
      setStoredValue(readValue());
    };
    
    // Ouvir o evento de mudança do localStorage
    window.addEventListener('storage', handleStorageChange);
    window.addEventListener('local-storage', handleStorageChange);
    
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('local-storage', handleStorageChange);
    };
  }, []);

  return [storedValue, setValue];
}

export default useLocalStorage; 