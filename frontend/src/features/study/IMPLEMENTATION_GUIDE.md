# Implementação da Feature de Estudo

Esta documentação descreve a implementação da feature de Estudo, responsável pelo gerenciamento de planos de estudo personalizados, progresso do usuário, reflexões e certificados no sistema FaleComJesus.

## Estrutura da Feature

A estrutura da feature de Estudo segue o padrão organizacional do projeto:

```
src/features/study/
├── api/
│   └── studyService.ts          # Serviços para interação com a API
├── components/
│   ├── PlanCard.tsx             # Card para exibição de plano de estudo
│   ├── OnboardingForm.tsx       # Formulário de onboarding para coleta de preferências
│   └── ReflectionForm.tsx       # Formulário para registrar reflexões 
├── contexts/
│   └── StudyContext.tsx         # Contexto para compartilhar estado da feature
├── hooks/
│   └── useStudy.ts              # Hook central com lógica de negócio
├── pages/
│   ├── OnboardingPage.tsx       # Página de onboarding para novos usuários
│   └── StudyPlansPage.tsx       # Página de listagem de planos
├── types/
│   └── index.ts                 # Tipos e interfaces da feature
└── index.ts                     # Exportações principais da feature
```

## Tipos Principais

Os tipos principais da feature são definidos em `types/index.ts`:

- `StudyPlan`: Representa um plano de estudo completo
- `StudySection`: Representa uma seção/dia de um plano
- `StudyContent`: Conteúdo específico de uma seção
- `UserStudyProgress`: Progresso do usuário em um plano
- `Reflection`: Reflexão do usuário sobre uma seção
- `Certificate`: Certificado de conclusão de um plano
- `OnboardingPreferences`: Preferências do usuário coletadas no onboarding
- `AIStudyPlanSuggestion`: Sugestão de plano gerada pela IA

## Serviço de API

O `studyService.ts` contém todos os métodos para comunicação com o backend:

- Obtenção de planos, seções e conteúdos
- Gerenciamento de progresso do usuário
- Criação e recuperação de reflexões
- Geração e download de certificados
- Envio de preferências para geração de plano personalizado pela IA

## Gerenciamento de Estado

O estado é gerenciado através do hook `useStudy` e compartilhado pela aplicação através do `StudyContext`. 

### Hook useStudy

O hook `useStudy` utiliza React Query para:

- Buscar dados (planos, progresso, certificados) 
- Gerenciar mutações (iniciar plano, atualizar progresso, criar reflexão)
- Manter estado local (plano selecionado, filtros)

### Contexto StudyContext

O `StudyContext` torna o estado disponível globalmente para outros componentes, facilitando o acesso a:

- Dados carregados da API
- Estados de loading e erros
- Funções para interagir com a API

## Fluxos Principais

### 1. Onboarding e Geração de Plano Personalizado

O fluxo de onboarding consiste em:

1. Usuário preenche formulário multi-etapas no `OnboardingForm` 
2. As preferências são enviadas para o backend via `submitOnboardingPreferences`
3. A IA gera uma sugestão de plano personalizado
4. O usuário revisa a sugestão na `OnboardingPage`
5. Ao confirmar, o plano é criado via `createPersonalizedPlan`

### 2. Exploração e Filtro de Planos

Na página `StudyPlansPage`, o usuário pode:

1. Visualizar planos disponíveis como cards (`PlanCard`)
2. Filtrar por categoria, dificuldade ou busca textual
3. Ver seu progresso em planos já iniciados
4. Iniciar novos planos ou continuar planos em andamento

### 3. Acompanhamento de Progresso e Reflexões

Durante o estudo de um plano:

1. O usuário visualiza o conteúdo da seção atual
2. Registra reflexões através do `ReflectionForm`
3. Marca a seção como concluída, atualizando o progresso
4. Ao completar todas as seções, recebe um certificado

## Integração com Outras Features

Esta feature se integra com:

- **Autenticação**: Para verificar permissões e acessar dados do usuário
- **Chat IA**: Para fornecer ajuda contextual durante o estudo
- **Bíblia**: Para referenciar e exibir versículos relevantes

## Páginas Implementadas

1. **OnboardingPage**: Coleta preferências do usuário e gera plano personalizado
2. **StudyPlansPage**: Lista todos os planos disponíveis com filtros

## Próximos Passos

Para completar a feature, é necessário implementar:

1. Página detalhada do plano (`StudyPlanPage`)
2. Página da sessão de estudo (`StudySectionPage`) 
3. Listagem de reflexões (`ReflectionsPage`)
4. Visualização e download de certificados (`CertificatesPage`)

## Considerações Técnicas

