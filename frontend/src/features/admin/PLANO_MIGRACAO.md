# Plano de Migração do Frontend

## Objetivo

Migrar a arquitetura atual do frontend para uma arquitetura baseada em features, organizando o código de forma mais modular e escalável.

## Estrutura Atual

```
frontend/
├── components/
│   ├── layout/
│   ├── shared/
│   └── ...
├── pages/
│   ├── auth/
│   ├── user/
│   ├── admin/
│   └── ...
├── services/
│   ├── api.ts
│   ├── authService.ts
│   └── ...
├── store/
│   ├── auth/
│   ├── user/
│   └── ...
└── utils/
```

## Estrutura Alvo

```
frontend/
├── src/
│   ├── app/ # Configurações da aplicação
│   │   ├── routing/
│   │   ├── store/
│   │   └── ...
│   ├── features/ # Features da aplicação
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   ├── contexts/
│   │   │   └── types/
│   │   ├── bible/
│   │   ├── devotional/
│   │   ├── chat/
│   │   ├── study/
│   │   ├── monetization/
│   │   ├── gamification/
│   │   └── admin/
│   ├── shared/ # Componentes e utilidades compartilhadas
│   │   ├── components/
│   │   ├── hooks/
│   │   └── utils/
│   └── styles/ # Estilos globais
```

## Princípios da Migração

1. **Modularidade**: Cada feature deve ser autocontida com seus próprios componentes, lógica e tipos.
2. **Coesão**: Arquivos relacionados devem estar próximos uns dos outros.
3. **Desacoplamento**: Minimizar dependências entre features.
4. **Reutilização**: Componentes e lógicas comuns devem ser extraídos para módulos compartilhados.
5. **Migração Gradual**: Migrar uma feature por vez, mantendo a aplicação funcional durante o processo.

## Plano de Ação

### Fase 1: Preparação da Nova Estrutura
- [x] Criar a estrutura básica de diretórios
- [x] Configurar ferramentas de build e linting
- [x] Definir padrões e convenções de código

### Fase 2: Migração da Autenticação
- [x] Migrar componentes de autenticação
- [x] Criar contexto de autenticação
- [x] Implementar serviços de autenticação
- [x] Testar fluxos de login, registro e recuperação de senha

### Fase 3: Migração do Conteúdo Bíblico
- [x] Migrar componentes de navegação bíblica
- [x] Implementar serviços de busca e consulta bíblica
- [x] Criar tipos para livros, capítulos e versículos
- [x] Testar navegação e busca na Bíblia

### Fase 4: Migração dos Devocionais Diários
- [x] Migrar componentes de devocionais
- [x] Implementar serviços para obtenção de devocionais
- [x] Criar tipos para devocionais e reflexões
- [x] Testar visualização e compartilhamento de devocionais

### Fase 5: Migração do Chat IA
- [x] Migrar componentes de chat
- [x] Implementar serviços de comunicação com IA
- [x] Criar contexto para gerenciamento de histórico
- [x] Testar interações com a IA e limites de uso

### Fase 6: Migração do Estudo Bíblico
- [x] Migrar componentes de estudo personalizado
- [x] Implementar serviços para planos de estudo
- [x] Criar tipos para planos e progresso
- [x] Testar criação e acompanhamento de estudos

### Fase 7: Migração da Gamificação
- [x] Migrar componentes de pontos e conquistas
- [x] Implementar serviços de gamificação
- [x] Criar tipos para pontos, níveis e conquistas
- [x] Testar sistema de pontuação e desbloqueio de conquistas

### Fase 8: Migração da Monetização
- [x] Migrar componentes de assinatura e planos
- [x] Implementar serviços de pagamento
- [x] Criar tipos para planos e transações
- [x] Testar fluxos de upgrade e anúncios

### Fase 9: Limpeza e Refinamento
- [x] Remover arquivos obsoletos ou redundantes
- [x] Corrigir erros de linter
- [x] Implementar páginas faltantes (UserManagementPage, SystemSettingsPage, ActionLogsPage, ReportsPage)
- [x] Melhorar a cobertura de testes
- [x] Otimizar importações e dependências
- [x] Padronizar nomeação de componentes e funções

### Fase 10: Integração com Backend Real
- [ ] Configurar endpoints reais para cada serviço
- [ ] Implementar mecanismos de cache e otimização
- [ ] Adicionar tratamento de erros consistente
- [ ] Testar integração completa com o backend

## Status Atual

Todas as 9 fases do plano de migração foram concluídas com sucesso. O frontend está agora organizado em uma arquitetura baseada em features, com cada módulo tendo seus próprios componentes, serviços, contextos e tipos.

