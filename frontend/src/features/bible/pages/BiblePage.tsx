import React, { useState, useEffect } from 'react';
import { useBibleContext } from '../providers/BibleProvider';
import useBibleQuery, { BibleQueryKeys } from '../hooks/useBibleQuery';
import { Book, Chapter, Verse, SearchParams } from '../types';

/**
 * Página de demonstração da Bíblia
 * (Item 10.5 - Integração com MS-Bible)
 */
const BiblePage: React.FC = () => {
  // Hooks de contexto e queries
  const bibleContext = useBibleContext();
  const bibleQueries = useBibleQuery();
  
  // Estados locais
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedTestament, setSelectedTestament] = useState<'old' | 'new' | undefined>(undefined);
  
  // Queries React Query (dados)
  const { 
    data: books = [], 
    isLoading: isLoadingBooks 
  } = bibleQueries.useBooksQuery(selectedTestament, {
    queryKey: [BibleQueryKeys.BOOKS, selectedTestament]
  });
  
  const { 
    data: chapters = [], 
    isLoading: isLoadingChapters 
  } = bibleQueries.useChaptersQuery(
    bibleContext.currentBook?.id || 0, 
    { 
      enabled: !!bibleContext.currentBook,
      queryKey: [BibleQueryKeys.CHAPTERS, bibleContext.currentBook?.id || 0]
    }
  );
  
  const { 
    data: verseOfDay, 
    isLoading: isLoadingVerseOfDay 
  } = bibleQueries.useVerseOfDayQuery({
    queryKey: [BibleQueryKeys.VERSE_OF_DAY, new Date().toDateString()]
  });
  
  // Pesquisa de versículos
  const searchParams: SearchParams = {
    query: searchQuery,
    book_id: bibleContext.currentBook?.id,
    testament: selectedTestament
  };
  
  const { 
    data: searchResults, 
    isLoading: isLoadingSearch 
  } = bibleQueries.useSearchQuery(searchParams, { 
    enabled: searchQuery.length > 2,
    queryKey: [BibleQueryKeys.SEARCH, searchParams]
  });
  
  // Adicionar pesquisa aos recentes quando for executada
  useEffect(() => {
    if (searchQuery.length > 2 && searchResults) {
      bibleContext.addRecentSearch(searchParams);
    }
  }, [searchResults, searchParams, bibleContext.addRecentSearch, searchQuery]);
  
  // Handlers
  const handleSelectBook = (book: Book) => {
    bibleContext.navigateToBook(book.id);
  };
  
  const handleSelectChapter = (chapter: Chapter) => {
    bibleContext.navigateToChapter(chapter.id);
  };
  
  const handleVerseClick = (verse: Verse) => {
    bibleContext.selectVerse(verse);
  };
  
  const handleTestamentFilter = (testament?: 'old' | 'new') => {
    setSelectedTestament(testament);
  };
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (searchQuery.length > 2) {
      bibleContext.searchBible(searchParams);
    }
  };
  
  const handleRandomVerse = async () => {
    const randomVerse = await bibleContext.getRandomVerse();
    if (randomVerse && randomVerse.chapter_id) {
      // Navegar até o versículo aleatório
      // (requer implementação de navegação por referência)
    }
  };
  
  const handleFontSizeChange = (size: 'small' | 'medium' | 'large') => {
    bibleContext.updatePreferences({
      font_size: size
    });
  };
  
  const handleToggleNightMode = () => {
    bibleContext.updatePreferences({
      night_mode: !bibleContext.preferences.night_mode
    });
  };
  
  // Manipulação de UI com base nas preferências
  const verseTextClass = bibleContext.preferences.font_size === 'small' 
    ? 'text-sm' 
    : bibleContext.preferences.font_size === 'large' 
      ? 'text-xl' 
      : 'text-base';
  
  const containerClass = bibleContext.preferences.night_mode 
    ? 'bg-gray-900 text-white' 
    : 'bg-white text-gray-800';
  
  // Renderização
  return (
    <div className={`flex flex-col min-h-screen ${containerClass}`}>
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Bíblia Online</h1>
        <div className="flex mt-2">
          <form onSubmit={handleSearch} className="flex-1 flex">
            <input
              type="text"
              placeholder="Pesquisar na Bíblia..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 text-gray-900 rounded-l"
            />
            <button
              type="submit"
              className="bg-blue-800 hover:bg-blue-900 px-4 py-2 rounded-r"
            >
              Buscar
            </button>
          </form>
          <div className="ml-4 flex items-center space-x-2">
            <button
              onClick={() => handleFontSizeChange('small')}
              className={`px-2 py-1 rounded ${
                bibleContext.preferences.font_size === 'small' ? 'bg-blue-800' : 'bg-blue-700'
              }`}
            >
              A-
            </button>
            <button
              onClick={() => handleFontSizeChange('medium')}
              className={`px-2 py-1 rounded ${
                bibleContext.preferences.font_size === 'medium' ? 'bg-blue-800' : 'bg-blue-700'
              }`}
            >
              A
            </button>
            <button
              onClick={() => handleFontSizeChange('large')}
              className={`px-2 py-1 rounded ${
                bibleContext.preferences.font_size === 'large' ? 'bg-blue-800' : 'bg-blue-700'
              }`}
            >
              A+
            </button>
            <button
              onClick={handleToggleNightMode}
              className="ml-2 px-3 py-1 rounded bg-blue-700 hover:bg-blue-800"
            >
              {bibleContext.preferences.night_mode ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </header>
      
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Navegação */}
        <div className="w-1/4 border-r overflow-y-auto">
          <div className="p-4 border-b">
            <h2 className="font-bold text-lg mb-2">Livros</h2>
            <div className="flex mb-4">
              <button
                onClick={() => handleTestamentFilter(undefined)}
                className={`flex-1 py-1 ${!selectedTestament ? 'font-bold' : ''}`}
              >
                Todos
              </button>
              <button
                onClick={() => handleTestamentFilter('old')}
                className={`flex-1 py-1 ${selectedTestament === 'old' ? 'font-bold' : ''}`}
              >
                AT
              </button>
              <button
                onClick={() => handleTestamentFilter('new')}
                className={`flex-1 py-1 ${selectedTestament === 'new' ? 'font-bold' : ''}`}
              >
                NT
              </button>
            </div>
            
            {isLoadingBooks ? (
              <div className="text-center p-4">Carregando livros...</div>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                {books.map((book) => (
                  <button
                    key={book.id}
                    onClick={() => handleSelectBook(book)}
                    className={`p-2 text-left hover:bg-blue-100 ${
                      bibleContext.currentBook?.id === book.id ? 'bg-blue-100 font-bold' : ''
                    } ${bibleContext.preferences.night_mode ? 'hover:bg-blue-900' : 'hover:bg-blue-100'}`}
                  >
                    {book.abbr} - {book.name}
                  </button>
                ))}
              </div>
            )}
          </div>
          
          {bibleContext.currentBook && (
            <div className="p-4">
              <h2 className="font-bold text-lg mb-2">
                Capítulos de {bibleContext.currentBook.name}
              </h2>
              {isLoadingChapters ? (
                <div className="text-center p-4">Carregando capítulos...</div>
              ) : (
                <div className="grid grid-cols-5 gap-2">
                  {chapters.map((chapter) => (
                    <button
                      key={chapter.id}
                      onClick={() => handleSelectChapter(chapter)}
                      className={`p-2 text-center hover:bg-blue-100 ${
                        bibleContext.currentChapter?.id === chapter.id ? 'bg-blue-100 font-bold' : ''
                      } ${bibleContext.preferences.night_mode ? 'hover:bg-blue-900' : 'hover:bg-blue-100'}`}
                    >
                      {chapter.number}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
        
        {/* Conteúdo principal */}
        <div className="flex-1 p-6 overflow-y-auto">
          {bibleContext.isLoading ? (
            <div className="text-center p-10">Carregando conteúdo...</div>
          ) : searchQuery.length > 2 && searchResults ? (
            // Resultados da pesquisa
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-4">
                Resultados para: "{searchQuery}"
              </h2>
              {searchResults.items.length === 0 ? (
                <p>Nenhum resultado encontrado.</p>
              ) : (
                <div className="space-y-4">
                  {searchResults.items.map((item) => (
                    <div
                      key={item.verse.id}
                      className="p-4 border rounded hover:bg-gray-50"
                      onClick={() => {
                        // Navegar para o versículo encontrado
                        // Requer implementação adicional
                      }}
                    >
                      <p className="font-bold">{item.verse.reference}</p>
                      <div
                        className={verseTextClass}
                        dangerouslySetInnerHTML={{ __html: item.highlight }}
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : bibleContext.currentChapter && bibleContext.currentVerses.length > 0 ? (
            // Exibição de capítulo
            <div>
              <h2 className="text-2xl font-bold mb-4">
                {bibleContext.currentBook?.name} {bibleContext.currentChapter.number}
              </h2>
              <div className="space-y-2">
                {bibleContext.currentVerses.map((verse) => (
                  <div
                    key={verse.id}
                    className={`${
                      bibleContext.selectedVerse?.id === verse.id
                        ? `bg-${bibleContext.preferences.highlight_color}`
                        : ''
                    }`}
                    onClick={() => handleVerseClick(verse)}
                  >
                    <span className="font-bold mr-2">
                      {bibleContext.preferences.show_verse_numbers && verse.number}
                    </span>
                    <span className={verseTextClass}>{verse.text}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : isLoadingVerseOfDay ? (
            <div className="text-center p-10">Carregando versículo do dia...</div>
          ) : verseOfDay ? (
            // Versículo do dia (quando nada está selecionado)
            <div className="text-center max-w-2xl mx-auto p-10 border rounded shadow">
              <h2 className="text-2xl font-bold mb-6">Versículo do Dia</h2>
              <p className="text-xl italic mb-4">{verseOfDay.text}</p>
              <p className="font-bold">{verseOfDay.reference}</p>
              <button
                onClick={handleRandomVerse}
                className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Versículo Aleatório
              </button>
            </div>
          ) : (
            // Estado inicial ou carregamento
            <div className="text-center p-10">
              <p className="mb-4">Selecione um livro e capítulo para começar a leitura.</p>
              <button
                onClick={handleRandomVerse}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Versículo Aleatório
              </button>
            </div>
          )}
        </div>
        
        {/* Painel lateral - detalhes do versículo */}
        {bibleContext.selectedVerse && (
          <div className="w-1/4 border-l p-4 overflow-y-auto">
            <h2 className="font-bold text-lg mb-2">Versículo Selecionado</h2>
            <p className="font-bold">{bibleContext.selectedVerse.reference}</p>
            <p className={`my-4 ${verseTextClass}`}>{bibleContext.selectedVerse.text}</p>
            
            <div className="space-y-4 mt-6">
              <button
                className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                onClick={() => {
                  // Aqui poderia abrir um modal ou direcionar para o chat IA
                  // para perguntar sobre este versículo
                }}
              >
                Perguntar ao Chat IA
              </button>
              
              <button
                className="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                onClick={() => {
                  // Função para compartilhar versículo
                }}
              >
                Compartilhar
              </button>
              
              <button
                className="w-full bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700"
                onClick={() => {
                  // Função para marcar versículo como favorito
                }}
              >
                Favorito
              </button>
            </div>
          </div>
        )}
      </div>
      
      <footer className="bg-gray-100 text-center p-4 border-t">
        <p>
          FaleComJesus © 2023 - Item 10.5 Integração com MS-Bible
        </p>
      </footer>
    </div>
  );
};

export default BiblePage; 