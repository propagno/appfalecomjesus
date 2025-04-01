import React, { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../features/auth/contexts/AuthContext';
import { BibleProvider } from '../../features/bible/contexts/BibleContext';
import { ChatProvider } from '../../features/chat/contexts/ChatContext';
import { StudyProvider } from '../../features/study/contexts/StudyContext';
import { Toaster } from 'react-hot-toast';
import { GamificationProvider } from '../../features/gamification';
import { MonetizationProvider } from '../../features/monetization';

// Configuração do cliente de query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

interface AppProvidersProps {
  children: ReactNode;
}

/**
 * Componente que agrupa todos os providers da aplicação
 * Providers são aninhados na ordem em que dependem um do outro
 */
export const AppProviders: React.FC<AppProvidersProps> = ({ children }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <BibleProvider>
            <ChatProvider>
              <StudyProvider>
                <GamificationProvider>
                  <MonetizationProvider>
                    <>
                      {/* Adicionar outros providers aqui */}
                      {children}
                      <Toaster 
                        position="top-right" 
                        toastOptions={{
                          duration: 4000,
                          style: {
                            background: '#fff',
                            color: '#333',
                          },
                          success: {
                            iconTheme: {
                              primary: '#38a169',
                              secondary: '#fff',
                            },
                          },
                          error: {
                            iconTheme: {
                              primary: '#e53e3e',
                              secondary: '#fff',
                            },
                          },
                        }} 
                      />
                    </>
                  </MonetizationProvider>
                </GamificationProvider>
              </StudyProvider>
            </ChatProvider>
          </BibleProvider>
        </AuthProvider>
      </BrowserRouter>
      
      {/* DevTools do React Query (apenas em desenvolvimento) */}
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
};

export default AppProviders; 