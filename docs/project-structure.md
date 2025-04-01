# Estrutura do Projeto FaleComJesus

## Visão Geral
O FaleComJesus é uma plataforma de estudo bíblico personalizado que utiliza IA para criar uma experiência única e adaptada para cada usuário.

## Estrutura de Diretórios

### Frontend
```
frontend/
├── src/
│   ├── components/     # Componentes React reutilizáveis
│   ├── pages/         # Páginas da aplicação
│   ├── services/      # Serviços de API
│   ├── contexts/      # Contextos React
│   ├── hooks/         # Hooks personalizados
│   ├── utils/         # Funções utilitárias
│   ├── types/         # Definições de tipos TypeScript
│   ├── styles/        # Estilos globais e temas
│   └── assets/        # Recursos estáticos
```

### Backend
```
backend/
├── ms-auth/           # Microsserviço de autenticação
├── ms-study/          # Microsserviço de planos de estudo
├── ms-chatia/         # Microsserviço de chat com IA
├── ms-bible/          # Microsserviço de conteúdo bíblico
├── ms-gamification/   # Microsserviço de gamificação
├── ms-monetization/   # Microsserviço de monetização
└── ms-admin/          # Microsserviço administrativo
```

## Microsserviços

### MS-Auth
- Autenticação e autorização
- Gerenciamento de usuários
- JWT e cookies seguros

### MS-Study
- Gerenciamento de planos de estudo
- Geração de certificados
- Progresso do usuário

### MS-ChatIA
- Integração com OpenAI
- Histórico de conversas
- Limites de uso por plano

### MS-Bible
- Base de dados bíblica
- Busca e navegação
- Versículos e temas

### MS-Gamification
- Sistema de pontos
- Conquistas e selos
- Certificados de conclusão

### MS-Monetization
- Planos e assinaturas
- Integração com gateways de pagamento
- Sistema de recompensas por anúncios

### MS-Admin
- Dashboard administrativo
- Métricas e relatórios
- Gerenciamento de conteúdo

## Infraestrutura

### Docker
- Containers para cada microsserviço
- NGINX como proxy reverso
- Redis para cache
- PostgreSQL para bancos de dados

### Monitoramento
- Elastic Stack (ELK)
- Logs centralizados
- Métricas e alertas

### Segurança
- HTTPS/TLS
- JWT em cookies HttpOnly
- CORS configurado
- Rate limiting

## Desenvolvimento

### Ambiente Local
1. Clonar o repositório
2. Copiar .env.example para .env
3. Executar `docker-compose up -d`
4. Acessar http://localhost:3000

### Testes
- Testes unitários com Jest
- Testes E2E com Cypress
- Cobertura mínima de 70%

### Deploy
- CI/CD com GitHub Actions
- Ambientes de staging e produção
- Deploy automatizado

## Manutenção

### Logs
- Logs estruturados em JSON
- Retenção de 30 dias
- Alertas configurados

### Backups
- Backup diário dos bancos
- Backup semanal completo
- Retenção de 7 dias

### Monitoramento
- Health checks
- Métricas de performance
- Alertas de erro

## Próximos Passos

### Curto Prazo
- Implementar testes E2E
- Melhorar documentação
- Otimizar performance

### Médio Prazo
- Adicionar mais recursos de gamificação
- Expandir integrações
- Melhorar UX/UI

### Longo Prazo
- Escalar para mais usuários
- Adicionar recursos premium
- Internacionalização 