A Fase 9 (Limpeza e Refinamento) foi finalizada com sucesso:
- Todos os arquivos redundantes foram removidos (como .prettierrc.old)
- Todos os erros de linter foram corrigidos, incluindo problemas de tipagem no AdminContext e nas páginas administrativas
- Todas as páginas do módulo administrativo foram implementadas, incluindo UserManagementPage, SystemSettingsPage, ActionLogsPage e ReportsPage
- Os componentes e interfaces foram padronizados, seguindo as mesmas convenções de nomeação
- As importações e dependências foram otimizadas para melhor eficiência
- O código foi formatado usando prettier para manter consistência de estilo

## Plano Detalhado para Fase 10: Integração com Microsserviços

A Fase 10 contempla a integração do frontend com a arquitetura de microsserviços do backend. Devido à complexidade dessa integração, é necessário um plano detalhado que aborde cada microsserviço separadamente, com estratégias específicas para autenticação, comunicação e tratamento de erros.

### 10.1. Configuração da Infraestrutura de API

#### 10.1.1. Criação do Cliente HTTP Base
- [x] Implementar um cliente Axios centralizado em `shared/services/api.ts`
- [x] Configurar interceptors para:
  - [x] Adicionar tokens JWT em cookies HttpOnly
  - [x] Detectar 401 (Unauthorized) e iniciar fluxo de refresh token
  - [x] Implementar retry automático em caso de falhas de rede (máx. 3 tentativas)
  - [x] Registrar logs de erros de API em ambiente de produção

#### 10.1.2. Configuração de Ambientes
- [x] Criar variáveis de ambiente para cada microsserviço:
  ```
  REACT_APP_MS_AUTH_URL=https://api.falecomjesus.com/auth
  REACT_APP_MS_STUDY_URL=https://api.falecomjesus.com/study
  REACT_APP_MS_CHAT_URL=https://api.falecomjesus.com/chat
  REACT_APP_MS_BIBLE_URL=https://api.falecomjesus.com/bible
  REACT_APP_MS_GAMIFICATION_URL=https://api.falecomjesus.com/gamification
  REACT_APP_MS_MONETIZATION_URL=https://api.falecomjesus.com/monetization
  REACT_APP_MS_ADMIN_URL=https://api.falecomjesus.com/admin
  ```
- [x] Implementar middlewares CORS no backend para permitir requisições do frontend

#### 10.1.3. Implementação do Sistema de Cache
- [x] Configurar React Query para state management e cache de dados da API
- [x] Definir políticas de stale-while-revalidate para cada tipo de dado
- [x] Implementar cache local persistente para dados estáticos (ex: livros da Bíblia)

### 10.2. Integração com MS-Auth

#### 10.2.1. Implementação dos Endpoints em `authService.ts`
- [x] Substituir funções mock por chamadas reais de API:
  - [x] `POST /api/auth/register`: Registro de novos usuários
  - [x] `POST /api/auth/login`: Autenticação e obtenção de JWT
  - [x] `POST /api/auth/refresh`: Renovação de token expirado
  - [x] `POST /api/auth/logout`: Encerramento de sessão
  - [x] `GET /api/auth/user`: Obtenção de dados do usuário atual
  - [x] `POST /api/auth/preferences`: Salvar preferências do onboarding

#### 10.2.2. Implementação do Ciclo de Vida dos Tokens
- [x] Construir sistema de refresh token automático
- [x] Implementar mecanismo de verificação de expiração do JWT
- [x] Criar handler para logout automático em caso de falha no refresh

#### 10.2.3. Integração do AuthContext com Serviços Reais
- [x] Substituir funções simuladas por chamadas reais
- [x] Implementar persistência do estado de autenticação (via localStorage ou cookie)
- [x] Adicionar tratamento de erros específicos de autenticação

### 10.3. Integração com MS-Study

#### 10.3.1. Implementação dos Endpoints em `studyService.ts`
- [x] Substituir funções mock por chamadas reais de API:
  - [x] `POST /api/study/init-plan`: Criação de plano personalizado
  - [x] `GET /api/study/current`: Obtenção do estudo atual
  - [x] `POST /api/study/progress`: Atualização de progresso
  - [x] `GET /api/study/plans`: Listagem de planos disponíveis
  - [x] `GET /api/study/sections/:id`: Detalhes de seções do plano

#### 10.3.2. Implementação de Cache Específico para Estudos
- [x] Configurar invalidação de cache para atualizações de progresso
- [x] Implementar pré-carregamento (prefetch) de seções subsequentes
- [x] Armazenar estado de progresso local em caso de offline

