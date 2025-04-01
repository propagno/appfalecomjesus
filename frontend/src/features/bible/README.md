# Feature: Bíblia

Este módulo é responsável por fornecer a funcionalidade de exploração e busca da Bíblia Sagrada no sistema FaleComJesus, permitindo aos usuários navegar por livros, capítulos e versículos de forma intuitiva.

## Estrutura

```
bible/
├── api/             # Serviços para comunicação com a API
├── components/      # Componentes específicos da Bíblia
├── contexts/        # Contexto global da Bíblia
├── hooks/           # Hooks customizados
├── pages/           # Páginas relacionadas à Bíblia
└── types/           # Tipos e interfaces
```

## Funcionalidades Principais

- Exploração por livros e capítulos
- Visualização de versículos
- Busca por palavras-chave e temas
- Compartilhamento de versículos
- Leitura em voz alta (acessibilidade)
- Marcação de versículos favoritos

## Uso do Contexto

```tsx
import { useBibleContext } from 'features/bible';

function MeuComponente() {
  const { 
    books, 
    selectedBook, 
    selectBook,
    search 
  } = useBibleContext();
  
  // Agora você tem acesso a todas as funcionalidades da Bíblia
}
```

## Páginas Principais

- **BibleExplorerPage**: Interface principal para navegação por livros e capítulos
- **BibleSearchPage**: Permite busca por palavras-chave ou temas

## Componentes Reutilizáveis

- **BookSelector**: Seleção de livros da Bíblia
- **ChapterSelector**: Seleção de capítulos
- **BibleReader**: Exibição de versículos
- **SearchResults**: Exibição de resultados de busca

## Integração com Backend

Este módulo se comunica com as seguintes rotas de API:

- GET /api/bible/books
- GET /api/bible/books/{book_id}/chapters
- GET /api/bible/chapters/{chapter_id}/verses
- GET /api/bible/search
- GET /api/bible/verse
- GET /api/bible/passage
- GET /api/bible/theme

## Integrações com Outras Features

- **Estudo**: Os planos de estudo podem referenciar passagens bíblicas
- **IA**: Explicações contextuais e aprofundadas de versículos
- **Gamificação**: Registro de leituras para conquistas e recompensas 