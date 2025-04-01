# Hook useApi

Este hook facilita o consumo das APIs do sistema com gerenciamento automático de estados de loading e erro. Ele simplifica o código dos componentes e provê uma interface consistente para trabalhar com requisições assíncronas.

## Funcionalidades

- Gerenciamento automático de estados (loading, error, success)
- Manipulação padronizada de erros
- Callbacks para sucesso e erro
- Helpers para verificar o estado atual da requisição

## Como Usar

### Uso Básico

```tsx
import { useApi } from 'shared/hooks/useApi';
import { authApi } from 'shared/services/api';

function LoginForm() {
  const { execute: login, loading, error, data } = useApi(
    (email, password) => authApi.post('/login', { email, password })
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const email = formData.get('email');
    const password = formData.get('password');
    
    await login(email, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <div className="error">{error.message}</div>}
      {data && <div className="success">Login realizado com sucesso!</div>}
      
      <input name="email" type="email" placeholder="Email" />
      <input name="password" type="password" placeholder="Senha" />
      
      <button type="submit" disabled={loading}>
        {loading ? 'Entrando...' : 'Entrar'}
      </button>
    </form>
  );
}
```

### Com Callbacks

```tsx
import { useApi } from 'shared/hooks/useApi';
import { studyApi } from 'shared/services/api';
import { useNavigate } from 'react-router-dom';

function CompleteStudyButton({ studyId }) {
  const navigate = useNavigate();
  
  const { execute: completeStudy, loading } = useApi(
    () => studyApi.post(`/progress/${studyId}/complete`),
    {
      onSuccess: () => {
        // Redireciona após completar o estudo
        navigate('/studies/completed');
      },
      onError: (error) => {
        // Exibe notificação de erro
        toast.error(error.message);
      }
    }
  );

  return (
    <button 
      onClick={() => completeStudy()} 
      disabled={loading}
    >
      {loading ? 'Salvando...' : 'Marcar como Concluído'}
    </button>
  );
}
```

### Verificando Estados

```tsx
import { useApi } from 'shared/hooks/useApi';
import { bibleApi } from 'shared/services/api';

function BibleVerses({ chapterId }) {
  const { 
    execute: fetchVerses, 
    isLoading, 
    isError, 
    isSuccess, 
    data: verses, 
    error 
  } = useApi(() => bibleApi.get(`/chapters/${chapterId}/verses`));

  useEffect(() => {
    if (chapterId) {
      fetchVerses();
    }
  }, [chapterId, fetchVerses]);

  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorMessage message={error?.message} />;
  if (isSuccess) {
    return (
      <div>
        {verses.map(verse => (
          <p key={verse.id}>{verse.number}. {verse.text}</p>
        ))}
      </div>
    );
  }
  
  return null;
}
```

## API Completa

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| apiFunction | (...params: P[]) => Promise<T> | Função que faz a chamada à API |
| options | UseApiOptions | Opções para personalizar o comportamento |

### Opções

| Opção | Tipo | Default | Descrição |
|-------|------|---------|-----------|
| onSuccess | (data: T) => void | undefined | Callback executado quando a requisição for bem-sucedida |
| onError | (error: ApiError) => void | undefined | Callback executado quando ocorrer um erro |
| resetOnExecute | boolean | true | Se true, limpa dados e erros antes de nova execução |

### Retorno

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| data | T \| null | Dados retornados pela API ou null |
| loading | boolean | Se a requisição está em andamento |
| error | ApiError \| null | Objeto de erro ou null |
| execute | (...params: P[]) => Promise<T \| null> | Função para executar a requisição |
| reset | () => void | Função para resetar o estado (data, loading, error) |
| isIdle | boolean | Se ainda não houve requisição |
| isLoading | boolean | Se a requisição está em andamento |
| isError | boolean | Se ocorreu um erro |
| isSuccess | boolean | Se a requisição foi bem-sucedida | 