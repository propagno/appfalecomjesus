import React, { useState } from 'react';
import { Book } from '../types';
import { useBibleContext } from '../contexts/BibleContext';
import { Search } from 'lucide-react';

interface BookSelectorProps {
  className?: string;
}

/**
 * Componente para seleção de livros da Bíblia
 * Permite filtrar e selecionar um livro
 */
export const BookSelector: React.FC<BookSelectorProps> = ({ className = '' }) => {
  const { books, selectBook, selectedBook, isLoadingBooks } = useBibleContext();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTestament, setSelectedTestament] = useState<'all' | 'old' | 'new'>('all');

  // Filtra os livros baseado no termo de busca e testamento selecionado
  const filteredBooks = books.filter((book) => {
    const matchesSearch = book.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesTestament = selectedTestament === 'all' || book.testament === selectedTestament;
    return matchesSearch && matchesTestament;
  });

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleTestamentChange = (testament: 'all' | 'old' | 'new') => {
    setSelectedTestament(testament);
  };

  const handleSelectBook = (book: Book) => {
    selectBook(book);
  };

  if (isLoadingBooks) {
    return (
      <div className={`p-4 ${className}`}>
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 ${className}`}>
      {/* Barra de pesquisa */}
      <div className="relative mb-4">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Buscar livro..."
          className="pl-10 w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchTerm}
          onChange={handleSearch}
        />
      </div>

      {/* Filtro de testamento */}
      <div className="flex mb-4 space-x-2">
        <button
          className={`px-3 py-1 rounded-md text-sm ${
            selectedTestament === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
          onClick={() => handleTestamentChange('all')}
        >
          Todos
        </button>
        <button
          className={`px-3 py-1 rounded-md text-sm ${
            selectedTestament === 'old'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
          onClick={() => handleTestamentChange('old')}
        >
          Antigo Testamento
        </button>
        <button
          className={`px-3 py-1 rounded-md text-sm ${
            selectedTestament === 'new'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
          onClick={() => handleTestamentChange('new')}
        >
          Novo Testamento
        </button>
      </div>

      {/* Lista de livros */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
        {filteredBooks.map((book) => (
          <button
            key={book.id}
            className={`p-2 text-left rounded-md transition-colors ${
              selectedBook?.id === book.id
                ? 'bg-blue-100 border-blue-500 border'
                : 'hover:bg-gray-100 border border-transparent'
            }`}
            onClick={() => handleSelectBook(book)}
          >
            <div className="font-medium">{book.name}</div>
            <div className="text-xs text-gray-500">
              {book.testament === 'old' ? 'AT' : 'NT'} • {book.chapters_count} cap.
            </div>
          </button>
        ))}
      </div>

      {filteredBooks.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          Nenhum livro encontrado.
        </div>
      )}
    </div>
  );
};

export default BookSelector; 