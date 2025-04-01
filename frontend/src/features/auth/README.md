# Módulo de Autenticação - FaleComJesus

O módulo de autenticação do FaleComJesus foi projetado para proporcionar uma experiência de login, registro e gerenciamento de conta com visual acolhedor e inspirador, seguindo a temática espiritual do aplicativo.

## Componentes Atualizados

Os componentes de autenticação foram refatorados para usar um novo tema visual com cores, tipografia e elementos visuais que transmitem paz, acolhimento e espiritualidade.

### FormContainer

O `FormContainer` é o componente principal para envolver formulários de autenticação, proporcionando uma experiência visual consistente.

```tsx
import { FormContainer } from '../components';

// Uso básico
<FormContainer
  title="FaleComJesus"
  subtitle="Acesse sua conta"
  verse={{
    text: "O Senhor é meu pastor e nada me faltará.",
    reference: "Salmos 23:1"
  }}
  backLink={{
    to: "/login",
    label: "Voltar para o login"
  }}
>
  {/* Seu formulário aqui */}
</FormContainer>
```

#### Propriedades

- `title` (opcional): Título principal (padrão: "FaleComJesus")
- `subtitle` (opcional): Subtítulo ou instrução
- `verse` (opcional): Objeto com `text` e `reference` para exibir um versículo bíblico
- `backLink` (opcional): Objeto com `to` e `label` para criar um link de retorno
- `children`: Conteúdo do formulário

### Componentes UI Compartilhados

Os formulários utilizam componentes compartilhados do diretório `shared/components/ui`:

- `Button`: Botão estilizado com diferentes variantes
- `Input`: Campo de entrada com ícone, mensagem de erro e texto auxiliar
- `Card`: Container para seções de conteúdo
- `Checkbox`: Caixa de seleção estilizada

## Páginas Atualizadas

As seguintes páginas foram atualizadas com o novo tema espiritual:

1. **LoginPage**: Página de login com versículo inspirador
2. **RegisterPage**: Página de cadastro com explicação da jornada espiritual
3. **ForgotPasswordPage**: Recuperação de senha com mensagem de conforto
4. **ResetPasswordPage**: Redefinição de senha com tema espiritual
5. **ProfilePage**: Gerenciamento de perfil do usuário

## Formulários Atualizados

Os formulários também foram redesenhados:

1. **LoginForm**: Login com email/senha
2. **RegisterForm**: Cadastro de novos usuários
3. **ForgotPasswordForm**: Solicitação de recuperação de senha
4. **ResetPasswordForm**: Definição de nova senha
5. **ProfileForm**: Atualização de dados do usuário

## Ícones SVG Inline

Foram implementados ícones SVG inline para melhorar a experiência visual:

- Ícones de usuário
- Ícones de e-mail
- Ícones de cadeado
- Ícones de chave

## Tema Visual

### Cores

As cores seguem a paleta do tema espiritual:

- `spirit-blue`: Tons de azul para transmitir paz e tranquilidade
- `spirit-earth`: Tons terrosos para estabilidade e conexão
- `spirit-gold`: Tons dourados para elementos espirituais e destaque
- `spirit-red`: Tons vermelhos para alertas e erros

### Tipografia

- `font-heading`: Fonte para títulos e cabeçalhos
- `font-body`: Fonte para textos e conteúdos

## Arquivos Modificados

- `components/LoginForm.tsx`
- `components/RegisterForm.tsx`
- `components/ForgotPasswordForm.tsx`
- `components/ResetPasswordForm.tsx`
- `components/ProfileForm.tsx`
- `components/UserMenu.tsx`
- `components/FormContainer.tsx` (novo)
- `pages/LoginPage.tsx`
- `pages/RegisterPage.tsx`
- `pages/ForgotPasswordPage.tsx`
- `pages/ResetPasswordPage.tsx`
- `pages/ProfilePage.tsx`

## Benefícios da Nova Interface

1. **Experiência visual coesa**: Todos os componentes de autenticação seguem o mesmo padrão visual.
2. **Tema espiritual**: Incorpora elementos visuais que remetem à espiritualidade e bem-estar.
3. **Versículos incorporados**: Cada etapa do processo inclui versículos ou mensagens inspiradoras.
4. **Acessibilidade**: Estrutura semântica e contraste adequado para melhor leitura.
5. **Responsividade**: Design adaptável para diferentes tamanhos de tela.

## Como Contribuir

Para expandir ou modificar os componentes de autenticação:

1. Mantenha a consistência visual com o tema espiritual.
2. Utilize os componentes UI compartilhados sempre que possível.
3. Adicione versículos relevantes para cada contexto de uso.
4. Teste em diferentes tamanhos de tela para garantir responsividade.

## Estrutura

```
auth/
├── api/             # Serviços para comunicação com a API
├── components/      # Componentes específicos da autenticação
├── contexts/        # Contexto global de autenticação
├── hooks/           # Hooks customizados
├── pages/           # Páginas relacionadas à autenticação
└── types/           # Tipos e interfaces
```

## Fluxo Principal

1. Usuário realiza login ou registro
2. Token JWT é armazenado como cookie HttpOnly 
3. Dados do usuário são carregados
4. Componente ProtectedRoute controla acesso às rotas

## Funcionalidades

- Login / Logout
- Registro de novo usuário
- Recuperação de senha
- Gerenciamento de preferências (onboarding)
- Atualização de perfil
- Exclusão de conta

## Uso do Contexto

```tsx
import { useAuth } from 'features/auth';

function MeuComponente() {
  const { user, login, logout, isAuthenticated } = useAuth();
  
  // Agora você tem acesso a todas as funcionalidades de autenticação
}
```

## Proteção de Rotas

```tsx
import { ProtectedRoute } from 'features/auth';

<Route 
  path="/rota-privada" 
  element={
    <ProtectedRoute>
      <MinhaPaginaPrivada />
    </ProtectedRoute>
  } 
/>
```

## Integração com Backend

Este módulo se comunica com as seguintes rotas de API:

- POST /api/auth/login
- POST /api/auth/register
- POST /api/auth/logout
- GET /api/auth/user
- POST /api/auth/refresh
- POST /api/auth/preferences
- PUT /api/auth/user
- DELETE /api/auth/user
- POST /api/auth/forgot-password
- POST /api/auth/reset-password 