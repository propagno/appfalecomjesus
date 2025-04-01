# Testes Automatizados - MS-Auth

Este diretório contém testes unitários e de integração para o microsserviço de autenticação (MS-Auth).

## Estrutura de Diretórios

```
tests/
├── conftest.py         # Configurações e fixtures globais
├── unit/               # Testes unitários
│   └── test_*.py       # Arquivos de teste para componentes individuais
├── integration/        # Testes de integração
│   └── test_*.py       # Testes que exercitam APIs e componentes conectados
└── README.md           # Este arquivo
```

## Tipos de Testes

### Testes Unitários

Testes focados em componentes individuais (funções, classes) isolados do resto do sistema. Estes testes são rápidos e ajudam a identificar problemas em funções específicas.

Exemplos:
- Testes de funções de autenticação
- Testes de modelos e schemas
- Testes de utilitários

### Testes de Integração

Testes que verificam a interação entre componentes do sistema. Exercitam APIs completas e verificam o funcionamento do sistema como um todo.

Exemplos: 
- Testes de rotas da API
- Testes com banco de dados
- Testes de comunicação entre serviços

## Executando os Testes

### Pré-requisitos

- Python 3.9+
- Dependências instaladas (`pip install -r requirements.txt`)

### Comando para Executar Todos os Testes

```bash
# No Linux/Mac
./run_tests.sh

# No Windows
run_tests.bat
```

### Executar Apenas Testes Unitários

```bash
python -m pytest tests/unit -v
```

### Executar Apenas Testes de Integração

```bash
python -m pytest tests/integration -v
```

### Executar com Relatório de Cobertura

```bash
python -m pytest --cov=app --cov-report=term --cov-report=html
```

Após executar o comando acima, um relatório de cobertura será gerado na pasta `htmlcov/`. Abra o arquivo `index.html` para visualizar os resultados.

### Executar Testes por Marcadores

```bash
# Apenas testes marcados como "auth"
python -m pytest -m auth

# Excluir testes lentos
python -m pytest -m "not slow"
```

## Boas Práticas para Testes

1. **Mantenha os testes independentes**: Cada teste deve poder ser executado isoladamente.

2. **Utilize fixtures para código repetitivo**: Use as fixtures do pytest para reutilizar código.

3. **Organize os testes com descritores claros**: Use nomes descritivos para funções de teste.

4. **Siga o padrão AAA (Arrange, Act, Assert)**:
   - Arrange: Configure o contexto do teste
   - Act: Execute a ação a ser testada
   - Assert: Verifique os resultados

5. **Mocking quando necessário**: Use mock para simular comportamentos externos.

6. **Mantenha testes rápidos**: Testes lentos devem ser marcados com `@pytest.mark.slow`.

## Convenções de Nomenclatura

- Arquivos de teste: `test_*.py`
- Funções de teste: `test_*`
- Classes de teste: `Test*`

## Contribuição

Ao adicionar novos recursos, certifique-se de adicionar testes correspondentes. Mantenha a cobertura de código alta para garantir a qualidade do código. 