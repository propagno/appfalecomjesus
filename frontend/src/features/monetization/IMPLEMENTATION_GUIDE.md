# Guia de Implementação - Funcionalidade de Monetização

Este documento descreve a implementação da funcionalidade de Monetização no aplicativo FaleComJesus, detalhando a estrutura de arquivos, tipos, API, hooks, contextos, componentes e fluxos principais.

## Estrutura de Arquivos

```
src/features/monetization/
├── api/
│   └── monetizationService.ts    # Serviços de API para monetização
├── components/
│   ├── AdRewardModal.tsx         # Modal para assistir anúncios
│   ├── PlanCard.tsx              # Card de plano de assinatura
│   ├── SubscriptionInfo.tsx      # Informações da assinatura atual
│   └── UsageLimits.tsx           # Exibição de limites de uso
├── contexts/
│   └── MonetizationContext.tsx   # Contexto para compartilhar estado
├── hooks/
│   └── useMonetization.ts        # Hook para gerenciar estado
├── pages/
│   └── MonetizationPage.tsx      # Página principal de monetização
├── types/
│   └── index.ts                  # Definições de tipos
└── index.ts                      # Arquivo barrel para exportações
```

## Tipos e Interfaces

A feature utiliza os seguintes tipos principais, definidos em `types/index.ts`:

- `Plan`: Representa um plano de assinatura e seus limites
- `Subscription`: Detalhes da assinatura atual do usuário
- `AdReward`: Recompensa por assistir anúncios
- `MonetizationLimits`: Limites de uso atuais para chat e estudos
- `PaymentIntent`: Resposta de inicialização de pagamento

## API Service

O arquivo `api/monetizationService.ts` inclui métodos para interagir com o backend:

- `getPlans`: Obtém planos disponíveis
- `getSubscription`: Obtém detalhes da assinatura atual
- `checkLimits`: Verifica limites de uso do usuário
- `registerAdReward`: Registra recompensa após assistir anúncio
- `upgradePlan`: Inicia processo de upgrade para plano premium
- `cancelSubscription`: Cancela assinatura atual

## State Management

### Hook `useMonetization`

O hook `useMonetization` gerencia o estado da monetização usando React Query:

- Carrega planos disponíveis
- Carrega detalhes da assinatura atual
- Gerencia limites de uso
- Fornece métodos para iniciar upgrades, cancelar assinaturas e assistir anúncios

### Contexto `MonetizationContext`

O contexto fornece acesso global ao estado de monetização e métodos:

- Estado: planos, assinatura atual, limites, etc.
- Métodos: upgradePlan, cancelSubscription, watchAd
- Flags úteis: isFreePlan, isPremium

## Componentes de UI

### `PlanCard`

Exibe um plano de assinatura com:
- Nome e preço
- Lista de recursos incluídos
- Botão para upgrade
- Marcação se é o plano atual

### `SubscriptionInfo`

Exibe detalhes da assinatura atual:
- Tipo de plano
- Status (ativo, cancelado, etc.)
- Data de início e expiração
- Opção para cancelar assinatura

### `UsageLimits`

Exibe os limites atuais de uso:
- Limite de mensagens no chat
- Limite de dias de estudo
- Barras de progresso visual
- Botões para assistir anúncios e ganhar mais recursos

### `AdRewardModal`

Modal para assistir anúncios:
- Simulação de player de vídeo
- Temporizador de contagem regressiva
- Recompensa após conclusão

## Página Principal

`MonetizationPage` contém:
- Abas para navegação entre:
  - Assinatura atual
  - Planos disponíveis
  - Limites de uso
- Informações contextuais e call-to-actions

## Fluxos Principais

1. **Visualização de Planos**:
   - Usuário navega para a aba de planos
   - Visualiza opções disponíveis
   - Clica em "Assinar" para um plano escolhido

2. **Upgrade para Premium**:
   - Ao clicar em upgrade, front-end inicia processo de pagamento
   - Redirecionamento para página de checkout (Stripe/Hotmart)
   - Após conclusão, status é verificado e assinatura atualizada

3. **Obtenção de Recompensas por Anúncios**:
   - Usuário do plano Free atinge limite de uso
   - Clica em assistir anúncio para ganhar mais recursos
   - Assiste vídeo simulado (seria um Ad real no ambiente de produção)
   - Após conclusão, ganha recompensa (mensagens ou dias de estudo)

4. **Cancelamento de Assinatura**:
   - Usuário navega para tela de assinatura
   - Clica em "Cancelar assinatura"
   - Confirma decisão
   - Assinatura é marcada como cancelada mas permanece ativa até data de expiração

## Integração com Outras Features

- **Auth**: Verifica identidade do usuário para operações sensíveis
- **Chat**: Utiliza os limites de mensagens para controle de acesso
- **Study**: Utiliza os limites de dias de estudo para controle de acesso
- **Gamification**: Pode conceder pontos por assistir anúncios (integração futura)

## Próximos Passos

- Integração real com gateways de pagamento (Stripe/Hotmart)
- Integração real com plataformas de anúncios (AdMob, Google Ads)
- Implementação de webhooks para notificações de pagamento
- Expansão de planos e opções de assinatura 