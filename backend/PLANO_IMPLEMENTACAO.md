## Plano de Implementação - FaleComJesus Backend

### 1. MS-Auth (Microsserviço de Autenticação)
- [x] Estrutura inicial e configurações 
- [x] Modelos e schemas
- [x] Endpoints de registro e login
- [x] Middleware JWT
- [x] Endpoints de preferências de usuário
- [x] Endpoints de refresh token
- [x] Gerenciamento de assinaturas (Free/Premium)
- [x] Webhook para integração com gateways de pagamento

### 2. MS-Bible (Microsserviço Bíblico)
- [x] Estrutura inicial e configurações 
- [x] Modelos e schemas para livros, capítulos e versículos
- [x] Endpoint para listar livros
- [x] Endpoint para listar capítulos de um livro
- [x] Endpoint para listar versículos de um capítulo
- [x] Endpoint de busca por palavra-chave
- [x] Endpoint para versículo aleatório
- [x] Endpoint para versículo do dia
- [x] Autenticação via middleware (opcional)

### 3. MS-Study (Microsserviço de Estudo)
- [x] Estrutura inicial e configurações
- [x] Modelos e schemas para planos, seções, conteúdo, progresso
- [x] Endpoints para planos de estudo (CRUD)
- [x] Endpoints para progresso do usuário
- [x] Endpoints para reflexões pessoais
- [x] Endpoints para certificados
- [x] Integração com MS-ChatIA para geração de planos personalizados

### 4. MS-ChatIA (Microsserviço de Chat com IA)
- [x] Estrutura inicial e configurações
- [x] Modelos e schemas para histórico de chat
- [x] Endpoint para envio de mensagem e resposta da IA
- [x] Endpoint para histórico de conversa
- [x] Integração com OpenAI (API key segura)
- [x] Lógica de limites de uso diário (Free vs Premium)
- [x] Endpoint para geração de plano personalizado

### 5. MS-Gamification (Microsserviço de Gamificação)
- [x] Estrutura inicial e configurações
- [x] Modelos e schemas para pontos e conquistas
- [x] Endpoints para pontos do usuário
- [x] Endpoints para conquistas
- [x] Endpoints para ranking ou estatísticas

### 6. MS-Monetization (Microsserviço de Monetização)
- [x] Estrutura inicial do projeto
- [x] Modelos de dados e schemas para assinaturas
- [x] Modelos de dados e schemas para recompensas de anúncios
- [x] Endpoints para consulta de status da assinatura
- [x] Endpoints para webhooks de gateways de pagamento (Stripe, Hotmart)
- [x] Endpoints para recompensas de anúncios
- [x] Integração com MS-Auth para obter usuários e atualizar assinaturas
- [x] Serviço de gestão de recompensas por anúncios
- [x] Serviço de limite de mensagens de chat com Redis
- [ ] Testes unitários para serviços 
- [ ] Testes de integração

### 7. MS-Admin (Microsserviço Administrativo)
- [x] Estrutura inicial e configurações
- [x] Modelos e schemas para relatórios e métricas
- [x] Endpoints para dashboard de métricas
- [x] Endpoints para gerenciamento de usuários
- [x] Endpoints para relatórios
- [x] Endpoints para backups e configurações
- [x] Controle de acesso administrativo

### 8. Integração e Testes
- [x] Testes unitários para MS-Auth (funções de segurança, tokens JWT)
- [x] Testes de integração para MS-Auth (rotas de autenticação, registro e login)
- [ ] Testes unitários para demais microsserviços
- [ ] Testes de integração entre microsserviços
- [x] Docker Compose para ambiente completo
- [x] Documentação da API com Swagger
- [ ] Postman Collection para testes manuais
- [ ] Monitoramento com Elastic Stack

### Próximos passos:
1. Implementar o MS-Monetization para controle de anúncios e rewards
2. Adicionar testes unitários e de integração
3. Completar a documentação com Swagger/OpenAPI para todos os serviços

## Objetivo