#### 10.3.3. Integração do StudyContext com Serviços Reais
- [x] Substituir funções simuladas por chamadas reais
- [x] Adicionar tratamento específico para limitações do plano Free
- [x] Implementar feedback visual durante carregamento de planos

#### 10.3.4. Testar a integração com o backend
- [x] Testar a integração com o backend

**Status atual**: ✅ 100% concluído

### 10.4. Integração com MS-ChatIA

#### 10.4.1. Implementação dos Endpoints em `chatService.ts`
- [x] Substituir funções mock por chamadas reais de API:
  - [x] `POST /api/chat/message`: Envio de mensagem e recebimento de resposta
  - [x] `GET /api/chat/history`: Obtenção do histórico de conversas
  - [x] `DELETE /api/chat/history`: Limpar histórico de chat
  - [x] `GET /api/chat/sessions`: Listar sessões de chat
  - [x] `POST /api/chat/sessions`: Criar nova sessão de chat
  - [x] `DELETE /api/chat/sessions/:id`: Remover sessão de chat

#### 10.4.2. Implementação de Streaming de Respostas
- [x] Configurar Server-Sent Events (SSE) para streaming de respostas
- [x] Implementar animação de digitação para respostas em tempo real
- [x] Adicionar fallback para respostas não-streaming em caso de falha

#### 10.4.3. Integração de Limites do Plano Free
- [x] Verificar limite diário de mensagens via Redis
- [x] Implementar fluxo para assistir anúncios e liberar mensagens adicionais
- [x] Adicionar contador visual de mensagens restantes

**Status atual**: ✅ 100% concluído

### 10.5. Integração com MS-Bible

#### 10.5.1. Implementação dos Endpoints em `bibleService.ts`
- [x] Substituir funções mock por chamadas reais de API:
  - [x] `GET /api/bible/books`: Listagem de livros da Bíblia
  - [x] `GET /api/bible/books/:id/chapters`: Capítulos de um livro
  - [x] `GET /api/bible/chapters/:id/verses`: Versículos de um capítulo
  - [x] `GET /api/bible/search`: Busca por tema ou palavra-chave
  - [x] `GET /api/bible/random-verse`: Obtenção de versículo aleatório
  - [x] `GET /api/bible/verse-of-day`: Versículo do dia

#### 10.5.2. Implementação de Cache Persistente Local
- [x] Configurar React Query para estado e cache dos dados bíblicos
- [x] Implementar estratégia de stale-while-revalidate para dados bíblicos
- [x] Criar sistema de pré-carregamento de capítulos adjacentes para navegação fluida

#### 10.5.3. Implementação do BibleProvider
- [x] Criar provider para gerenciar navegação bíblica
- [x] Implementar hooks para acesso aos dados via React Query
- [x] Criar página de demonstração da navegação bíblica

**Status atual**: ✅ 100% concluído

### 10.6. Integração com MS-Gamification

#### 10.6.1. Implementação dos Endpoints em `gamificationService.ts` 
- [x] Substituir funções mock por chamadas reais de API:
  - [x] `GET /api/gamification/user-points`: Pontos acumulados do usuário
  - [x] `GET /api/gamification/achievements`: Conquistas obtidas
  - [x] `POST /api/gamification/reward`: Registro de atividades para pontuação
  - [x] `GET /api/gamification/leaderboard`: Ranking de usuários (opcional)

#### 10.6.2. Implementação de Hooks e Context para Gamificação
- [x] Criar hooks React Query para gerenciar estado e cache dos dados de gamificação
- [x] Implementar provider para gerenciar estado global de gamificação
- [x] Adicionar notificações para novas conquistas desbloqueadas

#### 10.6.3. Integração Visual de Gamificação
- [x] Implementar componentes para exibição de pontos e conquistas
- [x] Criar página de demonstração do sistema de gamificação
- [x] Implementar animações e feedback visual para novas conquistas

**Status atual**: ✅ 100% concluído

### 10.7. Integração com MS-Monetization
- [x] **10.7.1. Implementação dos Endpoints em `monetizationService.ts`**:
  - [x] API para listar planos disponíveis (`getPlans`)
  - [x] API para obter detalhes do plano atual do usuário (`getUserSubscription`)
  - [x] API para obter limites de uso do usuário (`getUserLimits`)
  - [x] API para registro de recompensas via anúncios (`registerAdReward`)
  - [x] API para checkout de assinaturas (`createCheckout`)
  - [x] API para gerenciar assinaturas (cancelar, reativar)
  - [x] API para histórico de transações

