import React from 'react';
import { useBibleContext } from '../contexts/BibleContext';
import { ArrowLeft } from 'lucide-react';

interface ChapterSelectorProps {
  className?: string;
  onBack?: () => void;
}

/**
 * Componente para seleção de capítulos da Bíblia
 * Exibe uma grade com os capítulos disponíveis para o livro selecionado
 */
export const ChapterSelector: React.FC<ChapterSelectorProps> = ({ 
  className = '',
  onBack
}) => {
  const { 
    selectedBook, 
    chapters, 
    selectChapter, 
    selectedChapter,
    isLoadingChapters 
  } = useBibleContext();

  if (!selectedBook) {
    return null;
  }

  const handleBack = () => {
    if (onBack) {
      onBack();
    }
  };

  if (isLoadingChapters) {
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
      {/* Cabeçalho */}
      <div className="flex items-center mb-6">
        <button 
          onClick={handleBack}
          className="mr-2 p-1 rounded-full hover:bg-gray-200"
          aria-label="Voltar para seleção de livros"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h2 className="text-xl font-semibold">{selectedBook.name}</h2>
      </div>

      {/* Grade de capítulos */}
      <div className="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
        {chapters.map((chapter) => (
          <button
            key={chapter.id}
            className={`p-3 rounded-md flex items-center justify-center transition-colors ${
              selectedChapter?.id === chapter.id
                ? 'bg-blue-600 text-white'
                : 'hover:bg-gray-100 border border-gray-300'
            }`}
            onClick={() => selectChapter(chapter)}
            aria-label={`Capítulo ${chapter.number}`}
          >
            <span className="font-medium">{chapter.number}</span>
          </button>
        ))}
      </div>

      {chapters.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          Nenhum capítulo disponível.
        </div>
      )}
    </div>
  );
};

export default ChapterSelector; 