- Os dados são otimizados com caching via React Query
- Formulários possuem validação e feedback visual 
- Ações assíncronas mostram estados de loading
- Componentes são estilizados com Tailwind CSS 

# Guia de Implementação - MS-Study com React Query

Este documento serve como um guia para os desenvolvedores que precisam trabalhar com a funcionalidade de estudos, explicando como usar a infraestrutura de cache, offline e integração com React Query.

## 1. Contexto

A versão anterior do módulo de estudos usava um serviço Mock, agora migramos para uma implementação real usando React Query para comunicação com o MS-Study.

## 2. Como Usar em Componentes React

A maneira mais simples de acessar os dados e funcionalidades é usando o hook `useStudyContext`:

```tsx
import { useStudyContext } from '../features/study/contexts/StudyContext';

export const MyComponent = () => {
  const { 
    plans, 
    userProgress, 
    isLoading, 
    error, 
    startPlan,
    updateProgress,
    isOffline 
  } = useStudyContext();

  // Agora você pode usar os dados e funções
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  
  return (
    <div>
      {isOffline && <OfflineBanner />}
      
      <h1>Seus planos de estudo</h1>
      <ul>
        {plans.map(plan => (
          <li key={plan.id}>
            {plan.title}
            <button onClick={() => startPlan(plan.id)}>
              Iniciar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};
```

## 3. Acesso Direto às Queries e Mutations

Se você precisa de mais controle, pode usar diretamente o hook `useStudyQuery`:

```tsx
import useStudyQuery from '../features/study/hooks/useStudyQuery';

export const AdvancedComponent = () => {
  const {
    plans,
    isLoading,
    error,
    startPlan,
    // ... outros dados e funções
  } = useStudyQuery();
  
  // Implementação personalizada
};
```

## 4. Lidando com Modo Offline

A implementação detecta automaticamente quando a aplicação está offline e armazena dados relevantes no localStorage. Para verificar se o usuário está offline:

```tsx
const { isOffline } = useStudyContext();

// Renderizar interface adaptada para offline
if (isOffline) {
  return <OfflineView />; 
}
```

Quando o usuário voltar a ficar online, a sincronização acontecerá automaticamente.

## 5. Lidando com Limitações do Plano Free

Para verificar se o usuário atingiu o limite do plano Free:

```tsx
const { checkFreePlanLimitations } = useStudyContext();

const handleStartPlan = async (planId: string) => {
  const canProceed = await checkFreePlanLimitations();
  
  if (canProceed) {
    // Usuário pode prosseguir
    startPlan(planId);
  } else {
    // Exibir modal de upgrade
    showUpgradeModal();
  }
};
```

## 6. Gestão do Cache

O React Query gerencia automaticamente o cache, mas às vezes você pode precisar invalidar manualmente:

```tsx
import { useQueryClient } from '@tanstack/react-query';
import { QUERY_KEYS } from '../features/study/constants';

export const AdminComponent = () => {
  const queryClient = useQueryClient();
  
  const handleForceRefresh = () => {
    // Invalidar cache de planos
    queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PLANS] });
    
    // Invalidar cache de progresso
    queryClient.invalidateQueries({ queryKey: [QUERY_KEYS.PROGRESS] });
  };
  
  // restante do componente
};
```

## 7. Gerenciamento de Estado Local vs Global

- Use o contexto (`useStudyContext`) para dados e ações que precisam ser compartilhados entre múltiplos componentes.
- Use o `useState` local para estado de UI específico do componente (como modal aberto/fechado).
- Os dados críticos do MS-Study já são armazenados automaticamente no localStorage para suporte offline.

## 8. Tempos de Cache e Stale

Os tempos definidos para cada tipo de dado são:

- Planos: stale após 5 minutos, cache por 1 hora
- Progresso: stale após 1 minuto, cache por 30 minutos
- Conteúdo: stale após 10 minutos, cache por 24 horas
- Reflexões: stale após 2 minutos, cache por 1 hora

Se precisar modificar esses valores, edite o arquivo `frontend/src/features/study/constants.ts`.

## 9. Handling API Errors

Os erros são tratados automaticamente e armazenados na propriedade `error` do contexto:

```tsx
const { error } = useStudyContext();

if (error) {
  return (
    <ErrorView 
      message={error.message}
      retry={() => window.location.reload()}
    />
  );
}
```

## 10. Depuração e Ferramentas

Durante o desenvolvimento, você pode usar o React Query Devtools para inspecionar o cache:

```tsx
// Já configurado no AppProviders, ativo apenas em ambiente de desenvolvimento
```

O DevTools aparece no canto inferior direito da aplicação em ambiente de desenvolvimento.

---

Para mais detalhes sobre a implementação, consulte `frontend/src/features/study/README.md` ou entre em contato com a equipe de desenvolvimento. 