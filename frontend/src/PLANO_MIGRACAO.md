# Plano de Migração - FaleComJesus Frontend

Este documento detalha o processo de migração da arquitetura atual do frontend do FaleComJesus para a nova arquitetura baseada em features.

## Visão Geral da Migração

A migração será realizada de forma gradual, feature por feature, permitindo que o aplicativo continue funcionando durante todo o processo. Utilizaremos uma abordagem de strangler pattern, onde cada funcionalidade será migrada individualmente enquanto o sistema continua operacional.

## Estado Atual e Estado Alvo

### Estrutura Atual (Legado)
```
src/
├── components/    # Componentes compartilhados e específicos por tipo
├── contexts/      # Contextos React globais
├── hooks/         # Hooks customizados
├── pages/         # Páginas da aplicação
├── services/      # Serviços de API
├── types/         # Definições de tipos TypeScript
└── utils/         # Funções utilitárias
```

### Estrutura Alvo (Nova)
```
src/
├── app/           # Configuração do app, providers, etc.
├── features/      # Features encapsuladas
│   ├── auth/
│   ├── bible/
│   ├── chat/
│   ├── monetization/
│   ├── admin/
│   └── study/
├── shared/        # Código compartilhado entre features
│   ├── api/
│   ├── components/
│   ├── hooks/
│   └── utils/
```

## Princípios da Migração

1. **Não quebrar o funcionamento existente**: Cada mudança deve manter o aplicativo operacional
2. **Migração Feature por Feature**: Completar uma feature antes de seguir para a próxima
3. **Testes contínuos**: Garantir que cada parte migrada continue funcionando
4. **Documentação clara**: Atualizar documentação à medida que cada feature for migrada

## Plano de Ação Detalhado

### Fase 1: Estrutura Base e Autenticação
✅ **Concluído**
- ✅ Estrutura inicial do projeto
- ✅ Configuração do ambiente
- ✅ Sistema de autenticação com JWT
- ✅ Login/Registro com validação
- ✅ Proteção de rotas autenticadas

### Fase 2: Conteúdo Bíblico
✅ **Concluído**
- ✅ Importação da base bíblica
- ✅ API de consulta por livro, capítulo, versículo
- ✅ Interface para navegação bíblica
- ✅ Sistema de busca por palavra-chave
- ✅ Temas preferidos e marcações

### Fase 3: Devocional Diário
✅ **Concluído**
- ✅ Sistema de devocionais programados
- ✅ Componentes visuais para exibição
- ✅ Integração com API de conteúdo
- ✅ Lembretes e notificações
- ✅ Sistema de favoritos e compartilhamento

### Fase 4: Chat IA Básico
✅ **Concluído**
- ✅ Integração inicial com API da OpenAI
- ✅ Interface de chat responsiva
- ✅ Prompts pré-definidos para temas bíblicos
- ✅ Limitação de uso para plano Free
- ✅ Histórico de conversas

### Fase 5: Estudo Bíblico
✅ **Concluído**
- ✅ Sistema de planos de estudo personalizados
- ✅ Acompanhamento de progresso do usuário
- ✅ Sistema de onboarding de preferências
- ✅ Página de listagem com filtros
- ✅ Componentes de exibição de planos
- ✅ Página de detalhes do plano
- ✅ Sistema de acompanhamento de progresso

### Fase 6: Gamificação e Motivação
✅ **Concluído (100%)**
- ✅ Definição de tipos e interfaces para pontos, conquistas e notificações
- ✅ Implementação do contexto e serviços para interação com backend
- ✅ Componentes para exibição de pontos e progresso
- ✅ Componentes para exibição de conquistas e medalhas
- ✅ Componentes para notificações de gamificação
- ✅ Dashboard de progresso do usuário
- ✅ Integração com ações do usuário (login diário, conclusão de estudo)
- ✅ Persistência local dos dados para desenvolvimento
- ✅ Integração com rotas de navegação

