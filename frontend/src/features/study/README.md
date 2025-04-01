# Feature Study - Integração com MS-Study

Esta documentação descreve a implementação da integração do frontend com o microsserviço MS-Study, usando React Query para gerenciamento de estado, cache e suporte offline.

## Arquitetura

A feature Study foi migrada da arquitetura anterior (com mocks e dados simulados) para uma integração completa com o backend seguindo princípios de Clean Architecture:

```
feature/study/
│
├── api/              # Camada de serviço para comunicação com o backend
│   └── studyService.ts  # Implementa as chamadas HTTP para o MS-Study
│
├── hooks/            # Hooks customizados para lógica de negócios
│   ├── useStudyCache.ts  # Hook para gerenciamento de cache específico
│   └── useStudyQuery.ts  # Hook principal com React Query
│
├── contexts/         # Contextos React para compartilhamento de estado
│   └── StudyContext.tsx  # Context Provider usando React Query
│
├── components/       # Componentes de UI específicos da feature
│
├── types/            # Tipos e interfaces TypeScript
│   └── index.ts      # Definições de tipos para planos, seções, etc.
│
└── pages/            # Páginas da feature
```

## React Query e Caching

### 1. Estrutura de Cache

Utilizamos React Query para gerenciar o cache dos dados com as seguintes chaves:

```typescript
const QUERY_KEYS = {
  plans: 'study-plans',
  plan: 'study-plan',
  sections: 'study-sections',
  content: 'study-content',
  progress: 'study-progress',
  reflections: 'study-reflections',
  currentStudy: 'current-study',
};
```

### 2. Tempos de Cache

- **Planos de estudo**: 5 minutos de staleTime
- **Progresso do usuário**: 1 minuto de staleTime
- **Conteúdo de seções**: 30 minutos de cacheTime com armazenamento local

### 3. Prefetch de Dados

Implementamos prefetch automático de seções subsequentes para melhorar a experiência do usuário:

```typescript
// Pré-carrega a próxima seção quando o usuário está quase terminando a atual
const prefetchNextSections = useCallback((planId: string, currentPosition: number) => {
  // Lógica de prefetch
}, []);
```

## Suporte Offline

### 1. Detecção de Status Online/Offline

```typescript
// Detecta se estamos offline e sincroniza quando retornar online
useEffect(() => {
  const handleOnline = () => setOfflineMode(false);
  const handleOffline = () => setOfflineMode(true);
  
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
}, []);
```

### 2. Armazenamento Local

Salvamos dados críticos localmente quando o usuário está offline:

```typescript
// Salva progresso localmente para sincronização posterior
const saveProgressLocally = useCallback((planId: string, sectionId: string, percentage: number) => {
  saveToCache(`offline_progress:${planId}`, { sectionId, percentage, timestamp: Date.now() });
}, []);
```

### 3. Sincronização

```typescript
// Sincroniza alterações feitas offline quando o usuário fica online novamente
const syncOfflineChanges = useCallback(async () => {
  const offlineChanges = await getFromCache("offline_changes_flag");
  if (offlineChanges) {
    // Lógica de sincronização
  }
}, []);
```

## Integração com Limitações do Plano Free

Foi implementada verificação de limitações do plano gratuito:

```typescript
// Verifica se o usuário atingiu o limite do plano Free (10 dias/mês)
const checkFreePlanLimitations = useCallback(async (): Promise<boolean> => {
  if (user?.role === 'premium') {
    return true; // Sem limitações para usuários premium
  }
  
  // Verificação com o MS-Monetization
}, [user?.role]);
```

## Como Usar

### Dentro de Componentes React

```tsx
import { useStudyContext } from '../contexts/StudyContext';

function StudyComponent() {
  const { 
    plans, 
    isLoading, 
    fetchPlanDetails, 
    updateProgress,
    isOffline 
  } = useStudyContext();
  
  // Seu componente aqui
}
```

### Acesso a Funções de Cache

```tsx
import useStudyCache from '../hooks/useStudyCache';

function CacheComponent() {
  const { 
    prefetchNextSections,
    invalidateProgressCache
  } = useStudyCache();
  
  // Invalidar cache após alguma ação
  const handleComplete = () => {
    // Ação aqui
    invalidateProgressCache();
  };
}
```

## Decisões Técnicas

1. **Separação de Hooks**: Criamos hooks separados para cache e para queries para melhor separação de responsabilidades.

2. **Interface Consistente**: Mantivemos a mesma interface do contexto original para evitar mudanças nos componentes existentes.

3. **Otimização de Stale Times**: Diferentes tempos de stale e cache baseados na natureza dos dados:
   - Dados mais estáticos (planos) → Cache mais longo
   - Dados de usuário (progresso) → Cache mais curto

4. **Estratégia Offline-First**: Permite uso mesmo sem conexão com sincronização posterior.

## Testes

Implementação testada com os seguintes cenários:

1. Carregamento inicial de planos
2. Navegação entre seções com prefetch
3. Funcionamento offline e sincronização posterior
4. Verificação de limites do plano Free 