# Guia de Implementação - Funcionalidade de Chat IA

Este documento descreve a implementação da funcionalidade de Chat IA no aplicativo FaleComJesus, detalhando a estrutura de arquivos, tipos, API, hooks, contextos, componentes e fluxos principais.

## Estrutura de Arquivos

```
src/features/chat/
├── api/
│   └── chatService.ts           # Serviços de API para interação com Chat IA
├── components/
│   ├── ChatBubble.tsx           # Componente de mensagem (bolha)
│   ├── ChatForm.tsx             # Formulário de envio de mensagem
│   ├── ChatHistory.tsx          # Histórico de mensagens
│   ├── ChatLoader.tsx           # Animação de carregamento da resposta
│   ├── ChatPlaceholder.tsx      # Placeholder para chat vazio
│   ├── ChatScreen.tsx           # Tela principal do chat
│   └── AdRewardPrompt.tsx       # Prompt para assistir vídeo de recompensa
├── contexts/
│   └── ChatContext.tsx          # Contexto para gerenciar estado do chat
├── hooks/
│   └── useChat.ts               # Hook para gerenciar interações com chat
├── pages/
│   └── ChatPage.tsx             # Página principal do chat
├── types/
│   └── index.ts                 # Definições de tipos
├── utils/
│   ├── messageFormatter.ts      # Formatador de mensagens
│   └── promptTemplates.ts       # Templates para prompts da IA
└── index.ts                     # Arquivo barrel para exportações
```

## Tipos e Interfaces

A feature utiliza os seguintes tipos principais, definidos em `types/index.ts`:

- `Message`: Representa uma mensagem de chat (usuário ou IA)
- `ChatHistory`: Lista de mensagens do histórico
- `ChatState`: Estado atual do chat
- `ChatSettings`: Configurações do chat (tom, estilo, etc.)
- `ChatError`: Erros específicos do chat
- `AdReward`: Recompensa por assistir anúncios

## API Service

O arquivo `api/chatService.ts` inclui métodos para interagir com o backend:

- `sendMessage`: Envia mensagem do usuário e recebe resposta da IA
- `getHistory`: Obtém histórico de conversas do usuário
- `deleteHistory`: Limpa histórico de conversas
- `checkMessageLimit`: Verifica limites diários do plano Free
- `rewardAdWatched`: Registra recompensa por anúncio assistido

## State Management

### Hook `useChat`

O hook `useChat` gerencia o estado e as interações do chat usando React Query:

- Controla mensagens enviadas e recebidas
- Gerencia histórico de conversa
- Mantém estado de digitação e carregamento
- Verifica limites de mensagens para usuários Free
- Integra com sistema de recompensas por anúncios

### Contexto `ChatContext`

O contexto fornece acesso global ao estado do chat e métodos:

- `messages`: Lista de mensagens da conversa atual
- `isLoading`: Estado de carregamento da resposta da IA
- `isTyping`: Simulação de digitação da IA (opcional)
- `sendMessage`: Método para enviar mensagem ao chat
- `clearHistory`: Método para limpar histórico
- `remainingMessages`: Número de mensagens restantes no plano Free
- `watchAdForReward`: Método para obter mais mensagens assistindo anúncio

## Componentes de UI

### `ChatBubble`

Exibe uma mensagem no chat:
- Estilo diferente para mensagens do usuário e da IA
- Suporte a formatação Markdown para respostas da IA
- Opções para copiar, compartilhar ou ouvir a mensagem
- Timestamp da mensagem

### `ChatForm`

Formulário para envio de mensagens:
- Campo de texto expandível
- Botão de envio
- Indicação de limite de caracteres
- Feedback quando limite de mensagens é atingido

### `ChatHistory`

Exibe o histórico de conversas:
- Rolagem automática para a mensagem mais recente
- Agrupamento de mensagens por data
- Carregamento incremental do histórico (lazy loading)
- Animação para novas mensagens

### `AdRewardPrompt`

Prompt exibido quando usuário atinge limite de mensagens:
- Explicação clara sobre o limite
- Opção para assistir anúncio e ganhar mais mensagens
- Botão para upgrade para plano Premium
- Contador de mensagens liberadas após anúncio

## Páginas Principais

### `ChatPage`

Exibe a interface completa do chat:
- Histórico de mensagens
- Formulário de envio
- Indicadores de status (digitando, limite atingido)
- Integração com sistema de recompensas

## Integração com Monetização

A feature de Chat IA se integra diretamente com a de Monetização:

1. Verifica o plano do usuário para determinar limites
2. Para plano Free:
   - Limita a 5 mensagens por dia
   - Oferece opção de assistir anúncio para ganhar 5 mensagens adicionais
   - Exibe botão para upgrade para plano Premium
3. Para plano Premium:
   - Sem limites de mensagens
   - Sem publicidade
   - Prioridade nas respostas da IA

## Fluxos Principais

1. **Envio de Mensagem**:
   - Usuário digita e envia mensagem
   - Frontend adiciona mensagem ao estado local imediatamente
   - Sistema verifica se usuário atingiu limite (plano Free)
   - Se não atingiu, envia requisição ao backend
   - Exibe indicador de "digitando..." durante resposta
   - Recebe e exibe resposta da IA
   - Atualiza contador de mensagens restantes

2. **Limite Atingido (Plano Free)**:
   - Sistema detecta que usuário atingiu limite diário
   - Exibe `AdRewardPrompt` com opções
   - Usuário pode assistir anúncio para ganhar mais mensagens
   - Após assistir, sistema registra recompensa
   - Limite é atualizado, permitindo continuar conversa

3. **Histórico de Conversas**:
   - Ao abrir o chat, sistema carrega histórico de conversas
   - Exibe histórico por data/hora, com mensagens mais recentes no final
   - Usuário pode limpar histórico
   - Histórico é sincronizado com backend para acesso em diferentes dispositivos

## Integração com Outras Features

- **Autenticação**: Associa histórico de chat ao usuário logado
- **Estudo**: Permite compartilhar respostas do chat no estudo diário
- **Bíblia**: Integra versículos citados com links para a Bíblia
- **Monetização**: Controle de limites e recompensas

## Considerações de UX/UI

- Animações suaves para transições e novas mensagens
- Feedback visual claro sobre limites e opções
- Design responsivo para desktop e mobile
- Acessibilidade: contraste adequado, navegação por teclado, textos alternativos

## Considerações de Performance

- Otimização de renders com `React.memo` e `useCallback`
- Lazy loading para histórico extenso
- Armazenamento local de mensagens recentes
- Debounce para requisições de digitação em tempo real 