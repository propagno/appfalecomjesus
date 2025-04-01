import React, { useState } from 'react';
import { useBibleContext } from '../contexts/BibleContext';
import { ArrowLeft, Share2, Volume2, Bookmark } from 'lucide-react';
import { Verse } from '../types';

interface BibleReaderProps {
  className?: string;
  onBack?: () => void;
}

/**
 * Componente para leitura da Bíblia
 * Exibe os versículos do capítulo selecionado
 */
export const BibleReader: React.FC<BibleReaderProps> = ({
  className = '',
  onBack,
}) => {
  const {
    selectedBook,
    selectedChapter,
    verses,
    isLoadingVerses,
  } = useBibleContext();

  const [highlightedVerses, setHighlightedVerses] = useState<number[]>([]);

  if (!selectedBook || !selectedChapter) {
    return null;
  }

  const handleBack = () => {
    if (onBack) {
      onBack();
    }
  };

  const toggleVerseHighlight = (verse: Verse) => {
    setHighlightedVerses((prev) => {
      if (prev.includes(verse.id)) {
        return prev.filter((id) => id !== verse.id);
      } else {
        return [...prev, verse.id];
      }
    });
  };

  const readVerseAloud = (verse: Verse) => {
    if ('speechSynthesis' in window) {
      const text = `Versículo ${verse.number}: ${verse.text}`;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'pt-BR';
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Seu navegador não suporta a funcionalidade de leitura em voz alta.');
    }
  };

  const shareVerse = (verse: Verse) => {
    const verseText = `${selectedBook.name} ${selectedChapter.number}:${verse.number} - "${verse.text}" #FaleComJesus`;
    
    if (navigator.share) {
      navigator.share({
        title: `${selectedBook.name} ${selectedChapter.number}:${verse.number}`,
        text: verseText,
      }).catch((error) => console.log('Erro ao compartilhar:', error));
    } else {
      // Fallback para navegadores que não suportam a Web Share API
      navigator.clipboard.writeText(verseText)
        .then(() => alert('Versículo copiado para a área de transferência!'))
        .catch((error) => console.log('Erro ao copiar:', error));
    }
  };

  const bookmarkVerse = (verse: Verse) => {
    // Aqui seria implementada a lógica para salvar o marcador
    // usando algum serviço ou estado global da aplicação
    alert(`Versículo ${verse.number} marcado como favorito!`);
  };

  if (isLoadingVerses) {
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
          aria-label="Voltar para seleção de capítulos"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h2 className="text-xl font-semibold">
          {selectedBook.name} {selectedChapter.number}
        </h2>
      </div>

      {/* Texto bíblico */}
      <div className="prose max-w-none">
        {verses.length > 0 ? (
          verses.map((verse) => (
            <div
              key={verse.id}
              className={`py-2 flex group ${
                highlightedVerses.includes(verse.id) ? 'bg-yellow-100' : ''
              }`}
              onClick={() => toggleVerseHighlight(verse)}
            >
              <span className="text-xs text-gray-500 w-7 pt-1 shrink-0">
                {verse.number}
              </span>
              <div className="flex-1">
                <p className="m-0 leading-relaxed text-base">
                  {verse.text}
                </p>
                
                {/* Ações de versículo */}
                <div className="mt-1 opacity-0 group-hover:opacity-100 transition-opacity flex space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      readVerseAloud(verse);
                    }}
                    className="p-1 text-gray-600 hover:text-blue-600 rounded-full hover:bg-gray-100"
                    title="Ouvir versículo"
                  >
                    <Volume2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      shareVerse(verse);
                    }}
                    className="p-1 text-gray-600 hover:text-blue-600 rounded-full hover:bg-gray-100"
                    title="Compartilhar versículo"
                  >
                    <Share2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      bookmarkVerse(verse);
                    }}
                    className="p-1 text-gray-600 hover:text-blue-600 rounded-full hover:bg-gray-100"
                    title="Marcar como favorito"
                  >
                    <Bookmark className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8 text-gray-500">
            Nenhum versículo disponível.
          </div>
        )}
      </div>
    </div>
  );
};

export default BibleReader; 