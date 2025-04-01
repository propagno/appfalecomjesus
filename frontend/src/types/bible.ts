export interface BibleBook {
  id: string;
  name: string;
  testament: 'old' | 'new';
  chapters: BibleChapter[];
}

export interface BibleChapter {
  id: string;
  bookId: string;
  number: number;
  verses: BibleVerse[];
}

export interface BibleVerse {
  id: string;
  chapterId: string;
  number: number;
  text: string;
}

export interface BibleReference {
  book: string;
  chapter: number;
  verse: number;
  text?: string;
}

export interface BibleSearchResult {
  verse: BibleVerse;
  chapter: BibleChapter;
  book: BibleBook;
  highlights?: {
    start: number;
    end: number;
  }[];
}

export interface BibleFilters {
  testament?: BibleBook['testament'];
  book?: string;
  chapter?: number;
  search?: string;
  theme?: string;
}

export interface BibleTheme {
  id: string;
  name: string;
  description: string;
  references: BibleReference[];
} 
