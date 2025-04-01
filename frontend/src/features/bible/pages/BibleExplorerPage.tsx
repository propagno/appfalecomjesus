import React, { useState, useEffect } from 'react';
import { useBibleContext } from '../contexts/BibleContext';
import BookSelector from '../components/BookSelector';
import ChapterSelector from '../components/ChapterSelector';
import BibleReader from '../components/BibleReader';
import { Search, Book, History } from 'lucide-react';
import { Link } from 'react-router-dom';

/**
 * Página principal do explorador de Bíblia
 * Permite navegar pelos livros, capítulos e versículos da Bíblia
 */
export const BibleExplorerPage: React.FC = () => {
  const { selectedBook, selectedChapter, clearSelection, loadBooks } = useBibleContext();
  const [view, setView] = useState<'books' | 'chapters' | 'verses'>('books');

  // Carregar os livros da bíblia apenas quando a página for aberta
  useEffect(() => {
    loadBooks();
  }, [loadBooks]);

  // Determina a visão atual com base na seleção
  useEffect(() => {
    if (selectedChapter) {
      setView('verses');
    } else if (selectedBook) {
      setView('chapters');
    } else {
      setView('books');
    }
  }, [selectedBook, selectedChapter]);

  const handleBackToBooks = () => {
    clearSelection();
    setView('books');
  };

  const handleBackToChapters = () => {
    // Remove apenas a seleção do capítulo
    setView('chapters');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Cabeçalho da página */}
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-blue-600">Bíblia Sagrada</h1>
          <p className="text-gray-600 mt-2">
            Explore livros, capítulos e versículos da Palavra de Deus
          </p>
        </header>

        {/* Barra de navegação */}
        <div className="bg-white shadow rounded-lg mb-6">
          <div className="flex p-2">
            <Link 
              to="/bible/search" 
              className="flex items-center justify-center px-4 py-2 rounded-md hover:bg-gray-100"
            >
              <Search className="h-5 w-5 mr-2 text-blue-500" />
              <span>Pesquisar</span>
            </Link>
            
            <button 
              className={`flex items-center justify-center px-4 py-2 rounded-md ${
                view === 'books' ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'
              }`}
              onClick={handleBackToBooks}
            >
              <Book className="h-5 w-5 mr-2 text-blue-500" />
              <span>Livros</span>
            </button>
            
            <button 
              className="flex items-center justify-center px-4 py-2 rounded-md hover:bg-gray-100 ml-auto"
              onClick={() => {}} // Função para exibir histórico de leitura (a implementar)
            >
              <History className="h-5 w-5 mr-2 text-blue-500" />
              <span>Histórico</span>
            </button>
          </div>
        </div>

        {/* Conteúdo principal */}
        <div className="bg-white shadow rounded-lg">
          {view === 'books' && (
            <BookSelector />
          )}

          {view === 'chapters' && selectedBook && (
            <ChapterSelector onBack={handleBackToBooks} />
          )}

          {view === 'verses' && selectedBook && selectedChapter && (
            <BibleReader onBack={handleBackToChapters} />
          )}
        </div>

        {/* Informações adicionais */}
        <div className="mt-6 text-center text-gray-500 text-sm">
          <p>Versão NVI - Nova Versão Internacional</p>
          <p className="mt-1">
            Use esta Bíblia para estudar, meditar e compartilhar a Palavra de Deus.
          </p>
        </div>
      </div>
    </div>
  );
};

export default BibleExplorerPage; 