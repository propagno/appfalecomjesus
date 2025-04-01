# Cliente API Centralizado

Este módulo implementa um cliente Axios centralizado para comunicação com os microsserviços do backend do FaleComJesus. O cliente gerencia automaticamente funcionalidades importantes como:

- Autenticação JWT com cookies HttpOnly
- Refresh token automático
- Retry automático para erros de rede
- Formatação consistente de erros
- Logging em produção

## Como usar

### Importação das instâncias pré-configuradas

```typescript
import { authApi, studyApi, chatApi, bibleApi, gamificationApi, monetizationApi, adminApi } from 'shared/services/api';

// Usando para autenticação
async function login(email: string, password: string) {
  try {
    const userData = await authApi.post('/login', { email, password });
    return userData;
  } catch (error) {
    // O erro já está formatado em um objeto ApiError
    console.error('Falha no login:', error.message);
    throw error;
  }
}

// Obtendo dados de estudo
async function getCurrentStudy() {
  try {
    return await studyApi.get('/current');
  } catch (error) {
    console.error('Erro ao obter estudo atual:', error.message);
    throw error;
  }
}
```

### Métodos disponíveis

Cada instância possui os seguintes métodos:

- **get<T>(url, config?)**: Para requisições GET
- **post<T>(url, data?, config?)**: Para requisições POST
- **put<T>(url, data?, config?)**: Para requisições PUT
- **delete<T>(url, config?)**: Para requisições DELETE
- **upload<T>(url, formData, config?)**: Para upload de arquivos

### Tratamento de erros

Os erros são padronizados no formato `ApiError`:

```typescript
interface ApiError {
  status: number;    // Código HTTP
  message: string;   // Mensagem amigável
  code?: string;     // Código de erro específico (opcional)
  details?: Record<string, any>; // Detalhes adicionais (opcional)
}
```

### Criação de novos clientes (caso necessário)

```typescript
import { createApiClient } from 'shared/services/api';

const customApi = createApiClient('https://api.external-service.com');
```

## Recursos implementados

1. **Autenticação com cookies HttpOnly**
   - Tokens JWT são gerenciados automaticamente via cookies
   - Não é necessário manipular tokens manualmente

2. **Refresh Token automático**
   - Em caso de erro 401, tenta renovar o token automaticamente
   - Requisição original é automaticamente repetida após o refresh
   - Todas as requisições pendentes são colocadas em fila e processadas após o refresh

3. **Retry automático para falhas de rede**
   - Tentativas automáticas para requisições GET que falham por problemas de rede
   - Implementa exponential backoff para evitar sobrecarga do servidor
   - Configurável via constantes MAX_RETRY_ATTEMPTS e RETRY_DELAY_MS

4. **Formatação consistente de erros**
   - Todos os erros são formatados no padrão ApiError
   - Mensagens amigáveis para erros comuns
   - Preservação de detalhes do erro quando disponíveis

5. **Logging em produção**
   - Registro detalhado de erros em ambiente de produção
   - Preparado para integração com serviços como Sentry (comentado no código)

## Considerações técnicas

- Os tokens JWT são gerenciados via cookies HttpOnly, o que melhora a segurança
- `withCredentials: true` é necessário para enviar/receber cookies em requisições cross-origin
- As URLs base são configuradas via variáveis de ambiente, com fallback para caminhos relativos 