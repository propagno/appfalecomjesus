import React, { createContext, ReactNode, useContext } from 'react';
import { useBible } from '../hooks/useBible';
import { Book, Chapter, Verse, SearchResultItem } from '../types';

// Definir o tipo para o contexto da Bíblia
export interface BibleContextType {
  // Estado
  books: Book[];
  chapters: Chapter[];
  verses: Verse[];
  selectedBook: Book | null;
  selectedChapter: Chapter | null;
  searchResults: SearchResultItem[];
  isLoading: boolean;
  error: Error | null;
  
  // Estados específicos de loading
  isLoadingBooks: boolean;
  isLoadingChapters: boolean;
  isLoadingVerses: boolean;
  isSearching: boolean;
  
  // Ações
  selectBook: (book: Book | null) => void;
  selectChapter: (chapter: Chapter | null) => void;
  clearSelection: () => void;
  search: (query: string) => Promise<SearchResultItem[]>;
  getSpecificVerse: (bookId: number, chapterNumber: number, verseNumber: number) => Promise<Verse>;
  getVersesByTheme: (theme: string, count?: number) => Promise<SearchResultItem[]>;
  loadBooks: () => void;
}

// Criar o contexto
const BibleContext = createContext<BibleContextType | undefined>(undefined);

// Props do Provider
interface BibleProviderProps {
  children: ReactNode;
}

/**
 * Provider que fornece o contexto da Bíblia para toda a aplicação
 */
export const BibleProvider: React.FC<BibleProviderProps> = ({ children }) => {
  const bible = useBible();
  
  return (
    <BibleContext.Provider value={bible}>
      {children}
    </BibleContext.Provider>
  );
};

/**
 * Hook para usar o contexto da Bíblia
 * Deve ser usado dentro de um BibleProvider
 */
export const useBibleContext = (): BibleContextType => {
  const context = useContext(BibleContext);
  
  if (context === undefined) {
    throw new Error('useBibleContext deve ser usado dentro de um BibleProvider');
  }
  
  return context;
};

export default BibleContext; 