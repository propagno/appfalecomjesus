import React, { Component, ErrorInfo, ReactNode } from 'react';
import { errorHandler } from '../utils/errorHandler';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * Componente que captura erros não tratados nas árvores de componentes abaixo
 * Evita que erros de um componente derrubem toda a aplicação
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
    };
  }

  /**
   * Atualiza o estado quando um erro é capturado
   */
  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    };
  }

  /**
   * Registra o erro capturado
   */
  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Registra o erro usando o errorHandler atualizado
    errorHandler.handleError(error, {
      source: 'ErrorBoundary',
      component: errorInfo.componentStack
    }, {
      showNotification: false, // Não dispara notificações, pois já estamos mostrando o fallback
    });
    
    console.error('Erro capturado pelo ErrorBoundary:', error);
    console.error('Informações do componente:', errorInfo);
  }

  /**
   * Tenta recuperar a aplicação
   */
  handleReset = (): void => {
    this.setState({
      hasError: false,
      error: null,
    });
  };

  render(): ReactNode {
    const { children, fallback } = this.props;
    const { hasError, error } = this.state;

    if (hasError) {
      // Componente de fallback personalizado
      if (fallback) {
        return fallback;
      }

      // Fallback padrão
      return (
        <div className="error-boundary">
          <div className="error-container">
            <h2>Ops! Algo deu errado</h2>
            <p>Ocorreu um erro inesperado na aplicação.</p>
            {error && (
              <details className="error-details">
                <summary>Detalhes do erro</summary>
                <p>{error.toString()}</p>
              </details>
            )}
            <div className="error-actions">
              <button onClick={this.handleReset}>Tentar novamente</button>
              <button onClick={() => window.location.reload()}>
                Recarregar página
              </button>
            </div>
          </div>
        </div>
      );
    }

    return children;
  }
}

export default ErrorBoundary; 