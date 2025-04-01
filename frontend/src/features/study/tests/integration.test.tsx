/**
 * Testes de integração para o microsserviço MS-Study
 * Implementação do item 10.3.4 da migração
 */
import React from 'react';
import { renderHook, act } from '@testing-library/react-hooks';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import useStudyQuery from '../hooks/useStudyQuery';
import { API_URLS } from '../../../shared/constants/config';
import { AuthProvider } from '../../auth/contexts/AuthContext';
import { OnboardingPreferences, UserStudyProgress } from '../types';

// Mock do servidor para interceptar chamadas de API
const server = setupServer(
  // Mock da chamada para obter planos
  rest.get(`${API_URLS.study}/plans`, (req, res, ctx) => {
    return res(
      ctx.json({
        plans: [
          {
            id: 'plan1',
            title: 'Plano de Teste',
            description: 'Plano para testes',
            category: 'teste',
            difficulty: 'iniciante',
            duration_days: 7,
            created_at: new Date().toISOString(),
          },
        ],
        total: 1,
        page: 1,
        per_page: 10,
      })
    );
  }),

  // Mock da chamada para obter progresso do usuário
  rest.get(`${API_URLS.study}/progress`, (req, res, ctx) => {
    return res(
      ctx.json({
        progress: [
          {
            id: 'progress1',
            user_id: 'user1',
            study_plan_id: 'plan1',
            current_section_id: 'section1',
            completion_percentage: 50,
            started_at: new Date().toISOString(),
          },
        ],
      })
    );
  }),

  // Mock da chamada para iniciar um plano
  rest.post(`${API_URLS.study}/plans/:planId/start`, (req, res, ctx) => {
    return res(
      ctx.json({
        id: 'progress2',
        user_id: 'user1',
        study_plan_id: req.params.planId,
        current_section_id: 'section1',
        completion_percentage: 0,
        started_at: new Date().toISOString(),
      })
    );
  }),

  // Mock da chamada para atualizar progresso
  rest.post(`${API_URLS.study}/progress/update`, (req, res, ctx) => {
    const { plan_id, section_id, completion_percentage } = req.body as any;
    return res(
      ctx.json({
        id: 'progress1',
        user_id: 'user1',
        study_plan_id: plan_id,
        current_section_id: section_id,
        completion_percentage,
        started_at: new Date().toISOString(),
      })
    );
  }),

  // Mock da chamada para enviar preferências do onboarding
  rest.post(`${API_URLS.study}/init-plan`, (req, res, ctx) => {
    return res(
      ctx.json({
        suggestion: {
          title: 'Plano Personalizado',
          description: 'Plano criado com base nas suas preferências',
          duration_days: 7,
          sections: [
            {
              title: 'Introdução',
              content: 'Conteúdo introdutório',
              duration_minutes: 15,
            },
          ],
          justification: 'Este plano foi recomendado com base nas suas preferências',
        },
      })
    );
  }),

  // Mock para todas as outras requisições
  rest.all('*', (req, res, ctx) => {
    console.error(`Requisição não mockada: ${req.url.toString()}`);
    return res(ctx.status(404));
  })
);

// Wrapper do Provider para testes
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>{children}</AuthProvider>
    </QueryClientProvider>
  );
};

// Setup e teardown do servidor mock
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Spy no console.error para verificar erros
jest.spyOn(console, 'error').mockImplementation(() => {});

describe('Integração com MS-Study', () => {
  test('busca planos de estudo com sucesso', async () => {
    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Espera a query ser executada
    await waitFor(() => !result.current.isLoading);

    // Verifica se os planos foram carregados
    expect(result.current.plans).toHaveLength(1);
    expect(result.current.plans[0].title).toBe('Plano de Teste');
  });

  test('busca progresso do usuário com sucesso', async () => {
    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Espera a query ser executada
    await waitFor(() => !result.current.isLoading);

    // Verifica se o progresso foi carregado
    expect(result.current.userProgress).toHaveLength(1);
    expect(result.current.userProgress[0].completion_percentage).toBe(50);
  });

  test('inicia um plano com sucesso', async () => {
    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Espera a query ser executada
    await waitFor(() => !result.current.isLoading);

    // Inicia um plano
    await act(async () => {
      await result.current.startPlan('plan1');
    });

    // Verifica se o plano foi iniciado
    await waitFor(() => {
      expect(result.current.error).toBeNull();
    });
  });

  test('atualiza progresso com sucesso', async () => {
    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Espera a query ser executada
    await waitFor(() => !result.current.isLoading);

    // Atualiza o progresso
    await act(async () => {
      await result.current.updateProgress('plan1', 'section1', 75);
    });

    // Verifica se o progresso foi atualizado
    await waitFor(() => {
      expect(result.current.error).toBeNull();
    });
  });

  test('envia preferências do onboarding com sucesso', async () => {
    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Espera a query ser executada
    await waitFor(() => !result.current.isLoading);

    // Cria preferências de onboarding
    const preferences: OnboardingPreferences = {
      objectives: ['ansiedade', 'fé'],
      bible_experience_level: 'iniciante' as any,
      content_preferences: ['texto', 'áudio'] as any,
      preferred_time: 'manhã' as any,
    };

    // Envia preferências
    await act(async () => {
      await result.current.submitOnboarding(preferences);
    });

    // Verifica se as preferências foram processadas
    await waitFor(() => {
      expect(result.current.onboardingSuggestion).not.toBeNull();
      expect(result.current.onboardingSuggestion?.title).toBe('Plano Personalizado');
    });
  });

  test('simula comportamento offline', async () => {
    // Mock da API para simular erro de rede
    server.use(
      rest.get(`${API_URLS.study}/plans`, (req, res, ctx) => {
        return res.networkError('Failed to connect');
      })
    );

    const { result, waitFor } = renderHook(() => useStudyQuery(), { wrapper: TestWrapper });

    // Forçar estado offline
    Object.defineProperty(navigator, 'onLine', {
      value: false,
      writable: true,
    });

    // Dispara evento offline para que o hook detecte
    window.dispatchEvent(new Event('offline'));

    // Espera a query ser executada
    await waitFor(() => {
      expect(result.current.isOffline).toBe(true);
    });

    // Simular retorno da conexão
    Object.defineProperty(navigator, 'onLine', {
      value: true,
      writable: true,
    });

    // Dispara evento online para que o hook detecte
    window.dispatchEvent(new Event('online'));

    // Verifica se o estado offline foi atualizado
    await waitFor(() => {
      expect(result.current.isOffline).toBe(false);
    });
  });
});

// Função auxiliar para renderizar componentes com o QueryClient
export const renderWithClient = (ui: React.ReactElement, client?: QueryClient) => {
  const testClient = client || new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return (
    <QueryClientProvider client={testClient}>
      {ui}
    </QueryClientProvider>
  );
}; 