import React, { useState } from 'react';

interface ReflectionFormProps {
  sectionId: string;
  sectionTitle: string;
  onSave: (sectionId: string, reflectionText: string) => Promise<void>;
  initialValue?: string;
  isLoading?: boolean;
}

/**
 * Componente para registrar reflexões do usuário sobre um estudo
 */
const ReflectionForm: React.FC<ReflectionFormProps> = ({
  sectionId,
  sectionTitle,
  onSave,
  initialValue = '',
  isLoading = false
}) => {
  const [reflectionText, setReflectionText] = useState(initialValue);
  const [charCount, setCharCount] = useState(initialValue.length);
  const MAX_CHARS = 2000;

  // Manipulador de alteração do texto
  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    
    if (newText.length <= MAX_CHARS) {
      setReflectionText(newText);
      setCharCount(newText.length);
    }
  };

  // Manipulador de envio do formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (reflectionText.trim().length === 0) {
      return;
    }
    
    try {
      await onSave(sectionId, reflectionText);
      // Não limpar o texto após salvar para permitir edições futuras
    } catch (error) {
      console.error('Erro ao salvar reflexão:', error);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Sua reflexão sobre {sectionTitle}
      </h3>
      
      <p className="text-sm text-gray-600 mb-4">
        Registre seus pensamentos, insights e aplicações pessoais sobre este estudo.
        Essas reflexões ficarão salvas em seu perfil para consulta futura.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <textarea
            value={reflectionText}
            onChange={handleTextChange}
            placeholder="Escreva sua reflexão aqui..."
            className="w-full p-3 border border-gray-300 rounded-md min-h-[120px] focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={isLoading}
          />
          
          <div className="flex justify-end mt-1">
            <span className={`text-xs ${charCount > MAX_CHARS * 0.9 ? 'text-red-500' : 'text-gray-500'}`}>
              {charCount}/{MAX_CHARS} caracteres
            </span>
          </div>
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isLoading || reflectionText.trim().length === 0}
            className={`
              py-2 px-4 rounded-md text-white flex items-center
              ${isLoading || reflectionText.trim().length === 0
                ? 'bg-gray-300 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700'}
            `}
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Salvando...
              </>
            ) : (
              'Salvar reflexão'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReflectionForm; 