Alinhar o desenvolvimento do backend com as funcionalidades já implementadas no frontend, garantindo que todos os endpoints necessários estejam disponíveis e operacionais.

## Análise de Situação Atual

O backend agora possui implementações robustas em todos os microsserviços essenciais (Auth, Study, Bible, ChatIA, Gamification e Admin). Eles oferecem todos os endpoints necessários para suportar o frontend e estão preparados para integração com sistemas externos como gateways de pagamento.

## Fase 1: Inicialização de Estrutura e Serviços Essenciais

### Semana 1 - MS-Auth e MS-Admin

#### MS-Auth (Alta Prioridade)
- [x] Estrutura inicial e configurações 
- [x] Modelos e schemas
- [x] Endpoints de registro e login
- [x] Middleware JWT
- [x] Endpoints de preferências de usuário
- [x] Endpoints de refresh token
- [x] Gerenciamento de assinaturas (Free/Premium)
- [x] Webhook para integração com gateways de pagamento

#### MS-Admin (Alta Prioridade)
- [x] Estrutura inicial do serviço administrativo
- [x] Implementação de endpoints para dashboard
- [x] Implementação de endpoints para gerenciamento de usuários
- [x] Implementação de endpoints para logs do sistema
- [x] Implementação de endpoints para tarefas de manutenção
- [x] Implementação de endpoints para configurações do sistema
- [x] Implementação de endpoints para backup e restauração
- [x] Implementação de endpoints para relatórios

### Semana 2 - MS-Bible e MS-Study

#### MS-Bible (Alta Prioridade) 
- [x] Estrutura inicial do serviço da Bíblia
- [x] Modelos e schemas para livros, capítulos e versículos
- [x] Endpoint para listar livros
- [x] Endpoint para listar capítulos de um livro
- [x] Endpoint para listar versículos de um capítulo
- [x] Endpoint de busca por palavra-chave
- [x] Endpoint para versículo aleatório
- [x] Endpoint para versículo do dia
- [x] Autenticação via middleware (opcional)

#### MS-Study (Alta Prioridade)
- [x] Estrutura inicial do serviço de estudos
- [x] Modelos e schemas para planos, seções, conteúdo, progresso
- [x] Endpoints para planos de estudo (CRUD)
- [x] Endpoints para progresso do usuário
- [x] Endpoints para reflexões pessoais
- [x] Endpoints para certificados
- [x] Integração com MS-ChatIA para geração de planos personalizados

### Semana 3 - MS-ChatIA e MS-Gamification

#### MS-ChatIA (Média Prioridade)
- [x] Estrutura inicial e configurações
- [x] Modelos e schemas para histórico de chat
- [x] Endpoint para envio de mensagem e resposta da IA
- [x] Endpoint para histórico de conversa
- [x] Integração com OpenAI (API key segura)
- [x] Lógica de limites de uso diário (Free vs Premium)
- [x] Endpoint para geração de plano personalizado

#### MS-Gamification (Média Prioridade)
- [x] Estrutura inicial do serviço de gamificação
- [x] Modelos e schemas para pontos e conquistas
- [x] Endpoints para pontos do usuário
- [x] Endpoints para conquistas
- [x] Endpoints para ranking ou estatísticas

### Semana 4 - MS-Monetization e Integração Geral

#### MS-Monetization (Média Prioridade)
- [x] Estrutura inicial do serviço de monetização
- [x] Modelos e schemas para assinaturas e recompensas
- [x] Endpoint para verificar status da assinatura
- [x] Endpoint para webhooks (Stripe/Hotmart)
- [x] Endpoint para recompensas por anúncios assistidos
- [x] Integração completa com MS-Auth para gestão de assinaturas
- [ ] Testes unitários e de integração dos webhooks

#### Integração Geral (Alta Prioridade)
- [ ] Revisão e testes de integração entre todos os microsserviços
- [ ] Implementação de registro central de APIs (opcional)
- [ ] Validação final de contratos entre microsserviços
- [ ] Testes de carga e stress
- [ ] Documentação geral do backend
- [ ] Preparação para integração com o frontend

