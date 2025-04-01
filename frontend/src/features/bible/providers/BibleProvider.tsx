import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import useBibleQuery, { BibleQueryKeys } from '../hooks/useBibleQuery';
import { Book, Chapter, Verse, SearchParams, BiblePreferences } from '../types';

/**
 * Interface para o contexto da Bíblia
 */
interface BibleContextData {
  // Estado
  currentBook: Book | null;
  currentChapter: Chapter | null;
  currentVerses: Verse[];
  selectedVerse: Verse | null;
  recentSearches: SearchParams[];
  preferences: BiblePreferences;
  isLoading: boolean;
  error: Error | null;

  // Navegação
  navigateToBook: (bookId: number) => void;
  navigateToChapter: (chapterId: number) => void;
  selectVerse: (verse: Verse) => void;
  navigateToBookChapterVerse: (bookId: number, chapterNumber: number, verseNumber?: number) => void;
  
  // Pesquisa
  searchBible: (params: SearchParams) => void;
  addRecentSearch: (search: SearchParams) => void;
  clearRecentSearches: () => void;
  
  // Preferências
  updatePreferences: (newPreferences: Partial<BiblePreferences>) => void;
  
  // Versículo do dia
  getVerseOfDay: () => Promise<Verse | null>;
  getRandomVerse: (themeId?: string) => Promise<Verse | null>;
  
  // Cache
  prefetchBible: () => Promise<boolean>;
}

// Valores padrão para o contexto
const defaultContextValue: BibleContextData = {
  currentBook: null,
  currentChapter: null,
  currentVerses: [],
  selectedVerse: null,
  recentSearches: [],
  preferences: {
    preferred_version: 'nvi',
    font_size: 'medium',
    show_verse_numbers: true,
    highlight_color: '#FFEB3B',
    night_mode: false,
  },
  isLoading: false,
  error: null,
  
  navigateToBook: () => {},
  navigateToChapter: () => {},
  selectVerse: () => {},
  navigateToBookChapterVerse: () => {},
  searchBible: () => {},
  addRecentSearch: () => {},
  clearRecentSearches: () => {},
  updatePreferences: () => {},
  getVerseOfDay: async () => null,
  getRandomVerse: async () => null,
  prefetchBible: async () => false,
};

// Criar o contexto
const BibleContext = createContext<BibleContextData>(defaultContextValue);

// Hook customizado para usar o contexto da Bíblia
export const useBibleContext = () => {
  const context = useContext(BibleContext);
  
  if (!context) {
    throw new Error('useBibleContext deve ser usado dentro de um BibleProvider');
  }
  
  return context;
};

// Propriedades do provider
interface BibleProviderProps {
  children: ReactNode;
}

/**
 * Provider para o contexto da Bíblia usando React Query
 */
