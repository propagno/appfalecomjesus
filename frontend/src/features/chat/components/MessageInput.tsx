import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

// Interfaces para o SpeechRecognition
interface SpeechRecognitionErrorEvent extends Event {
  error: string;
}

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: (event: SpeechRecognitionEvent) => void;
  onerror: (event: SpeechRecognitionErrorEvent) => void;
  onend: () => void;
  start: () => void;
  stop: () => void;
}

declare global {
  interface Window {
    SpeechRecognition: {
      new(): SpeechRecognition;
    };
    webkitSpeechRecognition: {
      new(): SpeechRecognition;
    };
  }
}

/**
 * Componente de input para envio de mensagens com suporte a voz
 */
export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  isLoading = false,
  placeholder = 'Digite sua mensagem...',
}) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Verificar se o navegador suporta reconhecimento de voz
  const isSupported = 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;

  // Variáveis para reconhecimento de voz
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Configurar o reconhecimento de voz
  useEffect(() => {
    if (isSupported) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'pt-BR';

      recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
        const transcript = Array.from(event.results)
          .map(result => result[0].transcript)
          .join('');
        setMessage(transcript);
      };

      recognitionRef.current.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('Erro no reconhecimento de voz:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, [isSupported]);

  // Ajustar altura do textarea conforme conteúdo
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  // Lidar com envio da mensagem
  const handleSendMessage = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  // Lidar com tecla Enter
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Alternar reconhecimento de voz
  const toggleListening = () => {
    if (!isSupported) return;

    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
    }
    setIsListening(!isListening);
  };

  return (
    <div className="flex items-end gap-2 p-4 bg-white border-t border-gray-200">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={isLoading}
          className="w-full p-3 pr-10 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none overflow-hidden"
          rows={1}
          style={{ minHeight: '44px', maxHeight: '120px' }}
        />
      </div>

      {isSupported && (
        <button
          onClick={toggleListening}
          disabled={isLoading}
          className={`p-3 rounded-lg transition-colors ${
            isListening
              ? 'bg-red-500 hover:bg-red-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
          }`}
          title={isListening ? 'Parar gravação' : 'Iniciar gravação de voz'}
        >
          {isListening ? <MicOff size={20} /> : <Mic size={20} />}
        </button>
      )}

      <button
        onClick={handleSendMessage}
        disabled={!message.trim() || isLoading}
        className={`p-3 rounded-lg transition-colors ${
          message.trim() && !isLoading
            ? 'bg-blue-500 hover:bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
        }`}
        title="Enviar mensagem"
      >
        <Send size={20} />
      </button>
    </div>
  );
};

export default MessageInput; 