## Fase 2: Otimização e Recursos Adicionais

### Semana 5-6 - Melhorias de Performance e Recursos Adicionais

#### Melhorias de Performance (Média Prioridade)
- [ ] Implementação de cache com Redis
- [ ] Otimização de queries de banco de dados
- [ ] Implementação de rate limiting
- [ ] Monitoramento com ELK stack

#### Recursos Adicionais (Baixa Prioridade)
- [ ] Sistema de certificados para conclusão de estudos
- [ ] API para compartilhamento em redes sociais
- [ ] Recursos avançados de estatísticas
- [ ] Sistema de notificações
- [ ] Funcionalidades de comunidade (opcional)

## Próximos Passos

Agora que concluímos a implementação do MS-Auth, MS-Monetization e a documentação com Swagger/OpenAPI, devemos focar em:

1. Implementar testes unitários e de integração para todos os microsserviços, especialmente para os fluxos críticos de autenticação e monetização.

2. Realizar testes de carga para verificar o comportamento do sistema sob alto volume de usuários, especialmente para serviços com possível gargalo como MS-ChatIA e MS-Bible.

3. Configurar um ambiente de staging para testes integrados com o frontend, simulando o ambiente de produção.

4. Implementar monitoramento com ELK Stack para logs centralizado e alertas em tempo real.

5. Revisar e aprimorar a segurança do sistema, especialmente nas rotas de pagamento e autenticação.

A integração entre todos os microsserviços continuará sendo uma prioridade alta, garantindo que cada parte do sistema funcione harmoniosamente com as demais.

## Cronograma de Implementação

| Semana | Dias | Tarefa | Status |
|--------|------|--------|--------|
| 1 | 1-2 | Estruturação Inicial MS-Admin | ✅ Concluído |
| 1 | 3-4 | Endpoints Dashboard/Métricas | ✅ Concluído |
| 1 | 5-7 | Gerenciamento de Usuários | ✅ Concluído |
| 2 | 1-2 | Implementação de Logs | ✅ Concluído |
| 2 | 3-4 | Implementação de Manutenção | ✅ Concluído |
| 2 | 5-6 | Implementação de Configurações | ✅ Concluído |
| 2 | 7 - 3.2 | Backup e Relatórios | ✅ Concluído |
| 3 | 3-5 | MS-Auth - Assinaturas e Webhooks | ✅ Concluído |
| 3 | 6-7 | MS-Gamification - Finalização | ✅ Concluído |
| 4 | 1-3 | MS-Monetization - Ads e Rewards | ✅ Concluído |
| 4 | 4-5 | Documentação com Swagger/OpenAPI | ✅ Concluído |
| 4 | 6-7 | Testes Automatizados | 🔄 Em progresso |
| 5 | 1-2 | Testes de Carga | 🔲 Não iniciado |
| 5 | 3-4 | Revisão Final e Ajustes | 🔲 Não iniciado |

## Legenda de Status
- 🔲 Não iniciado
- 🔄 Em progresso
- ✅ Concluído
- ⚠️ Com problemas

## Atribuições e Responsabilidades

| Área | Responsáveis |
|------|--------------|
| Desenvolvimento Backend | [Nome do Desenvolvedor Backend] |
| DevOps | [Nome do Responsável DevOps] |
| QA/Testes | [Nome do Responsável QA] |
| Revisão | [Nome do Revisor] |

## Critérios de Aceitação

Para cada endpoint implementado, os seguintes critérios devem ser atendidos:

1. **Contrato de API**: Endpoint deve seguir exatamente o formato esperado pelo frontend
2. **Documentação**: Endpoint deve estar documentado via Swagger/OpenAPI
3. **Testes**: Deve ter cobertura de testes unitários e de integração
4. **Segurança**: Deve implementar autenticação e autorização adequadas
5. **Performance**: Deve responder dentro dos limites de tempo definidos (< 500ms)

