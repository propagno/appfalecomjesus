import React, { ReactNode, useState, useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ENV, FEATURES } from '../shared/constants/config';
import { AuthProvider } from '../features/auth/contexts/AuthContext';
import { StudyProvider } from '../features/study/contexts/StudyContext';
import { BibleProvider } from '../features/bible/contexts/BibleContext';
import { ChatProvider } from '../features/chat/contexts/ChatContext';
import { GamificationProvider } from '../features/gamification/contexts/GamificationContext';
import { MonetizationProvider } from '../features/monetization';

// Configurações do QueryClient para diferentes tipos de dados
const defaultQueryConfig = {
  queries: {
    // Configuração padrão para todas as queries
    staleTime: 1000 * 60 * 5, // 5 minutos
    cacheTime: 1000 * 60 * 30, // 30 minutos
    refetchOnWindowFocus: ENV.isDevelopment ? false : true,
    refetchOnReconnect: true,
    retry: 1,
    retryDelay: (attemptIndex: number) => Math.min(1000 * 2 ** attemptIndex, 30000),
  },
  mutations: {
    // Configuração padrão para todas as mutations
    retry: 0,
    onError: (err: unknown) => {
      console.error('Mutation error:', err);
    },
  },
};

/**
 * Hook para criar uma instância do QueryClient com configurações otimizadas
 */
export const createQueryClient = () => {
  return new QueryClient({
    defaultOptions: defaultQueryConfig,
  });
};

// Criação do QueryClient
const queryClient = createQueryClient();

// Componente para lidar com erros em providers
const ErrorBoundaryProvider: React.FC<{
  fallback: React.ReactNode;
  children: React.ReactNode;
  name: string;
}> = ({ fallback, children, name }) => {
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const handleError = (error: ErrorEvent) => {
      console.error(`Erro no provider ${name}:`, error);
      setHasError(true);
    };

    window.addEventListener('error', handleError);
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, [name]);

  if (hasError) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
};

interface AppProvidersProps {
  children: ReactNode;
}

/**
 * Componente que configura todos os providers da aplicação
 */
export const AppProviders: React.FC<AppProvidersProps> = ({ children }) => {
  // Fallback para exibir quando um provider falha
  const providerFallback = (
    <div style={{ padding: '20px', color: 'red', textAlign: 'center' }}>
      <h2>Erro ao carregar a aplicação</h2>
      <p>Não foi possível inicializar um ou mais providers.</p>
      <p>Verifique o console para mais detalhes.</p>
    </div>
  );

  return (
    <ErrorBoundaryProvider name="QueryClientProvider" fallback={providerFallback}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <ErrorBoundaryProvider name="AuthProvider" fallback={providerFallback}>
            <AuthProvider>
              <ErrorBoundaryProvider name="StudyProvider" fallback={providerFallback}>
                <StudyProvider>
                  <ErrorBoundaryProvider name="BibleProvider" fallback={providerFallback}>
                    <BibleProvider>
                      <ErrorBoundaryProvider name="ChatProvider" fallback={providerFallback}>
                        <ChatProvider>
                          <ErrorBoundaryProvider name="GamificationProvider" fallback={providerFallback}>
                            <GamificationProvider>
                              <ErrorBoundaryProvider name="MonetizationProvider" fallback={providerFallback}>
                                <MonetizationProvider>
                                  {children}
                                </MonetizationProvider>
                              </ErrorBoundaryProvider>
                            </GamificationProvider>
                          </ErrorBoundaryProvider>
                        </ChatProvider>
                      </ErrorBoundaryProvider>
                    </BibleProvider>
                  </ErrorBoundaryProvider>
                </StudyProvider>
              </ErrorBoundaryProvider>
            </AuthProvider>
          </ErrorBoundaryProvider>
        </BrowserRouter>
        {/* Mostra as devtools apenas em ambiente de desenvolvimento */}
        {ENV.isDevelopment && <ReactQueryDevtools initialIsOpen={false} position="bottom" />}
      </QueryClientProvider>
    </ErrorBoundaryProvider>
  );
};

export default AppProviders; 