### Fase 7: Monetização e Planos
✅ **Concluído (100%)**
- ✅ Definir tipos para planos (Free, Premium)
- ✅ Implementar MonetizationContext
- ✅ Criar hook useMonetization
- ✅ Criar componentes para exibição de planos
- ✅ Criar páginas de planos e assinaturas
- ✅ Implementar sistema de recompensas por anúncios para usuários Free
- ✅ Criar layout principal com barra lateral para navegação
- ✅ Atualizar rotas principais para incorporar a funcionalidade

### Fase 8: Recursos Administrativos
✅ **Concluído (100%)**
- ✅ Definir tipos e interfaces para o painel admin
- ✅ Implementar AdminContext
- ✅ Criar componentes para dashboard admin
- ✅ Implementar visualização de métricas e usuários
- ✅ Implementar controle de conteúdo
- ✅ Criar rotas protegidas para administradores
- ✅ Implementar layout administrativo com sidebar
- ✅ Criar componentes para visualização de logs e ações
- ✅ Implementar sistema de permissões baseado em roles

### Fase 9: Limpeza e Refinamento
🔄 **Em Andamento (50%)**
- ✅ Remover arquivos redundantes ou antigos (como .prettierrc.old)
- ✅ Corrigir erros de linter em componentes principais
- ✅ Refatorar o componente ProtectedRoute para integração com o sistema de roles
- 🔄 Verificar dependências circulares entre features
- 🔄 Otimizar os imports e reduzir o código redundante
- 🔄 Corrigir problemas nas importações de componentes ausentes no módulo de admin

### Fase 10: Integração com Backend Real
⏱️ **Planejado (0%)**
- ⏱️ Substituir os dados mock por chamadas reais à API
- ⏱️ Implementar interceptadores para tratamento de erros de API
- ⏱️ Configurar ambiente de produção e staging
- ⏱️ Integrar autenticação com backend real
- ⏱️ Implementar mecanismos de retry e fallback
- ⏱️ Teste em um ambiente integrado completo

---

## Resumo do Progresso Atual

**Concluído:** Fases 1-8 (100%)
**Em andamento:** Fase 9: Limpeza e Refinamento (50%)
**Planejado:** Fase 10: Integração com Backend Real (0%)

A migração para a nova arquitetura baseada em features foi concluída com sucesso. Agora estamos na fase de limpeza e refinamento, corrigindo erros de linter, removendo arquivos desnecessários e otimizando o código antes da integração com o backend real.

## Cronograma Estimado

1. **Fase 1: Estrutura Base e Autenticação** ✅ Concluído
   - Setup do projeto, estrutura de pastas, configurações iniciais
   - Sistema de autenticação (registro, login, refresh token)
   - Layout base da aplicação

2. **Fase 2: Conteúdo Bíblico** ✅ Concluído
   - Implementação da Bíblia digital
   - Navegação por livros, capítulos e versículos
   - Pesquisa por palavras-chave

3. **Fase 3: Devocional Diário** ✅ Concluído
   - Funcionalidade de devocional diário
   - Sistema de favoritos e histórico
   - Compartilhamento de versículos

4. **Fase 4: Chat IA Básico** ✅ Concluído
   - Integração com API da OpenAI
   - Interface de chat
   - Histórico de conversas

5. **Fase 5: Estudo Bíblico** ✅ Concluído
   - Planos de estudo bíblico personalizados
   - Progresso do usuário
   - Sistema de onboarding para preferências
   - Página de listagem de planos com filtros
   - Componentes de exibição de planos
   - Página de detalhes do plano/estudo
   - Sistema de progresso e acompanhamento

6. **Fase 6: Gamificação e Motivação** ✅ Concluído
   - Sistema de pontos e conquistas
   - Notificações de gamificação
   - Dashboard de progresso do usuário

7. **Fase 7: Monetização e Planos** ✅ Concluído
   - Implementação de planos premium
   - Sistema de recompensas por anúncios
   - Componentes de exibição de planos

8. **Fase 8: Recursos Administrativos** ✅ Concluído
   - Painel administrativo com dashboard
   - Gerenciamento de usuários e conteúdo
   - Sistema de permissões baseado em roles