## Acompanhamento e Relatórios

Reuniões diárias de acompanhamento às 10:00, com duração máxima de 15 minutos.
Relatório semanal de progresso às sextas-feiras às 16:00.

## Dependências e Possíveis Riscos

1. **Acesso a API de terceiros**: Dependência para obtenção de dados bíblicos pode gerar atrasos
2. **Integração com Elastic Stack**: Configuração pode ser complexa e exigir ajustes
3. **Performance do MS-Bible**: Grande volume de dados bíblicos pode exigir otimizações adicionais
4. **Integração entre microsserviços**: Comunicação entre serviços pode exigir ajustes no RabbitMQ

## Próximos Passos após Conclusão

1. Iniciar a Fase 11 do Plano de Migração (Testes)
2. Implementar melhorias de observabilidade com métricas detalhadas
3. Criar ambientes de homologação e produção separados
4. Implementar pipeline de CI/CD completo para todos os microsserviços

## Configuração do Nginx para Comunicação entre Frontend e Microsserviços

O Nginx atua como um proxy reverso essencial na arquitetura do sistema FaleComJesus, sendo responsável por:

1. **Roteamento de Requisições**: Direciona as requisições do frontend para os microsserviços apropriados, baseado na URL.

2. **Resolução de CORS**: Implementa cabeçalhos CORS para permitir comunicação segura entre domínios.

3. **Terminação SSL**: Gerencia certificados SSL/TLS, permitindo comunicação segura via HTTPS.

4. **Load Balancing**: Capacidade de distribuir carga entre múltiplas instâncias de um mesmo microsserviço.

### Exemplo de Configuração

