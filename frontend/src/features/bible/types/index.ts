/**
 * Tipos para a feature da Bíblia
 */

/**
 * Representa um livro da Bíblia
 */
export interface Book {
  id: number;
  name: string;
  abbr: string;
  testament: 'old' | 'new';
  position: number;
  chapters_count: number;
}

/**
 * Representa um capítulo da Bíblia
 */
export interface Chapter {
  id: number;
  book_id: number;
  number: number;
  verses_count: number;
  book_name?: string;
  book_abbr?: string;
}

/**
 * Representa um versículo da Bíblia
 */
export interface Verse {
  id: number;
  chapter_id: number;
  number: number;
  text: string;
  book_name?: string;
  chapter_number?: number;
  reference?: string;
}

/**
 * Parâmetros para pesquisa na Bíblia
 */
export interface SearchParams {
  query?: string;         // Texto de busca
  book_id?: number;       // Filtrar por livro
  testament?: 'old' | 'new'; // Filtrar por testamento
  theme?: string;         // Filtrar por tema
  limit?: number;         // Limitar quantidade de resultados
  page?: number;          // Paginação
}

/**
 * Estrutura de um item nos resultados de pesquisa
 */
export interface SearchResultItem {
  verse: Verse;
  relevance: number;
  highlight: string;
}

/**
 * Resultados de uma pesquisa na Bíblia
 */
export interface SearchResult {
  items: SearchResultItem[];
  total: number;
  page: number;
  limit: number;
  query: string;
}

/**
 * Resposta da API para listagem de livros
 */
export interface BooksResponse {
  books: Book[];
  total: number;
}

/**
 * Resposta da API para listagem de capítulos
 */
export interface ChaptersResponse {
  chapters: Chapter[];
  book: Book;
}

/**
 * Resposta da API para listagem de versículos
 */
export interface VersesResponse {
  verses: Verse[];
  chapter: Chapter;
}

/**
 * Resposta da API para pesquisa
 */
export interface SearchResponse {
  results: SearchResult;
}

/**
 * Representa um tema ou categoria da Bíblia
 */
export interface BibleTheme {
  id: string;
  name: string;
  description?: string;
  verses_count: number;
}

/**
 * Resposta da API para listagem de temas
 */
export interface ThemesResponse {
  themes: BibleTheme[];
  total: number;
}

/**
 * Preferências do usuário para navegação bíblica
 */
export interface BiblePreferences {
  preferred_version: string;
  font_size: 'small' | 'medium' | 'large';
  show_verse_numbers: boolean;
  highlight_color: string;
  night_mode: boolean;
}

/**
 * Estado global da navegação bíblica
 */
export interface BibleState {
  currentBook: Book | null;
  currentChapter: Chapter | null;
  verses: Verse[];
  recentSearches: string[];
  isLoading: boolean;
  error: string | null;
  preferences: BiblePreferences;
} 