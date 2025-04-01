# Guia de Implementação: Feature Bíblia

Este documento descreve o processo para implementar a feature de exploração da Bíblia no FaleComJesus, seguindo a mesma arquitetura modular usada na feature de autenticação.

## Estrutura de Diretórios

```
features/bible/
├── api/               # Serviços de API
│   └── bibleService.ts
├── components/        # Componentes específicos da Bíblia
│   ├── BibleReader.tsx
│   ├── BookSelector.tsx
│   ├── ChapterSelector.tsx
│   ├── VerseHighlight.tsx
│   └── SearchResults.tsx
├── contexts/          # Contexto para estado da Bíblia
│   └── BibleContext.tsx
├── hooks/             # Hooks customizados
│   └── useBible.ts
├── pages/             # Páginas da feature
│   ├── BibleExplorerPage.tsx
│   ├── BibleSearchPage.tsx
│   └── index.ts
├── types/             # Tipos e interfaces
│   └── index.ts
└── index.ts           # Exportações principais
```

## Passo a Passo da Implementação

### 1. Definir Tipos (types/index.ts)

Comece definindo as interfaces principais:

```typescript
export interface Book {
  id: number;
  name: string;
  testament: 'old' | 'new';
  chapters: number;
}

export interface Chapter {
  id: number;
  book_id: number;
  number: number;
  verses_count: number;
}

export interface Verse {
  id: number;
  chapter_id: number;
  verse_number: number;
  text: string;
}

export interface BibleSearchResult {
  book_name: string;
  chapter_number: number;
  verse_number: number;
  text: string;
}

export interface BibleState {
  books: Book[];
  selectedBook: Book | null;
  selectedChapter: Chapter | null;
  verses: Verse[];
  isLoading: boolean;
  error: string | null;
}
```

### 2. Implementar API Service (api/bibleService.ts)

Crie um serviço para comunicação com a API da Bíblia:

```typescript
import apiClient from '../../../shared/api/apiClient';
import { Book, Chapter, Verse, BibleSearchResult } from '../types';

export const bibleService = {
  getBooks: async (): Promise<Book[]> => {
    return apiClient.get('/bible/books');
  },
  
  getChapters: async (bookId: number): Promise<Chapter[]> => {
    return apiClient.get(`/bible/books/${bookId}/chapters`);
  },
  
  getVerses: async (chapterId: number): Promise<Verse[]> => {
    return apiClient.get(`/bible/chapters/${chapterId}/verses`);
  },
  
  searchBible: async (query: string): Promise<BibleSearchResult[]> => {
    return apiClient.get('/bible/search', { params: { query } });
  }
};
```

### 3. Criar Hook e Contexto

Siga o padrão utilizado na feature de autenticação:
- Crie um hook `useBible` que utilize React Query
- Implemente um contexto `BibleContext` e provider

### 4. Implementar Componentes

Os componentes devem refletir as diferentes partes da interface da Bíblia:
- `BookSelector`: Seleção de livros
- `ChapterSelector`: Seleção de capítulos
- `BibleReader`: Exibição de versículos
- `VerseHighlight`: Destaque de versículos

### 5. Criar Páginas

- `BibleExplorerPage`: Navegação por livros e capítulos
- `BibleSearchPage`: Busca de textos na Bíblia

### 6. Atualizar Rotas

Adicione as rotas às existentes em `app/routes/Routes.tsx`.

### 7. Implementar Funcionalidades Avançadas

- Compartilhamento de versículos
- Marcadores de texto
- Histórico de leitura
- Modo de leitura (dia/noite)

## Integrações

### Integração com Estudo Personalizado

A feature de Bíblia deve se integrar com o plano de estudo personalizado:
- Os planos de estudo devem poder referenciar textos bíblicos
- Um versículo deve poder ser adicionado para reflexão

### Integração com IA

- A IA deve poder explicar versículos selecionados
- Deve ser possível pedir contexto histórico de passagens

## Implementação Técnica

Use React Query para obter e gerenciar os dados:
- Cache de livros, capítulos e versículos para melhor performance
- Prefetch de dados relacionados para navegação mais fluida

Utilize Tailwind CSS para o estilo dos componentes:
- Design responsivo para diferentes tamanhos de tela
- Acessibilidade com alto contraste e tamanhos de fonte ajustáveis

## Considerações de Performance

- Cache de versículos usados frequentemente
- Carregar apenas os versículos do capítulo atual
- Usar virtualização para listas longas de versículos

Esta implementação segue o mesmo padrão arquitetural da feature de autenticação, mantendo consistência e modularidade no desenvolvimento do sistema. 