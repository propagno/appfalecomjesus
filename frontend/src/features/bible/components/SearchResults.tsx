import React from 'react';
import { SearchX, ExternalLink } from 'lucide-react';
import { SearchResultItem } from '../types';
import useBibleQuery, { BibleQueryKeys } from '../hooks/useBibleQuery';
import { SearchParams } from '../types';

interface SearchResultsProps {
  className?: string;
  onResultClick?: (result: SearchResultItem) => void;
  searchParams: SearchParams;
}

/**
 * Componente para exibir resultados de busca na Bíblia
 * Mostra uma lista de versículos que correspondem à consulta de pesquisa
 */
export const SearchResults: React.FC<SearchResultsProps> = ({
  className = '',
  onResultClick,
  searchParams
}) => {
  const { useSearchQuery } = useBibleQuery();
  const { data: searchResults, isLoading: isSearching, error } = useSearchQuery(searchParams, {
    enabled: !!searchParams.query,
    queryKey: [BibleQueryKeys.SEARCH, searchParams]
  });

  const handleResultClick = (result: SearchResultItem) => {
    if (onResultClick) {
      onResultClick(result);
    }
  };

  // Destaca o termo de busca no texto do versículo
  const highlightSearchTerm = (text: string, searchTerm: string): JSX.Element => {
    if (!searchTerm) return <>{text}</>;
    
    try {
      const regex = new RegExp(`(${searchTerm})`, 'gi');
      const parts = text.split(regex);
      
      return (
        <>
          {parts.map((part, i) => 
            regex.test(part) ? 
              <span key={i} className="bg-yellow-200 font-medium">{part}</span> : 
              <span key={i}>{part}</span>
          )}
        </>
      );
    } catch (e) {
      // Em caso de erro na regex (ex: caracteres especiais), retorna o texto original
      return <>{text}</>;
    }
  };

  if (isSearching) {
    return (
      <div className={`p-4 ${className}`}>
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`p-4 ${className}`}>
        <div className="text-center py-8 text-red-500">
          <SearchX className="h-12 w-12 mx-auto mb-4 text-red-400" />
          <p>Erro ao realizar a busca: {error instanceof Error ? error.message : String(error)}</p>
        </div>
      </div>
    );
  }

  if (!searchResults?.items || searchResults.items.length === 0) {
    return (
      <div className={`p-4 ${className}`}>
        <div className="text-center py-8 text-gray-500">
          <SearchX className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <p>Nenhum resultado encontrado.</p>
          <p className="text-sm mt-2">Tente usar termos diferentes ou mais gerais.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 ${className}`}>
      <h3 className="text-lg font-semibold mb-4">
        {searchResults.items.length} {searchResults.items.length === 1 ? 'resultado' : 'resultados'} encontrados
      </h3>

      <div className="space-y-4">
        {searchResults.items.map((result, index) => (
          <div
            key={index}
            className="p-4 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer"
            onClick={() => handleResultClick(result)}
          >
            <div className="flex justify-between items-start">
              <h4 className="font-medium text-blue-600">
                {result.verse.book_name} {result.verse.chapter_number}:{result.verse.number}
              </h4>
              <ExternalLink className="h-4 w-4 text-gray-400" />
            </div>
            <p className="mt-2 text-gray-700">
              {highlightSearchTerm(result.verse.text, result.highlight)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults; 