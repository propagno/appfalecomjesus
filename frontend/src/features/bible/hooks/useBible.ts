import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import bibleService from '../api/bibleService';
import { 
  Book, 
  Chapter, 
  Verse, 
  SearchResultItem, 
  BooksResponse, 
  ChaptersResponse, 
  VersesResponse,
  SearchResponse
} from '../types';
import { BibleContextType } from '../contexts/BibleContext';

/**
 * Interface para estado da Bíblia
 */
interface BibleState {
  selectedBook: Book | null;
  selectedChapter: Chapter | null;
  verses: Verse[];
  searchResults: SearchResultItem[];
  isLoading: boolean;
  isSearching: boolean;
  error: Error | null;
}

/**
 * Hook para gerenciar a interação com a Bíblia
 * Utiliza React Query para gerenciar cache e estado
 */
export const useBible = (): BibleContextType => {
  const queryClient = useQueryClient();
  
  // Estado local para rastrear seleções do usuário
  const [state, setState] = useState<BibleState>({
    selectedBook: null,
    selectedChapter: null,
    verses: [],
    searchResults: [],
    isLoading: false,
    isSearching: false,
    error: null
  });

  // Query para buscar lista de livros da Bíblia (desabilitada por padrão)
  const {
    data: booksResponse,
    isLoading: isLoadingBooks,
    error: booksError,
    refetch: refetchBooks,
  } = useQuery<BooksResponse, Error>({
    queryKey: ['books'],
    queryFn: () => bibleService.getBooks(),
    enabled: false, // Não carregar automaticamente
  });

  // Query para buscar capítulos de um livro selecionado
  const {
    data: chaptersResponse,
    isLoading: isLoadingChapters,
    error: chaptersError,
    refetch: refetchChapters,
  } = useQuery<ChaptersResponse, Error>({
    queryKey: ['chapters', state.selectedBook?.id],
    queryFn: async () => {
      if (!state.selectedBook?.id) {
        throw new Error('Livro não selecionado');
      }
      return await bibleService.getChapters(state.selectedBook.id);
    },
    enabled: !!state.selectedBook?.id,
  });

  // Query para buscar versículos de um capítulo selecionado
  const {
    data: versesResponse,
    isLoading: isLoadingVerses,
    error: versesError,
    refetch: refetchVerses,
  } = useQuery<VersesResponse, Error>({
    queryKey: ['verses', state.selectedChapter?.id],
    queryFn: async () => {
      if (!state.selectedChapter?.id) {
        throw new Error('Capítulo não selecionado');
      }
      return await bibleService.getVerses(state.selectedChapter.id);
    },
    enabled: !!state.selectedChapter?.id,
  });

  // Busca na Bíblia
  const search = async (query: string): Promise<SearchResultItem[]> => {
    if (!query || query.trim().length < 3) {
      setState(prev => ({ ...prev, searchResults: [], isSearching: false }));
      return [];
    }
    
    try {
      setState(prev => ({ ...prev, isSearching: true, error: null }));
      const response = await bibleService.searchBible(query);
      const searchItems = response.results.items || [];
      setState(prev => ({ ...prev, searchResults: searchItems }));
      return searchItems;
    } catch (error) {
      setState(prev => ({ ...prev, error: error as Error, searchResults: [] }));
      return [];
    } finally {
      setState(prev => ({ ...prev, isSearching: false }));
    }
  };

  // Obter um versículo específico
  const getSpecificVerse = async (bookId: number, chapterNumber: number, verseNumber: number): Promise<Verse> => {
    try {
      setState(prev => ({ ...prev, isLoading: true, error: null }));
      // Buscar todos os capítulos do livro
      const chaptersResp = await bibleService.getChapters(bookId);
      const chapter = chaptersResp.chapters.find(c => c.number === chapterNumber);
      
      if (!chapter) throw new Error('Capítulo não encontrado');
      
      // Buscar todos os versículos do capítulo
      const versesResp = await bibleService.getVerses(chapter.id);
      const verse = versesResp.verses.find(v => v.number === verseNumber);
      
      if (!verse) throw new Error('Versículo não encontrado');
      
      return verse;
    } catch (error) {
      setState(prev => ({ ...prev, error: error as Error }));
      throw error;
    } finally {
      setState(prev => ({ ...prev, isLoading: false }));
    }
  };

  // Obter versículos por tema
  const getVersesByTheme = async (theme: string, count: number = 10): Promise<SearchResultItem[]> => {
    try {
      setState(prev => ({ ...prev, isSearching: true, error: null }));
      // Usar a função de busca normal
      const response = await bibleService.searchBible(theme);
      const searchItems = response.results.items || [];
      const limitedItems = searchItems.slice(0, count);
      setState(prev => ({ ...prev, searchResults: limitedItems }));
      return limitedItems;
    } catch (error) {
      setState(prev => ({ ...prev, error: error as Error, searchResults: [] }));
      return [];
    } finally {
      setState(prev => ({ ...prev, isSearching: false }));
    }
  };

  // Ações
  const selectBook = (book: Book | null) => {
    setState(prev => ({ 
      ...prev, 
      selectedBook: book,
      selectedChapter: null,
      verses: []
    }));
    
    if (book) {
      refetchChapters();
    }
  };

  const selectChapter = (chapter: Chapter | null) => {
    setState(prev => ({ 
      ...prev, 
      selectedChapter: chapter,
      verses: []
    }));
    
    if (chapter) {
      refetchVerses();
    }
  };

  const clearSelection = () => {
    setState(prev => ({
      ...prev,
      selectedBook: null,
      selectedChapter: null,
      verses: []
    }));
  };

  // Função para inicializar a carga de livros quando necessário
  const loadBooks = () => {
    refetchBooks();
  };

  // Extrair arrays das respostas
  const books: Book[] = booksResponse?.books || [];
  const chapters: Chapter[] = chaptersResponse?.chapters || [];
  const verses: Verse[] = versesResponse?.verses || [];

  return {
    // Estados
    books,
    chapters,
    verses,
    selectedBook: state.selectedBook,
    selectedChapter: state.selectedChapter,
    searchResults: state.searchResults,
    isLoading: isLoadingBooks || isLoadingChapters || isLoadingVerses || state.isLoading,
    error: (booksError || chaptersError || versesError || state.error) as Error | null,
    
    // Estados específicos de loading
    isLoadingBooks,
    isLoadingChapters,
    isLoadingVerses,
    isSearching: state.isSearching,
    
    // Ações
    selectBook,
    selectChapter,
    clearSelection,
    search,
    getSpecificVerse,
    getVersesByTheme,
    loadBooks
  };
}; 