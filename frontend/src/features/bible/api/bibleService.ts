import { bibleApi } from '../../../shared/services/api';
import { API_URLS, USE_MOCKS } from '../../../shared/constants/config';
import { 
  Book, 
  Chapter, 
  Verse, 
  SearchResult,
  BooksResponse,
  ChaptersResponse,
  VersesResponse,
  SearchResponse
} from '../types';
import { mockBooks, mockChapters, mockVerses, mockSearchResults } from '../mocks/bibleMocks';

/**
 * Serviço para operações relacionadas à Bíblia
 */
const bibleService = {
  /**
   * Obter todos os livros da Bíblia
   */
  getBooks: async (testament?: string): Promise<BooksResponse> => {
    // Usar mocks quando necessário
    if (USE_MOCKS) {
      const filteredBooks = testament 
        ? mockBooks.filter(book => book.testament === testament) 
        : mockBooks;
      
      return {
        total: filteredBooks.length,
        books: filteredBooks
      };
    }
    
    // Implementação normal com API
    const params = testament ? { testament } : {};
    const response = await bibleApi.get<BooksResponse>('/books', { params });
    return response.data;
  },

  /**
   * Obter um livro específico
   */
  getBook: async (bookId: number): Promise<Book> => {
    if (USE_MOCKS) {
      const book = mockBooks.find(book => book.id === bookId);
      if (!book) throw new Error('Livro não encontrado');
      return book;
    }
    
    const response = await bibleApi.get<Book>(`/books/${bookId}`);
    return response.data;
  },

  /**
   * Obter todos os capítulos de um livro
   */
  getChapters: async (bookId: number): Promise<ChaptersResponse> => {
    if (USE_MOCKS) {
      const filteredChapters = mockChapters.filter(chapter => chapter.book_id === bookId);
      const book = mockBooks.find(book => book.id === bookId);
      
      return {
        chapters: filteredChapters,
        book: book || { 
          id: bookId, 
          name: 'Livro desconhecido', 
          abbr: '', 
          testament: 'old', 
          position: 0, 
          chapters_count: 0 
        }
      };
    }
    
    const response = await bibleApi.get<ChaptersResponse>(`/books/${bookId}/chapters`);
    return response.data;
  },

  /**
   * Obter todos os versículos de um capítulo
   */
  getVerses: async (chapterId: number): Promise<VersesResponse> => {
    if (USE_MOCKS) {
      const filteredVerses = mockVerses.filter(verse => verse.chapter_id === chapterId);
      const chapter = mockChapters.find(chapter => chapter.id === chapterId);
      const book = chapter ? mockBooks.find(book => book.id === chapter.book_id) : undefined;
      
      return {
        verses: filteredVerses,
        chapter: chapter || { 
          id: chapterId, 
          book_id: 0, 
          number: 0, 
          verses_count: 0 
        }
      };
    }
    
    const response = await bibleApi.get<VersesResponse>(`/chapters/${chapterId}/verses`);
    return response.data;
  },

  /**
   * Pesquisar versículos na Bíblia
   */
  searchBible: async (
    query: string, 
    testament?: string, 
    bookId?: number
  ): Promise<SearchResponse> => {
    if (USE_MOCKS) {
      const filteredResults = mockSearchResults.filter(result => {
        // Filtragem simulada baseada nos parâmetros
        const matchesTestament = testament 
          ? mockBooks.find(b => b.id === result.book_id)?.testament === testament 
          : true;
        const matchesBook = bookId ? result.book_id === bookId : true;
        
        return matchesTestament && matchesBook;
      });
      
      // Ajustar para o formato SearchResult esperado
      const searchResult: SearchResult = {
        items: filteredResults.map(item => ({
          verse: {
            id: item.verse_number,
            chapter_id: item.book_id * 1000,
            number: item.verse_number,
            text: item.text
          },
          relevance: 1.0,
          highlight: item.highlight
        })),
        total: filteredResults.length,
        page: 1,
        limit: 20,
        query
      };
      
      return {
        results: searchResult
      };
    }
    
    const params = { q: query };
    if (testament) params['testament'] = testament;
    if (bookId) params['book_id'] = bookId;
    
    const response = await bibleApi.get<SearchResponse>('/search', { params });
    return response.data;
  },

  /**
   * Obter versículo aleatório
   */
  getRandomVerse: async (testament?: string, bookId?: number): Promise<Verse> => {
    if (USE_MOCKS) {
      // Filtrar por testamento e livro, se fornecidos
      let filteredVerses = [...mockVerses];
      
      if (bookId) {
        filteredVerses = filteredVerses.filter(verse => {
          const chapter = mockChapters.find(ch => ch.id === verse.chapter_id);
          return chapter && chapter.book_id === bookId;
        });
      }
      
      if (testament) {
        filteredVerses = filteredVerses.filter(verse => {
          const chapter = mockChapters.find(ch => ch.id === verse.chapter_id);
          if (!chapter) return false;
          const book = mockBooks.find(b => b.id === chapter.book_id);
          return book && book.testament === testament;
        });
      }
      
      // Escolher um versículo aleatório
      const randomIndex = Math.floor(Math.random() * filteredVerses.length);
      return filteredVerses[randomIndex] || mockVerses[0];
    }
    
    const params = {};
    if (testament) params['testament'] = testament;
    if (bookId) params['book_id'] = bookId;
    
    const response = await bibleApi.get<Verse>('/random-verse', { params });
    return response.data;
  },

  /**
   * Obter versículo do dia
   */
  getVerseOfDay: async (): Promise<Verse> => {
    if (USE_MOCKS) {
      // Usar um versículo fixo como "versículo do dia"
      return mockVerses[0];
    }
    
    const response = await bibleApi.get<Verse>('/verse-of-day');
    return response.data;
  }
};

export default bibleService; 