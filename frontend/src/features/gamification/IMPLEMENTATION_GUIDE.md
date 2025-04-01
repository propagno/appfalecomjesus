# Guia de Implementação - Funcionalidade de Gamificação

Este documento descreve a implementação da funcionalidade de Gamificação no aplicativo FaleComJesus, detalhando a estrutura de arquivos, tipos, API, hooks, contextos, componentes, fluxos principais e integrações com outras funcionalidades.

## Estrutura de Arquivos

```
src/features/gamification/
├── api/
│   └── gamificationService.ts    # Serviços de API para gamificação
├── components/
│   ├── AchievementCard.tsx       # Card de conquista individual
│   ├── AchievementsList.tsx      # Lista de conquistas
│   ├── NewAchievementModal.tsx   # Modal para novas conquistas
│   └── PointsCard.tsx            # Card de pontos do usuário
├── contexts/
│   └── GamificationContext.tsx   # Contexto para compartilhar estado
├── hooks/
│   └── useGamification.ts        # Hook para gerenciar estado
├── pages/
│   └── GamificationPage.tsx      # Página principal de gamificação
├── types/
│   └── index.ts                  # Definições de tipos
└── index.ts                      # Arquivo barrel para exportações
```

## Tipos e Interfaces

A feature utiliza os seguintes tipos principais, definidos em `types/index.ts`:

- `UserPoints`: Pontos do usuário, nível atual e próximo
- `UserAchievement`: Conquista desbloqueada pelo usuário
- `Badge`: Conquista que pode ser desbloqueada
- `GamificationState`: Estado do sistema de gamificação
- `AchievementCategory`: Categorias de conquistas

## API Service

O arquivo `api/gamificationService.ts` inclui métodos para interagir com o backend:

- `getUserPoints`: Obter pontos e nível do usuário
- `getAchievements`: Obter conquistas desbloqueadas
- `getAvailableBadges`: Obter conquistas disponíveis
- `shareAchievement`: Compartilhar conquista nas redes sociais

## State Management

### Hook `useGamification`

O hook `useGamification` gerencia o estado da gamificação usando React Query:

- Carrega pontos do usuário
- Carrega conquistas e badges disponíveis
- Gerencia notificações de novas conquistas
- Fornece métodos para compartilhamento social

### Contexto `GamificationContext`

O contexto fornece acesso global ao estado de gamificação e métodos:

- Estado: pontos, conquistas, loading, error
- Métodos: compartilhar conquistas, verificar novas conquistas
- Novas conquistas: lista de conquistas recém-desbloqueadas

## Componentes de UI

### `PointsCard`

Exibe pontos do usuário, nível atual e progresso para o próximo nível.

### `AchievementCard`

Card de conquista individual com:
- Badge/ícone
- Nome
- Descrição
- Status (desbloqueada/bloqueada)
- Botão para compartilhar

### `AchievementsList`

Lista de conquistas com:
- Filtros por categoria
- Busca
- Estatísticas (total, desbloqueadas, %)

### `NewAchievementModal`

Modal que aparece quando o usuário desbloqueia novas conquistas:
- Animação com confetes
- Detalhes da conquista
- Botões para compartilhar nas redes sociais

## Página Principal

`GamificationPage` contém:
- Card de pontos e nível
- Abas para navegação:
  - Conquistas
  - Ranking (em breve)
  - Atividades (em breve)
- Modal para novas conquistas

## Fluxos Principais

1. **Visualização de Pontos e Nível**:
   - Carrega pontos do usuário via API
   - Exibe pontuação e barra de progresso 

2. **Exploração de Conquistas**:
   - Carrega conquistas via API
   - Permite filtrar e buscar
   - Exibe estatísticas de progresso

3. **Desbloqueio de Conquistas**:
   - Modal exibido automaticamente após o desbloqueio
   - Animação com confetes para celebrar
   - Opções de compartilhamento

4. **Compartilhamento Social**:
   - Compartilhar conquistas em redes sociais
   - Integração com WhatsApp, Twitter, Facebook

## Integração com Outras Features

- **Autenticação**: Verifica tipo de assinatura do usuário 
- **Estudo**: Recebe eventos de progresso de estudo para atribuir pontos
- **Chat**: Recebe eventos de uso do chat para atribuir pontos

## Próximos Passos

- Implementar ranking de usuários
- Adicionar visualização de histórico de atividades
- Expandir sistema de conquistas com categorias adicionais
- Implementar notificações push para novas conquistas 