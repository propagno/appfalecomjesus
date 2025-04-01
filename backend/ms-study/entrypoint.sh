#!/bin/bash
set -e

# Instalar netcat se necessário
apt-get update && apt-get install -y netcat-openbsd

# Definir o PYTHONPATH para encontrar os módulos
export PYTHONPATH=/app:$PYTHONPATH

# Define os valores padrão de conexão com o banco de dados
DB_HOST=${POSTGRES_HOST:-study-db}
DB_PORT=${POSTGRES_PORT:-5432}

# Aguardar PostgreSQL
echo "Esperando PostgreSQL iniciar em $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL iniciado com sucesso!"

# Pulando migrações devido a problemas com tabelas existentes
echo "AVISO: Pulando migrações do banco de dados devido a problemas conhecidos."
echo "As tabelas devem ser criadas manualmente ou corrigir o script de migração."

# Iniciar a aplicação
echo "Iniciando a aplicação..."
python -m uvicorn main:app --host 0.0.0.0 --port 5000

# Mantém o container rodando
exec "$@" 