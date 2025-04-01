import React, { useState } from 'react';
import { useBibleContext } from '../providers/BibleProvider';
import SearchResults from '../components/SearchResults';
import { Search, MoveLeft, X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { SearchResultItem, SearchParams } from '../types';
import useBibleQuery, { BibleQueryKeys } from '../hooks/useBibleQuery';

/**
 * Página de busca da Bíblia
 * Permite buscar versículos por palavra-chave ou tema
 */
export const BibleSearchPage: React.FC = () => {
  const navigate = useNavigate();
  const { searchBible, addRecentSearch } = useBibleContext();
  const { useSearchQuery } = useBibleQuery();
  const [searchTerm, setSearchTerm] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  // Configurar a query de busca
  const searchParams: SearchParams = {
    query: searchTerm,
    limit: 20,
    page: 1
  };

  const { data: searchResults, isLoading: isSearching } = useSearchQuery(searchParams, {
    enabled: hasSearched && !!searchTerm.trim(),
    queryKey: [BibleQueryKeys.SEARCH, searchTerm]
  });

  // Função para lidar com a pesquisa
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchTerm.trim()) return;
    
    searchBible(searchParams);
    addRecentSearch(searchParams);
    setHasSearched(true);
  };

  // Limpar a busca
  const clearSearch = () => {
    setSearchTerm('');
    setHasSearched(false);
  };

  // Navegar para um resultado específico
  const handleResultClick = (result: SearchResultItem) => {
    // Aqui você implementaria a navegação para o versículo específico
    // Por exemplo:
    // navigate(`/bible/read?book=${result.verse.book_id}&chapter=${result.verse.chapter_number}&verse=${result.verse.number}`);
    
    // Por enquanto apenas mostra um alerta
    alert(`Navegando para ${result.verse.book_name} ${result.verse.chapter_number}:${result.verse.number}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Cabeçalho da página */}
        <header className="mb-6">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/bible')}
              className="mr-3 p-2 rounded-full hover:bg-gray-200"
              aria-label="Voltar para o explorador da Bíblia"
            >
              <MoveLeft className="h-5 w-5" />
            </button>
            <h1 className="text-3xl font-bold text-blue-600">Pesquisar na Bíblia</h1>
          </div>
          <p className="text-gray-600 mt-2 ml-10">
            Encontre versículos por palavras-chave, temas ou referências
          </p>
        </header>

        {/* Formulário de busca */}
        <div className="bg-white shadow rounded-lg p-4 mb-6">
          <form onSubmit={handleSearch} className="relative">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Digite palavras-chave, temas ou referências (ex: amor, João 3:16)..."
                className="pl-10 pr-10 py-3 w-full border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              
              {searchTerm && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="absolute inset-y-0 right-12 flex items-center pr-3"
                >
                  <X className="h-5 w-5 text-gray-400 hover:text-gray-700" />
                </button>
              )}
            </div>
            
            <button
              type="submit"
              disabled={!searchTerm.trim() || isSearching}
              className="absolute right-0 inset-y-0 px-4 py-2 bg-blue-600 text-white rounded-r-md hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed"
            >
              {isSearching ? 'Buscando...' : 'Buscar'}
            </button>
          </form>

          {/* Dicas de busca */}
          <div className="mt-4 text-sm text-gray-500">
            <h3 className="font-medium mb-1">Dicas de busca:</h3>
            <ul className="list-disc list-inside space-y-1">
              <li>Use termos específicos para resultados mais precisos (ex: "perdão" em vez de "perda")</li>
              <li>Busque por referências específicas (ex: "João 3:16" ou "Salmos 23")</li>
              <li>Pesquise por temas como "amor", "fé", "esperança", "salvação", etc.</li>
            </ul>
          </div>
        </div>

        {/* Resultados da busca */}
        <div className="bg-white shadow rounded-lg">
          {hasSearched ? (
            <SearchResults 
              searchParams={searchParams}
              onResultClick={handleResultClick} 
            />
          ) : (
            <div className="p-8 text-center text-gray-500">
              <Search className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p className="text-lg">Digite uma palavra ou frase para pesquisar na Bíblia</p>
              <p className="mt-2">
                Sugestões: amor, fé, esperança, salvação, graça, perdão
              </p>
            </div>
          )}
        </div>

        {/* Recursos adicionais */}
        <div className="mt-6 text-center">
          <h3 className="text-lg font-medium mb-2">Recursos de estudo</h3>
          <div className="flex flex-wrap justify-center gap-2">
            <button className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm">
              Concordância
            </button>
            <button className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm">
              Dicionário Bíblico
            </button>
            <button className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm">
              Comentários
            </button>
            <button className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-md text-sm">
              Temas Populares
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BibleSearchPage; 