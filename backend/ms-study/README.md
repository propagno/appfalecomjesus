# MS-Study: Microserviço de Estudos Bíblicos

Este microserviço é responsável por gerenciar planos de estudo bíblico personalizados, incluindo a criação, recuperação e atualização de planos de estudo, bem como o acompanhamento do progresso do usuário.

## Funcionalidades

- Geração de planos de estudo personalizados com base nas preferências do usuário
- Organização de planos em seções diárias e conteúdos
- Acompanhamento do progresso do usuário em cada plano
- Registro de reflexões e notas pessoais
- Integração com o serviço de IA para gerar conteúdo personalizado

## Tecnologias

- FastAPI: Framework web de alta performance
- SQLAlchemy: ORM para interação com o banco de dados
- Pydantic: Validação de dados e serialização
- httpx: Cliente HTTP assíncrono para comunicação com outros serviços

## Estrutura do Projeto

```
app/
├── api/
│   └── v1/
│       ├── dependencies.py
│       ├── routes.py
│       └── study.py
├── core/
│   └── config.py
├── domain/
│   └── study/
│       ├── models.py
│       ├── schemas.py
│       └── service.py
├── infrastructure/
│   └── database.py
└── main.py
```

## Instalação e Execução

### Requisitos

- Python 3.9+
- pip

### Configuração

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Configure as variáveis de ambiente:
   ```
   export DATABASE_URL=sqlite:///./study.db
   export SECRET_KEY=sua-chave-secreta
   export MS_CHATIA_URL=http://localhost:8003
   export SERVICE_API_KEY=chave-para-comunicação-entre-serviços
   ```

### Execução

```
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

### Docker

Para executar o serviço com Docker:

```
docker build -t ms-study .
docker run -p 8004:8004 --name ms-study ms-study
```

## Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | /api/v1/study/plans | Criar um novo plano de estudo |
| GET | /api/v1/study/plans | Obter todos os planos do usuário |
| GET | /api/v1/study/plans/{plan_id} | Obter um plano específico |
| GET | /api/v1/study/plans/{plan_id}/sections | Obter todas as seções de um plano |
| GET | /api/v1/study/sections/{section_id} | Obter uma seção específica |
| GET | /api/v1/study/sections/{section_id}/contents | Obter os conteúdos de uma seção |
| POST | /api/v1/study/progress | Atualizar o progresso do usuário |
| POST | /api/v1/study/reflections | Salvar uma reflexão do usuário |
| GET | /api/v1/study/plans/{plan_id}/progress | Obter o progresso do usuário em um plano |
| GET | /api/v1/study/daily-devotional | Obter um devocional diário |

## Integração com Outros Serviços

- **MS-Auth**: Autenticação e autorização dos usuários
- **MS-ChatIA**: Geração de conteúdo personalizado usando IA 