9. **Fase 9: Limpeza e Refinamento** 🔄 Em Andamento
   - Remoção de arquivos desnecessários
   - Correção de erros de linter
   - Otimização de código
   - Refatoração de componentes problemáticos

10. **Fase 10: Integração com Backend Real** ⏱️ Planejado
    - Substituição dos mocks por chamadas reais
    - Configuração de interceptores de API
    - Teste end-to-end com backend real
    - Deploy em ambiente de staging

## Considerações e Riscos

### Considerações Técnicas

1. **Dependências Circulares**: Evitar importações cruzadas entre features
2. **Tamanho dos bundles**: Monitorar o tamanho dos bundles gerados
3. **Componentização**: Extrair componentes reutilizáveis para `shared/components`
4. **Tipagem Consistente**: Manter tipagem consistente entre features

### Riscos e Mitigação

1. **Quebra de funcionalidades**: Teste rigoroso após cada migração de feature
2. **Tempo de migração**: Priorizar features críticas primeiro
3. **Performance**: Comparar métricas de performance antes e depois da migração
4. **Compatibilidade de browser**: Testar em diversos navegadores após cada fase

## Como testar cada migração

1. Criar uma branch por feature
2. Implementar todos os passos da feature
3. Testar localmente todas as funcionalidades da feature
4. Realizar merge request com revisão de código
5. Deploy em ambiente de homologação
6. Testes de aceitação
7. Merge para a branch principal

## Conclusão

Este plano de migração permitiu uma transição gradual e controlada para a nova arquitetura, mantendo o aplicativo funcional durante todo o processo. A abordagem feature por feature minimizou riscos e permitiu ajustes conforme necessário.

O progresso realizado até o momento confirma a eficácia da estratégia de migração. As oito fases principais foram concluídas com sucesso e demonstram que:

1. **A arquitetura baseada em features** proporciona melhor organização do código e facilita manutenções futuras
2. **A migração gradual** mantém o aplicativo funcional e minimiza riscos durante todo o processo
3. **A documentação atualizada** ajuda a equipe a compreender o sistema e facilita a integração de novos desenvolvedores
4. **A separação clara de responsabilidades** entre diferentes features reduz o acoplamento e torna o código mais sustentável

As próximas etapas envolvem a limpeza do código, otimização e integração com o backend real, preparando o aplicativo para o ambiente de produção.

## Plano de Migração Frontend - FaleComJesus

### Objetivos

Este documento detalha a migração da arquitetura frontend do aplicativo FaleComJesus de uma estrutura monolítica para uma estrutura modular baseada em feature.

### Estrutura Atual vs Estrutura Alvo

**Atual (Monolítica):**
```
src/
  components/      # Todos componentes misturados
  contexts/        # Contextos globais
  pages/           # Páginas da aplicação
  services/        # Serviços de API
  utils/           # Utilitários
  hooks/           # Custom hooks
  App.tsx
```

**Alvo (Baseada em Features):**
```
src/
  shared/          # Código compartilhado entre features
    components/    # Componentes base reutilizáveis
    hooks/         # Custom hooks genéricos 
    services/      # Serviços compartilhados (API, analytics)
    utils/         # Utilitários genéricos
    constants/     # Constantes globais
  features/        # Features da aplicação
    auth/          # Autenticação
      components/  # Componentes específicos de auth
      hooks/       # Hooks específicos de auth
      services/    # Serviços de auth
      types/       # Tipos/interfaces de auth
    bible/         # Módulo da Bíblia
    chat/          # Módulo do Chat com IA
    study/         # Módulo de estudos
    ...
  App.tsx          # Componente raiz
```

### Princípios da Migração

1. **Modularidade:** Cada feature deve ser independente e coesa.
2. **Coesão:** Componentes relacionados a uma feature devem estar juntos.
3. **Desacoplamento:** Mínimo de dependências entre features.
4. **Reuso:** Código compartilhado fica na pasta `shared/`.
5. **Migração Gradual:** Não refatorar tudo de uma vez, fazer por fases.

### Plano de Ação (Fases)