```nginx
# Configuração básica do servidor
server {
    listen 80;
    server_name falecomjesus.com;
    
    # Redirecionamento para HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name falecomjesus.com;
    
    # Configurações de SSL
    ssl_certificate /etc/nginx/ssl/falecomjesus.crt;
    ssl_certificate_key /etc/nginx/ssl/falecomjesus.key;
    
    # Frontend (SPA)
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    
    # Roteamento para microsserviços
    location /api/auth/ {
        proxy_pass http://ms-auth:5000/api/auth/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/study/ {
        proxy_pass http://ms-study:5000/api/study/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/chat/ {
        proxy_pass http://ms-chatia:5000/api/chat/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/bible/ {
        proxy_pass http://ms-bible:5000/api/bible/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/gamification/ {
        proxy_pass http://ms-gamification:5000/api/gamification/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/monetization/ {
        proxy_pass http://ms-monetization:5000/api/monetization/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        # Timeout estendido para webhooks de pagamento
        proxy_connect_timeout 90s;
        proxy_send_timeout 90s;
        proxy_read_timeout 90s;
    }
    
    location /api/admin/ {
        proxy_pass http://ms-admin:5000/api/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Aspectos de Segurança Implementados

1. **HTTP → HTTPS**: Redirecionamento automático para HTTPS para garantir comunicação segura.

2. **Headers de Segurança**:
   - `X-Frame-Options`: Protege contra clickjacking
   - `X-Content-Type-Options`: Previne MIME type sniffing
   - `Content-Security-Policy`: Controla quais recursos o navegador pode carregar

3. **Rate Limiting**:
   - Limitação de requisições por IP para prevenir ataques de DDoS
   - Configuração especial para APIs sensíveis como autenticação

4. **Timeouts Ajustados**:
   - Timeouts especiais para webhooks de pagamento no ms-monetization
   - Timeouts padrão para requisições regulares

### Manutenção e Monitoramento

- Os logs do Nginx são enviados para o Elastic Stack para análise
- Monitoramento de tempo de resposta dos endpoints
- Alertas configurados para código de status 5xx
- Health checks implementados para todos os microsserviços

Este componente central da infraestrutura é essencial para o correto funcionamento do sistema e deve ser considerado um ponto crítico na arquitetura de microsserviços.

## Guia de Acesso e Operação

### Links de Acesso e Portas

| Serviço | URL de Acesso (Desenvolvimento) | URL de Acesso (Produção) | Porta Interna | Porta Mapeada |
|---------|----------------------------------|--------------------------|---------------|---------------|
| Frontend | http://localhost:3000 | https://falecomjesus.com | 80 | 3000 |
| MS-Auth | http://localhost:8001 | https://falecomjesus.com/api/auth | 5000 | 8001 |
| MS-Study | http://localhost:8002 | https://falecomjesus.com/api/study | 5000 | 8002 |
| MS-ChatIA | http://localhost:8003 | https://falecomjesus.com/api/chat | 5000 | 8003 |
| MS-Bible | http://localhost:8004 | https://falecomjesus.com/api/bible | 5000 | 8004 |
| MS-Gamification | http://localhost:8005 | https://falecomjesus.com/api/gamification | 5000 | 8005 |
| MS-Monetization | http://localhost:8006 | https://falecomjesus.com/api/monetization | 5000 | 8006 |
| MS-Admin | http://localhost:8007 | https://falecomjesus.com/api/admin | 5000 | 8007 |

#### URLs de Documentação

| Serviço | Swagger URL (Desenvolvimento) | Swagger URL (Produção) |
|---------|-------------------------------|------------------------|
| MS-Auth | http://localhost:8001/api/docs | https://falecomjesus.com/api/auth/docs |
| MS-Study | http://localhost:8002/api/docs | https://falecomjesus.com/api/study/docs |
| MS-ChatIA | http://localhost:8003/api/docs | https://falecomjesus.com/api/chat/docs |
| MS-Bible | http://localhost:8004/api/docs | https://falecomjesus.com/api/bible/docs |
| MS-Gamification | http://localhost:8005/api/docs | https://falecomjesus.com/api/gamification/docs |
| MS-Monetization | http://localhost:8006/api/docs | https://falecomjesus.com/api/monetization/docs |
| MS-Admin | http://localhost:8007/api/docs | https://falecomjesus.com/api/admin/docs |

#### Portas de Banco de Dados

| Banco de Dados | Porta Interna | Porta Mapeada |
|----------------|---------------|---------------|
| Auth DB | 5432 | 5431 |
| Study DB | 5432 | 5432 |
| Chat DB | 5432 | 5433 |
| Bible DB | 5432 | 5434 |
| Gamification DB | 5432 | 5435 |
| Admin DB | 5432 | 5436 |

#### Serviços Auxiliares

| Serviço | URL de Acesso | Porta |
|---------|---------------|-------|
| Redis | localhost:6379 | 6379 |
| RabbitMQ | http://localhost:15672 (UI) | 15672 |
| RabbitMQ | localhost:5672 (AMQP) | 5672 |
| Elasticsearch | http://localhost:9200 | 9200 |
| Kibana | http://localhost:5601 | 5601 |

### Inicialização dos Serviços

#### Inicialização Completa com Docker Compose

Para iniciar todos os serviços em ambiente de desenvolvimento:

```bash
# No diretório raiz do projeto
docker-compose -f infra/docker-compose.dev.yml up
```

Para iniciar em segundo plano:

```bash
docker-compose -f infra/docker-compose.dev.yml up -d
```

Para iniciar apenas serviços específicos:

```bash
docker-compose -f infra/docker-compose.dev.yml up ms-auth ms-study frontend
```

#### Inicialização Individual de Microsserviços (para desenvolvimento)

Para iniciar um microsserviço individualmente durante o desenvolvimento:

```bash
# Para MS-Auth
cd backend/ms-auth
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Para outros serviços (ajustar path e porta conforme necessário)
cd backend/ms-monetization
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8006
```

#### Inicialização em Produção

```bash
# Iniciar serviços em produção
docker-compose -f infra/docker-compose.prod.yml up -d

# Verificar logs
docker-compose -f infra/docker-compose.prod.yml logs -f

