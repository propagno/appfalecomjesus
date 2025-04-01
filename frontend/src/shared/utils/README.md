# Utilitários Compartilhados

Este diretório contém utilitários que podem ser reutilizados em todo o aplicativo, proporcionando funcionalidades comuns de forma consistente.

## Utilitários disponíveis

### `auth.ts` - Funções de autenticação

Um conjunto de utilitários para gerenciar a autenticação e autorização no aplicativo.

```typescript
import auth from 'shared/utils/auth';

// Verificar se o usuário está autenticado
if (auth.isAuthenticated()) {
  // ...
}

// Verificar se o usuário é administrador
if (auth.isAdmin()) {
  // ...
}

// Armazenar dados do usuário após login
auth.storeUserData(userData);

// Obter dados do usuário atual
const user = auth.getUserData();

// Limpar dados de autenticação (logout)
auth.clearAuth();

// Validar dados de formulário
const emailValido = auth.isValidEmail('usuario@exemplo.com');
const senhaValida = auth.isValidPassword('Senha123');
const erroSenha = auth.getPasswordValidationError('senha123');
```

### `cache.ts` - Armazenamento em cache local

Um sistema de cache flexível que suporta localStorage e IndexedDB.

```typescript
import { cache } from 'shared/utils/cache';

// Armazenar dados no cache (com TTL padrão de 1 hora)
await cache.set('livros-biblia', livros);

// Armazenar com TTL personalizado (30 minutos)
await cache.set('versiculos-recentes', versiculos, 30 * 60 * 1000);

// Recuperar dados do cache
const livros = await cache.get('livros-biblia');

// Remover item do cache
await cache.remove('versiculos-recentes');

// Limpar todo o cache
await cache.clear();

// Remover apenas itens expirados
await cache.clearExpired();
```

Para casos mais específicos, você pode criar uma nova instância com configurações personalizadas:

```typescript
import LocalCache from 'shared/utils/cache';

// Cache de longa duração (1 dia) usando IndexedDB
const bibliaCache = new LocalCache({
  ttl: 24 * 60 * 60 * 1000, // 1 dia
  prefix: 'fcj_biblia_',
  storageType: 'indexedDB',
  dbName: 'BibleCache'
});

// Armazenar no cache personalizado
await bibliaCache.set('genesis', dadosGenesis);
```

## Boas práticas

1. **Padronize o uso de utilitários**:
   - Use estas funções em vez de reimplementar a mesma lógica em vários lugares.
   - Evite acessar diretamente localStorage ou IndexedDB - use os utilitários de cache.

2. **Cache sensível ao contexto**:
   - Para dados frequentemente acessados e que mudam raramente (como livros da Bíblia), use TTL longo.
   - Para dados que mudam com frequência (como progresso do usuário), use TTL curto ou evite o cache.

3. **Autenticação consistente**:
   - Para rotas protegidas, sempre verifique `auth.isAuthenticated()`.
   - Para validar permissões, use `auth.hasRole()` ou `auth.isAdmin()`.

4. **Extensibilidade**:
   - Se precisar de um novo utilitário comum, adicione a este diretório, seguindo o mesmo padrão.
   - Documente qualquer novo utilitário neste README. 