#### Fase 0: Preparação (Semana 1)
- ✅ Criar estrutura de diretórios baseada em features
- ✅ Atualizar configurações de build/lint
- ✅ Preparar documentação para desenvolvedores

#### Fase 1: Migração Inicial - Estrutura Shared (Semana 2)
- ✅ Criar pasta `shared/` com subdiretórios
- ✅ Migrar utilitários genéricos para `shared/utils/`
- ✅ Migrar hooks genéricos para `shared/hooks/`
- ✅ Migrar componentes base para `shared/components/`
- ✅ Criar `shared/services/` para serviços compartilhados

#### Fase 2: Migração de Autenticação (Semana 3)
- ✅ Criar diretório `features/auth/`
- ✅ Migrar componentes relacionados a autenticação
- ✅ Migrar serviços e contexto de autenticação
- ✅ Atualizar imports nos arquivos existentes

#### Fase 3: Migração de Conteúdo Bíblico (Semana 4)
- ✅ Criar diretório `features/bible/`
- ✅ Migrar componentes relacionados à Bíblia
- ✅ Migrar serviços de dados bíblicos
- ✅ Atualizar imports nos arquivos existentes

#### Fase 4: Migração de Devocional Diário (Semana 5)
- ✅ Criar diretório `features/devotional/`
- ✅ Migrar componentes do devocional diário
- ✅ Migrar lógica de negócio relacionada
- ✅ Atualizar imports nos arquivos existentes

#### Fase 5: Migração de Chat com IA (Semana 6)
- ✅ Criar diretório `features/chat/`
- ✅ Migrar componentes do chat com IA
- ✅ Migrar serviços de comunicação com a API de IA
- ✅ Atualizar imports nos arquivos existentes

#### Fase 6: Migração de Estudo e Planos (Semana 7)
- ✅ Criar diretório `features/study/`
- ✅ Migrar componentes de estudo e planos
- ✅ Migrar serviços relacionados
- ✅ Atualizar imports nos arquivos existentes

#### Fase 7: Migração de Gamificação (Semana 8)
- ✅ Criar diretório `features/gamification/`
- ✅ Migrar componentes de gamificação e recompensas
- ✅ Migrar serviços relacionados
- ✅ Atualizar imports nos arquivos existentes

#### Fase 8: Recursos Administrativos (Semana 9)
- ✅ Criar diretório `features/admin/`
- ✅ Migrar componentes administrativos
- ✅ Migrar painéis e relatórios
- ✅ Atualizar imports nos arquivos existentes

#### Fase 9: Limpeza e Testes (Semana 10)
- ✅ Remover código legado não utilizado
- ✅ Atualizar estrutura de rotas
- ✅ Refatorar `App.tsx` com nova estrutura
- ✅ Testes de regressão para garantir funcionalidade

#### Fase 10: Integração com Backend Real (Semanas 11-17)
- 🟡 Criar cliente API centralizado com Axios
  - ✅ 10.1.1 Implementação de base client com interceptors para JWT
  - ✅ 10.1.2 Configuração de ambientes (.env.*) e CORS
  - ⏳ 10.1.3 Sistema de cache e gerenciamento de estado com React Query
- ⏳ Integração com MS-Auth
- ⏳ Integração com MS-Study
- ⏳ Integração com MS-ChatIA
- ⏳ Integração com MS-Bible
- ⏳ Integração com MS-Gamification
- ⏳ Integração com MS-Monetization
- ⏳ Integração com MS-Admin

### Status Atual (Março/2023)

- **Progresso:** 92% (Fases 0-9 completas, Fase 10 em andamento)
- **Trabalhando atualmente:** Fase 10 - Integração com Backend Real
- **Próximos passos:** Finalizar integração com todos os microsserviços

### Detalhamento da Fase 10: Integração com Backend Real

#### 10.1 Infraestrutura de Comunicação

##### 10.1.1 Cliente HTTP Centralizado ✅
- ✅ Criar `shared/services/api.ts` com cliente Axios configurado
- Implementar interceptors para:
  - ✅ Autenticação via JWT
  - ✅ Refresh automático de token
  - ✅ Manipulação padronizada de erros
  - ✅ Retry em caso de falhas de rede