export const BibleProvider: React.FC<BibleProviderProps> = ({ children }) => {
  // Obter as queries e mutations para a Bíblia
  const bibleQueries = useBibleQuery();
  
  // Estado local
  const [currentBookId, setCurrentBookId] = useState<number | null>(null);
  const [currentChapterId, setCurrentChapterId] = useState<number | null>(null);
  const [selectedVerseNumber, setSelectedVerseNumber] = useState<number | null>(null);
  const [recentSearches, setRecentSearches] = useState<SearchParams[]>([]);
  const [preferences, setPreferences] = useState<BiblePreferences>({
    preferred_version: 'nvi',
    font_size: 'medium',
    show_verse_numbers: true,
    highlight_color: '#FFEB3B',
    night_mode: false,
  });
  
  // Carregar dados usando as queries
  const { data: currentBook, isLoading: isLoadingBook, error: bookError } = 
    bibleQueries.useBookQuery(currentBookId || 0, { 
      enabled: !!currentBookId,
      queryKey: [BibleQueryKeys.BOOK, currentBookId || 0]
    });
    
  const { data: currentChapter, isLoading: isLoadingChapter, error: chapterError } = 
    bibleQueries.useChapterQuery(currentChapterId || 0, { 
      enabled: !!currentChapterId,
      queryKey: [BibleQueryKeys.CHAPTER, currentChapterId || 0]
    });
    
  const { data: currentVerses = [], isLoading: isLoadingVerses, error: versesError } = 
    bibleQueries.useVersesQuery(currentChapterId || 0, { 
      enabled: !!currentChapterId,
      queryKey: [BibleQueryKeys.VERSES, currentChapterId || 0]
    });
  
  // Localizar o versículo selecionado
  const selectedVerse = selectedVerseNumber 
    ? currentVerses.find(v => v.number === selectedVerseNumber) || null 
    : null;
  
  // Estado de carregamento e erro
  const isLoading = isLoadingBook || isLoadingChapter || isLoadingVerses;
  const error = bookError || chapterError || versesError;
  
  // Navegação para um livro
  const navigateToBook = useCallback((bookId: number) => {
    setCurrentBookId(bookId);
    setCurrentChapterId(null);
    setSelectedVerseNumber(null);
    
    // Pré-carregar capítulos deste livro
    if (bookId) {
      bibleQueries.useChaptersQuery(bookId);
    }
  }, [bibleQueries]);
  
  // Navegação para um capítulo
  const navigateToChapter = useCallback((chapterId: number) => {
    setCurrentChapterId(chapterId);
    setSelectedVerseNumber(null);
    
    // Pré-carregar versículos deste capítulo
    if (chapterId) {
      bibleQueries.useVersesQuery(chapterId);
    }
  }, [bibleQueries]);
  
  // Selecionar um versículo
  const selectVerse = useCallback((verse: Verse) => {
    setSelectedVerseNumber(verse.number);
  }, []);
  
  // Navegação completa (livro -> capítulo -> versículo)
  const navigateToBookChapterVerse = useCallback(async (
    bookId: number, 
    chapterNumber: number, 
    verseNumber?: number
  ) => {
    // Navegar para o livro primeiro
    setCurrentBookId(bookId);
    
    try {
      // Obter capítulos do livro
      const chapters = await bibleQueries.useChaptersQuery(bookId).refetch();
      
      if (chapters.data) {
        // Encontrar ID do capítulo pelo número
        const targetChapter = chapters.data.find(c => c.number === chapterNumber);
        
        if (targetChapter) {
          // Navegar para o capítulo
          setCurrentChapterId(targetChapter.id);
          
          // Se houver versículo especificado, selecionar
          if (verseNumber) {
            setSelectedVerseNumber(verseNumber);
          }
          
          // Pré-carregar capítulos adjacentes para navegação fluida
          bibleQueries.prefetchAdjacentChapters(bookId, chapterNumber);
        }
      }
    } catch (error) {
      console.error('Erro ao navegar para referência bíblica:', error);
    }
  }, [bibleQueries]);
  
  // Pesquisa na Bíblia
  const searchBible = useCallback((params: SearchParams) => {
    // A pesquisa é feita diretamente via hook no componente que a utiliza
    // Mas adicionamos aos recentes aqui
    addRecentSearch(params);
  }, []);
  
  // Adicionar pesquisa recente
  const addRecentSearch = useCallback((search: SearchParams) => {
    setRecentSearches(prev => {
      // Remover a mesma pesquisa se já existir
      const filtered = prev.filter(s => 
        s.query !== search.query || 
        s.theme !== search.theme || 
        s.book_id !== search.book_id
      );
      
      // Adicionar ao início e limitar a 10 pesquisas
      return [search, ...filtered].slice(0, 10);
    });
  }, []);
  
  // Limpar pesquisas recentes
  const clearRecentSearches = useCallback(() => {
    setRecentSearches([]);
  }, []);
  
  // Atualizar preferências
  const updatePreferences = useCallback((newPreferences: Partial<BiblePreferences>) => {
    setPreferences(prev => ({
      ...prev,
      ...newPreferences
    }));
    
    // Aqui poderíamos salvar no localStorage também
    localStorage.setItem('biblePreferences', JSON.stringify({
      ...preferences,
      ...newPreferences
    }));
  }, [preferences]);
  
  // Obter versículo do dia
  const getVerseOfDay = useCallback(async (): Promise<Verse | null> => {
    try {
      const result = await bibleQueries.useVerseOfDayQuery().refetch();
      return result.data || null;
    } catch (error) {
      console.error('Erro ao obter versículo do dia:', error);
      return null;
    }
  }, [bibleQueries]);
  
  // Obter versículo aleatório
  const getRandomVerse = useCallback(async (themeId?: string): Promise<Verse | null> => {
    try {
      const result = await bibleQueries.useRandomVerseQuery(themeId).refetch();
      return result.data || null;
    } catch (error) {
      console.error('Erro ao obter versículo aleatório:', error);
      return null;
    }
  }, [bibleQueries]);
  
  // Pré-carregar Bíblia para uso offline
  const prefetchBible = useCallback(async (): Promise<boolean> => {
    return bibleQueries.prefetchEntireBible();
  }, [bibleQueries]);
  
  // Valor do contexto
  const contextValue: BibleContextData = {
    currentBook,
    currentChapter,
    currentVerses,
    selectedVerse,
    recentSearches,
    preferences,
    isLoading,
    error: error as Error | null,
    
    navigateToBook,
    navigateToChapter,
    selectVerse,
    navigateToBookChapterVerse,
    searchBible,
    addRecentSearch,
    clearRecentSearches,
    updatePreferences,
    getVerseOfDay,
    getRandomVerse,
    prefetchBible
  };
  
  return (
    <BibleContext.Provider value={contextValue}>
      {children}
    </BibleContext.Provider>
  );
};

export default BibleProvider; 