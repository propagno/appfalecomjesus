import { useQuery, useQueryClient, UseQueryOptions, UseQueryResult } from '@tanstack/react-query';
import bibleService from '../api/bibleService';
import { 
  Book, 
  Chapter, 
  Verse, 
  SearchParams, 
  SearchResult,
  BibleTheme,
  BooksResponse,
  ChaptersResponse,
  VersesResponse,
  SearchResponse
} from '../types';

/**
 * Chaves de query para a cache da Bíblia
 */
export enum BibleQueryKeys {
  BOOKS = 'bibleBooks',
  BOOK = 'bibleBook',
  CHAPTERS = 'bibleChapters',
  CHAPTER = 'bibleChapter',
  VERSES = 'bibleVerses',
  VERSE = 'bibleVerse',
  SEARCH = 'bibleSearch',
  THEMES = 'bibleThemes',
  VERSE_OF_DAY = 'bibleVerseOfDay',
  RANDOM_VERSE = 'bibleRandomVerse',
}

/**
 * Hook com queries e mutations para a Bíblia usando React Query
 * Implementação do item 10.5.2 - Cache persistente e React Query
 */
export const useBibleQuery = () => {
  const queryClient = useQueryClient();
  
  // Query para obter todos os livros da Bíblia
  const useBooksQuery = (testament?: 'old' | 'new', options?: UseQueryOptions<BooksResponse, Error, Book[]>) => 
    useQuery<BooksResponse, Error, Book[]>({
      queryKey: [BibleQueryKeys.BOOKS, testament],
      queryFn: () => bibleService.getBooks(testament),
      staleTime: 24 * 60 * 60 * 1000, // 24 horas (dados muito estáticos)
      gcTime: 30 * 24 * 60 * 60 * 1000, // 30 dias
      select: (data) => data.books,
      ...options
    });
  
  // Query para obter um livro específico
  const useBookQuery = (bookId: number, options?: UseQueryOptions<Book, Error>) => 
    useQuery<Book, Error>({
      queryKey: [BibleQueryKeys.BOOK, bookId],
      queryFn: () => bibleService.getBook(bookId),
      staleTime: 24 * 60 * 60 * 1000, // 24 horas
      gcTime: 30 * 24 * 60 * 60 * 1000, // 30 dias
      enabled: !!bookId,
      ...options
    });
  
  // Query para obter capítulos de um livro
  const useChaptersQuery = (bookId: number, options?: UseQueryOptions<ChaptersResponse, Error, Chapter[]>) => 
    useQuery<ChaptersResponse, Error, Chapter[]>({
      queryKey: [BibleQueryKeys.CHAPTERS, bookId],
      queryFn: () => bibleService.getChapters(bookId),
      staleTime: 24 * 60 * 60 * 1000, // 24 horas
      gcTime: 30 * 24 * 60 * 60 * 1000, // 30 dias
      enabled: !!bookId,
      select: (data) => data.chapters,
      ...options
    });
  
  // Query para obter um capítulo específico
  const useChapterQuery = (chapterId: number, options?: UseQueryOptions<Chapter, Error>) => 
    useQuery<Chapter, Error>({
      queryKey: [BibleQueryKeys.CHAPTER, chapterId],
      queryFn: async () => {
        // Implementação alternativa já que não existe getChapter diretamente
        const chapterId100 = Math.floor(chapterId / 1000); // Extrair bookId
        const chaptersResponse = await bibleService.getChapters(chapterId100);
        const chapter = chaptersResponse.chapters.find(c => c.id === chapterId);
        if (!chapter) throw new Error('Capítulo não encontrado');
        return chapter;
      },
      staleTime: 24 * 60 * 60 * 1000, // 24 horas
      gcTime: 30 * 24 * 60 * 60 * 1000, // 30 dias
      enabled: !!chapterId,
      ...options
    });
  
  // Query para obter versículos de um capítulo
  const useVersesQuery = (chapterId: number, options?: UseQueryOptions<VersesResponse, Error, Verse[]>) => 
    useQuery<VersesResponse, Error, Verse[]>({
      queryKey: [BibleQueryKeys.VERSES, chapterId],
      queryFn: () => bibleService.getVerses(chapterId),
      staleTime: 60 * 60 * 1000, // 1 hora
      gcTime: 7 * 24 * 60 * 60 * 1000, // 7 dias
      enabled: !!chapterId,
      select: (data) => data.verses,
      ...options
    });
  
  // Query para obter um versículo específico
  const useVerseQuery = (chapterId: number, verseNumber: number, options?: UseQueryOptions<Verse, Error>) => 
    useQuery<Verse, Error>({
      queryKey: [BibleQueryKeys.VERSE, chapterId, verseNumber],
      queryFn: async () => {
        // Implementação alternativa já que não existe getVerse diretamente
        const versesResponse = await bibleService.getVerses(chapterId);
        const verse = versesResponse.verses.find(v => v.number === verseNumber);
        if (!verse) throw new Error('Versículo não encontrado');
        return verse;
      },
      staleTime: 60 * 60 * 1000, // 1 hora
      gcTime: 7 * 24 * 60 * 60 * 1000, // 7 dias
      enabled: !!chapterId && !!verseNumber,
      ...options
    });
  
  // Query para pesquisa na Bíblia
  const useSearchQuery = (params: SearchParams, options?: UseQueryOptions<SearchResponse, Error, SearchResult>) => 
    useQuery<SearchResponse, Error, SearchResult>({
      queryKey: [BibleQueryKeys.SEARCH, params],
      queryFn: () => bibleService.searchBible(params.query || '', params.testament, params.book_id),
      staleTime: 5 * 60 * 1000, // 5 minutos
      gcTime: 24 * 60 * 60 * 1000, // 24 horas
      enabled: !!params.query || !!params.theme || !!params.book_id,
      select: (data) => data.results,
      ...options
    });
  
  // Query para obter versículos por tema
  const useVersesByThemeQuery = (themeId: string, options?: UseQueryOptions<SearchResponse, Error, Verse[]>) => 
    useQuery<SearchResponse, Error, Verse[]>({
      queryKey: [BibleQueryKeys.THEMES, themeId],
      queryFn: () => bibleService.searchBible(themeId),
      staleTime: 60 * 60 * 1000, // 1 hora
      gcTime: 7 * 24 * 60 * 60 * 1000, // 7 dias
      enabled: !!themeId,
      select: (data) => data.results.items.map(item => item.verse),
      ...options
    });
  
  // Query para obter o versículo do dia
  const useVerseOfDayQuery = (options?: UseQueryOptions<Verse, Error>) => 
    useQuery<Verse, Error>({
      queryKey: [BibleQueryKeys.VERSE_OF_DAY, new Date().toDateString()], // Mudamos a chave diariamente
      queryFn: () => bibleService.getVerseOfDay(),
      staleTime: 24 * 60 * 60 * 1000, // 24 horas (muda só uma vez por dia)
      ...options
    });
  
  // Query para obter um versículo aleatório
  const useRandomVerseQuery = (themeId?: string, options?: UseQueryOptions<Verse, Error>) => 
    useQuery<Verse, Error>({
      queryKey: [BibleQueryKeys.RANDOM_VERSE, themeId],
      queryFn: () => bibleService.getRandomVerse(themeId),
      staleTime: 0, // Sempre renovar quando solicitado
      gcTime: 0, // Não armazenar em cache (anteriormente cacheTime)
      ...options
    });
  
  // Prefetch versículos de capítulos adjacentes (para navegação mais fluida)
  const prefetchAdjacentChapters = async (bookId: number, currentChapterNumber: number) => {
    try {
      // Obter todos os capítulos do livro atual
      const chaptersResponse = await queryClient.fetchQuery<ChaptersResponse>({
        queryKey: [BibleQueryKeys.CHAPTERS, bookId],
        queryFn: () => bibleService.getChapters(bookId)
      });
      
      // Extrair array de capítulos
      const chapters = chaptersResponse.chapters;
      
      // Encontrar capítulos anterior e próximo
      const currentChapterIndex = chapters.findIndex(ch => ch.number === currentChapterNumber);
      
      // Prefetch do capítulo anterior
      if (currentChapterIndex > 0) {
        const prevChapter = chapters[currentChapterIndex - 1];
        queryClient.prefetchQuery<VersesResponse>({
          queryKey: [BibleQueryKeys.VERSES, prevChapter.id],
          queryFn: () => bibleService.getVerses(prevChapter.id)
        });
      }
      
      // Prefetch do próximo capítulo
      if (currentChapterIndex < chapters.length - 1) {
        const nextChapter = chapters[currentChapterIndex + 1];
        queryClient.prefetchQuery<VersesResponse>({
          queryKey: [BibleQueryKeys.VERSES, nextChapter.id],
          queryFn: () => bibleService.getVerses(nextChapter.id)
        });
      }
    } catch (error) {
      console.error('Erro ao pré-carregar capítulos adjacentes:', error);
    }
  };
  
  // Pré-carregar toda a Bíblia para uso offline (cuidado com o uso de dados do usuário)
  const prefetchEntireBible = async () => {
    try {
      // Obter todos os livros
      const booksResponse = await queryClient.fetchQuery<BooksResponse>({
        queryKey: [BibleQueryKeys.BOOKS],
        queryFn: () => bibleService.getBooks()
      });
      
      // Para cada livro, obter capítulos e versículos
      for (const book of booksResponse.books) {
        await queryClient.fetchQuery<ChaptersResponse>({
          queryKey: [BibleQueryKeys.CHAPTERS, book.id],
          queryFn: () => bibleService.getChapters(book.id)
        });
      }
      
      return true;
    } catch (error) {
      console.error('Erro ao pré-carregar Bíblia completa:', error);
      return false;
    }
  };
  
  return {
    useBooksQuery,
    useBookQuery,
    useChaptersQuery,
    useChapterQuery,
    useVersesQuery,
    useVerseQuery,
    useSearchQuery,
    useVersesByThemeQuery,
    useVerseOfDayQuery,
    useRandomVerseQuery,
    prefetchAdjacentChapters,
    prefetchEntireBible
  };
};

export default useBibleQuery; 