# Atualizar serviços (após um pull das alterações)
docker-compose -f infra/docker-compose.prod.yml build ms-auth ms-monetization
docker-compose -f infra/docker-compose.prod.yml up -d --no-deps ms-auth ms-monetization
```

### Versionamento

O projeto FaleComJesus segue a convenção de versionamento semântico (SemVer):

- **Formato**: MAJOR.MINOR.PATCH (Ex: 1.0.0)
- **MAJOR**: Mudanças incompatíveis com versões anteriores
- **MINOR**: Adição de funcionalidades retrocompatíveis
- **PATCH**: Correções de bugs retrocompatíveis

#### Fluxo de Git

- Branch `main`: Contém código de produção estável
- Branch `develop`: Branch de integração para desenvolvimento
- Branches de Feature: Nomeadas como `feature/nome-da-funcionalidade`
- Branches de Hotfix: Nomeadas como `hotfix/descricao-do-problema`

#### Convenções de Commit

O projeto segue o padrão de [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé(s) opcional(is)]
```

Tipos comuns:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Atualização de documentação
- `chore`: Tarefas de manutenção
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes

### Variáveis de Ambiente

Cada microsserviço possui seu próprio conjunto de variáveis de ambiente definidas em arquivos `.env`. Exemplos de arquivos `.env` são fornecidos como `.env.example` em cada diretório de microsserviço.

**Variáveis Críticas:**

- `SECRET_KEY`: Chave para assinatura de tokens JWT
- `DATABASE_URL`: String de conexão com o banco de dados
- `REDIS_URL`: URL para conexão com Redis
- `OPENAI_API_KEY`: Chave de API para o serviço da OpenAI
- `STRIPE_API_KEY` e `STRIPE_WEBHOOK_SECRET`: Credenciais para integração com Stripe
- `HOTMART_API_KEY` e `HOTMART_WEBHOOK_SECRET`: Credenciais para integração com Hotmart

### Backup e Restauração

#### Backup do Banco de Dados

```bash
# Backup de um banco de dados específico
docker-compose -f infra/docker-compose.prod.yml exec auth-db pg_dump -U auth_user auth_db > backup_auth_$(date +%Y%m%d).sql

# Script para backup de todos os bancos
./scripts/backup_all_dbs.sh
```

#### Restauração do Banco de Dados

```bash
# Restauração de banco de dados
cat backup_auth_20230329.sql | docker-compose -f infra/docker-compose.prod.yml exec -T auth-db psql -U auth_user auth_db
```

### Monitoramento e Logs

- **Logs de Aplicação**: Disponíveis através do Kibana (http://localhost:5601)
- **Logs de Containers**: Acessíveis via Docker:
  ```bash
  docker-compose -f infra/docker-compose.prod.yml logs -f ms-auth
  ```
- **Métricas de Sistema**: Monitoradas através do MS-Admin em http://localhost:8007/api/admin/metrics
- **Alertas**: Configurados no Elasticsearch para enviar notificações via email e Slack em caso de falhas

### Troubleshooting

#### Problemas Comuns e Soluções

1. **Erro de Conexão com o Banco de Dados**:
   - Verificar se o container do banco está em execução
   - Verificar as credenciais no arquivo `.env`
   - Verificar regras de firewall

2. **Erro de Autenticação**:
   - Verificar validade do token JWT
   - Garantir que o SECRET_KEY é o mesmo em todos os serviços
   - Verificar logs do MS-Auth para detalhes

3. **Problemas com Webhooks de Pagamento**:
   - Verificar logs do MS-Monetization
   - Confirmar que as chaves de webhook estão configuradas corretamente
   - Verificar se os timeouts do Nginx estão adequados

4. **Container não inicia**:
   - Verificar logs: `docker-compose logs ms-auth`
   - Verificar se as dependências estão instaladas
   - Verificar se as variáveis de ambiente estão configuradas

Para qualquer outro problema, consultar a wiki interna ou abrir uma issue no repositório do projeto. 