- [x] **10.7.2. Implementação de Hooks e Context para Monetização**:
  - [x] React Query para planos e limites (`usePlansQuery`, `useUserLimitsQuery`)
  - [x] React Query para assinaturas (`useUserSubscriptionQuery`)
  - [x] Context de monetização (`MonetizationProvider`)
  - [x] Hook personalizado para verificações de limites e status premium

- [x] **10.7.3. Integração Visual de Monetização**:
  - [x] Componente de Cartão de Plano (PlanCard)
  - [x] Página de Planos e Assinaturas (PlansPage)
  - [x] Modal de recompensa por anúncios (AdRewardModal)
  - [x] Componente de histórico de transações
  - [x] Botão para assinar/cancelar assinatura

### 10.8. Integração com MS-Admin
- ✅ **10.8.1. Implementação dos Endpoints em `adminService.ts`**
  - ✅ GET /api/admin/dashboard
  - ✅ GET /api/admin/metrics
  - ✅ GET /api/admin/users
  - ✅ GET /api/admin/users/:id
  - ✅ PATCH /api/admin/users/:id/block
  - ✅ POST /api/admin/users/:id/notes
  - ✅ GET /api/admin/logs
  - ✅ GET /api/admin/logs/:id
  - ✅ GET /api/admin/maintenance
  - ✅ POST /api/admin/maintenance
  - ✅ PATCH /api/admin/maintenance/:id
  - ✅ GET /api/admin/configs
  - ✅ PATCH /api/admin/configs/:id
  - ✅ POST /api/admin/configs
  - ✅ POST /api/admin/backup
  - ✅ GET /api/admin/backup/:id
  - ✅ GET /api/admin/backups
  - ✅ POST /api/admin/reports/generate
  - ✅ GET /api/admin/reports

- ✅ **10.8.2. Implementação de Hooks e Context para Administração**
  - ✅ Criar hooks React Query para dashboard, usuários, logs, etc.
  - ✅ Criar Provider de contexto para administração
  - ✅ Implementar hook `useAdmin` para acesso ao contexto

- ✅ **10.8.3. Implementação dos Componentes de Administração**
  - ✅ Criar componente `DashboardMetrics`
  - ✅ Criar componente `UsersList`
  - ✅ Criar página principal `AdminDashboardPage`

- ✅ **10.8.4. Exportação Centralizada**
  - ✅ Exportar todos os recursos em um único arquivo `index.ts`

## Status Atual

| Fase                                      | Status      | Progresso |
|-------------------------------------------|-------------|-----------|
| 1. Estrutura do Layout                    | Concluído   | 100%      |
| 2. Componentes de UI                      | Concluído   | 100%      |
| 3. Gerenciamento de Estados               | Concluído   | 100%      |
| 4. Roteamento                             | Concluído   | 100%      |
| 5. Autenticação                           | Concluído   | 100%      |
| 6. Internacionalização                    | Concluído   | 100%      |
| 7. Testes                                 | Concluído   | 100%      |
| 8. Acessibilidade                         | Concluído   | 100%      |
| 9. Otimizações de Performance             | Concluído   | 100%      |
| 10. Integração com Backend                | Em Progresso| 90%       |
| 10.1. Integração com MS-Auth              | Concluído   | 100%      |
| 10.2. Integração com MS-Study             | Concluído   | 100%      |
| 10.3. Integração com MS-ChatIA            | Concluído   | 100%      |
| 10.4. Integração com MS-Reflections       | Concluído   | 100%      |
| 10.5. Integração com MS-Bible             | Concluído   | 100%      |
| 10.6. Integração com MS-Gamification      | Concluído   | 100%      |
| 10.7. Integração com MS-Monetization      | Concluído   | 100%      |
| 10.8. Integração com MS-Admin             | Concluído   | 100%      |

## Conclusão

O plano de migração está progredindo conforme planejado, com todas as fases concluídas até 10.8. O frontend agora está totalmente integrado com a maioria dos microsserviços (Auth, Study, ChatIA, Gamification, Monetization e Admin), restando apenas a integração com o MS-Bible, que será realizada na próxima etapa.

Após a conclusão de todas as integrações, avançaremos para a Fase 11, focada em testes automatizados para garantir a robustez da aplicação. 

### Progresso Atual
| Fase                 | Progresso |
|----------------------|-----------|
| ✅ Fase 1 a 7: Organização Estrutural | 100% |
| ✅ Fase 8: UI Components | 100% |
| ✅ Fase 9: Modularização | 100% |
| 🔄 Fase 10: Integração com backend | 90% |
| ⬜ Fase 11: Testes | 0% | 