##### 10.1.2 Configuração de Ambientes ✅
- ✅ Criar arquivos de configuração para diferentes ambientes:
  - ✅ `.env.development` - Ambiente de desenvolvimento local
  - ✅ `.env.staging` - Ambiente de homologação
  - ✅ `.env.production` - Ambiente de produção
- ✅ Configurar URLs dos microsserviços em cada ambiente
- ✅ Criar constantes centralizadas em `shared/constants/config.ts`

##### 10.1.3 Cache e Estado Global ⏳
- Implementar React Query para gerenciamento de estado do servidor
- Configurar estratégias de cache por recurso
- Implementar mecanismos de invalidação de cache
- Criar custom hooks para abstrair a complexidade da API

#### 10.2 Integração com Microsserviços

##### 10.2.1 MS-Auth
- Implementar autenticação com microsserviço real
- Adaptar contexto de autenticação para usar MS-Auth
- Implementar login, registro e renovação de token
- Testes de integração com o backend real

##### 10.2.2 MS-Study
- Adaptação dos serviços de estudo para API real
- Implementar busca de planos de estudo e progresso
- Integrar com sistema de reflexões e anotações
- Testes de integração com o backend real

##### 10.2.3 MS-ChatIA
- Implementar comunicação com serviço de IA real
- Adaptar para suportar streaming de respostas
- Integrar com controle de limites de uso do plano gratuito
- Testes de performance e confiabilidade

##### 10.2.4 MS-Bible
- Implementar busca e navegação na API bíblica real
- Configurar cache para conteúdo bíblico (reduzir requisições)
- Adaptar componentes para estrutura de dados real
- Testes de integração para verificar navegação e busca

##### 10.2.5 MS-Gamification
- Integrar com sistema de pontos e conquistas real
- Implementar notificações de conquistas desbloqueadas
- Adaptar componentes para estrutura de dados real
- Testes de integração para verificar pontuação e desbloqueios

##### 10.2.6 MS-Monetization
- Implementar integração com sistemas de pagamento (Stripe/Hotmart)
- Adaptar para verificação de assinaturas ativas
- Implementar controle de acesso a recursos premium
- Testes de fluxo de compra e verificação de assinatura

##### 10.2.7 MS-Admin
- Integrar com serviço de administração real
- Implementar dashboards com dados reais
- Configurar controles de acesso baseado em perfil
- Testes de funcionalidades administrativas

#### 10.3 Estratégia de Tratamento de Erros
- ✅ Implementar tratamento global de erros
- ✅ Criar componentes de fallback para falhas de rede
- ✅ Implementar estratégia de retry para operações cruciais
- ✅ Integrar com sistema de log/monitoramento (Sentry)

#### 10.4 Testes e QA
- Implementar testes de integração com APIs reais
- Criar ambiente de staging para testes pré-produção
- Implementar monitoring de performance da comunicação
- Documentar todos os endpoints e contratos de API

#### 10.5 Estratégia de Deploy
- Configurar pipeline CI/CD para diferentes ambientes
- Implementar feature flags para lançamento controlado
- Criar estratégia de rollback para emergências
- Configurar monitoramento em produção

#### Cronograma Detalhado da Fase 10

| Semana | Atividade | Status |
|--------|-----------|--------|
| 11     | Infraestrutura de Comunicação (10.1) | 🟡 Em progresso (67%) |
| 12     | MS-Auth e MS-Bible (10.2.1, 10.2.4) | ⚪ Não iniciado |
| 13     | MS-Study (10.2.2) | ⚪ Não iniciado |
| 14     | MS-ChatIA (10.2.3) | ⚪ Não iniciado |
| 15     | MS-Gamification e MS-Monetization (10.2.5, 10.2.6) | ⚪ Não iniciado |
| 16     | MS-Admin, testes finais e deploy (10.2.7, 10.4, 10.5) | ⚪ Não iniciado |
| 17     | Limpeza e documentação final | ⚪ Não iniciado | 