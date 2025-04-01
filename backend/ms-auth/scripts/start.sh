#!/bin/bash

# Função para verificar se o PostgreSQL está acessível
check_postgres() {
    echo "Verificando conexão com PostgreSQL..."
    while ! pg_isready -h auth-db -p 5432 -U postgres; do
        echo "Aguardando PostgreSQL..."
        sleep 2
    done
    echo "PostgreSQL está pronto!"
}

# Função para verificar se o Redis está acessível
check_redis() {
    echo "Verificando conexão com Redis..."
    while ! curl -s redis:6379 > /dev/null; do
        echo "Aguardando Redis..."
        sleep 2
    done
    echo "Redis está pronto!"
}

# Verificar dependências
echo "Verificando dependências do serviço..."
check_postgres
check_redis

# Iniciar a aplicação
echo "Iniciando MS-Auth..."
exec uvicorn main:app --host 0.0.0.0 --port 5000 --reload --log-level info 