import { Book, Chapter, Verse } from '../types';

/**
 * Dados simulados para livros da Bíblia
 */
export const mockBooks: Book[] = [
  {
    id: 1,
    name: 'Gênesis',
    abbr: 'Gn',
    testament: 'old',
    position: 1,
    chapters_count: 50
  },
  {
    id: 2,
    name: 'Êxodo',
    abbr: 'Ex',
    testament: 'old',
    position: 2,
    chapters_count: 40
  },
  {
    id: 40,
    name: 'Mateus',
    abbr: 'Mt',
    testament: 'new',
    position: 40,
    chapters_count: 28
  },
  {
    id: 43,
    name: 'João',
    abbr: 'Jo',
    testament: 'new',
    position: 43,
    chapters_count: 21
  },
  {
    id: 19,
    name: 'Salmos',
    abbr: 'Sl',
    testament: 'old',
    position: 19,
    chapters_count: 150
  }
];

/**
 * Dados simulados para capítulos da Bíblia
 */
export const mockChapters: Chapter[] = [
  {
    id: 1,
    book_id: 1,
    number: 1,
    verses_count: 31
  },
  {
    id: 2,
    book_id: 1,
    number: 2,
    verses_count: 25
  },
  {
    id: 601,
    book_id: 19,
    number: 23,
    verses_count: 6
  },
  {
    id: 1001,
    book_id: 40,
    number: 1,
    verses_count: 25
  },
  {
    id: 1085,
    book_id: 43,
    number: 3,
    verses_count: 36
  },
  {
    id: 1089,
    book_id: 43,
    number: 14,
    verses_count: 31
  }
];

/**
 * Dados simulados para versículos da Bíblia
 */
export const mockVerses: Verse[] = [
  {
    id: 1,
    chapter_id: 1,
    number: 1,
    text: 'No princípio, Deus criou os céus e a terra.'
  },
  {
    id: 23786,
    chapter_id: 601,
    number: 1,
    text: 'O Senhor é o meu pastor; de nada terei falta.'
  },
  {
    id: 26000,
    chapter_id: 1001,
    number: 1,
    text: 'Livro da genealogia de Jesus Cristo, filho de Davi, filho de Abraão.'
  },
  {
    id: 31085,
    chapter_id: 1085,
    number: 16,
    text: 'Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.'
  },
  {
    id: 31520,
    chapter_id: 1089,
    number: 27,
    text: 'Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize.'
  }
];

/**
 * Dados simulados para resultados de pesquisa na Bíblia
 */
export const mockSearchResults = [
  {
    book_name: 'João',
    book_id: 43,
    chapter_number: 3,
    verse_number: 16,
    text: 'Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.',
    highlight: '<mark>Deus amou</mark> o mundo de tal maneira que deu o seu Filho unigênito'
  },
  {
    book_name: 'João',
    book_id: 43,
    chapter_number: 14,
    verse_number: 27,
    text: 'Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize.',
    highlight: 'Deixo-vos a <mark>paz</mark>, a minha <mark>paz</mark> vos dou'
  },
  {
    book_name: 'Salmos',
    book_id: 19,
    chapter_number: 23,
    verse_number: 1,
    text: 'O Senhor é o meu pastor; de nada terei falta.',
    highlight: 'O <mark>Senhor</mark> é o meu pastor'
  }
]; 