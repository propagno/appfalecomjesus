# MS-Monetization

Microsserviço responsável pela monetização do sistema FaleComJesus, incluindo gerenciamento de assinaturas, anúncios e recompensas.

## Configuração do Stripe

1. Crie uma conta no [Stripe](https://stripe.com)
2. Obtenha suas chaves de API no [Dashboard do Stripe](https://dashboard.stripe.com/apikeys)
3. Configure os produtos e preços no Stripe:
   - Crie um produto "FaleComJesus Premium"
   - Adicione dois preços:
     - Mensal (recurring, monthly)
     - Anual (recurring, yearly)
4. Configure o webhook no Stripe:
   - Vá para [Webhooks](https://dashboard.stripe.com/webhooks)
   - Adicione um endpoint: `https://seu-dominio.com/api/v1/webhook/stripe`
   - Selecione os eventos:
     - `checkout.session.completed`
     - `customer.subscription.deleted`
   - Copie o "Signing secret"

## Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_MONTHLY=price_...
STRIPE_PRICE_ID_YEARLY=price_...
```

## Banco de Dados

### Executando as Migrations

1. Certifique-se de que o PostgreSQL está rodando
2. Execute as migrations:
```bash
# Linux/Mac
./scripts/run_migrations.sh

# Windows
.\scripts\run_migrations.ps1
```

### Populando o Banco de Dados

Para popular o banco com dados iniciais (planos, assinaturas de exemplo, etc):
```bash
python scripts/seed_database.py
```

## Testando a Integração

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Teste a criação de uma sessão de checkout:
```bash
python scripts/test_stripe.py checkout
```

3. Teste a verificação de webhook:
```bash
python scripts/test_stripe.py webhook
```

## Endpoints

### Checkout

- `POST /api/v1/checkout`: Cria uma sessão de checkout
- `GET /api/v1/checkout/{session_id}`: Verifica o status do pagamento
- `POST /api/v1/cancel-subscription`: Cancela a assinatura atual

### Webhook

- `POST /api/v1/webhook/stripe`: Recebe webhooks do Stripe

### Planos

- `GET /api/v1/plans`: Lista todos os planos disponíveis
- `GET /api/v1/plans/{plan_id}`: Obtém detalhes de um plano específico
- `GET /api/v1/plans/compare`: Compara os planos disponíveis

### Assinaturas

- `GET /api/v1/subscription/status`: Obtém o status da assinatura do usuário
- `POST /api/v1/subscription/webhook`: Webhook para notificações de pagamento

### Recompensas por Anúncios

- `POST /api/v1/ad-rewards`: Registra uma recompensa por visualização de anúncio
- `GET /api/v1/ad-rewards`: Lista as recompensas por anúncios do usuário

## Segurança

- Todas as chaves do Stripe são armazenadas em variáveis de ambiente
- Webhooks são verificados com assinatura
- Tokens JWT são usados para autenticação
- Dados sensíveis são criptografados

## Monitoramento

- Logs de transações são salvos no banco de dados
- Erros são registrados com detalhes para debugging
- Métricas de conversão são coletadas

## Próximos Passos

1. Implementar integração com Hotmart
2. Adicionar mais métodos de pagamento
3. Implementar sistema de cupons
4. Adicionar relatórios financeiros 