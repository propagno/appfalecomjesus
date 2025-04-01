#!/bin/bash
set -e

# Check if DB_CHECK is explicitly set to 'false'
if [ "$DB_CHECK" = "false" ]; then
  echo "Skipping database check and migrations (DB_CHECK=false)"
else
  # Aguardar banco de dados
  echo "Esperando banco de dados..."
  until nc -z chat-db 5432; do
    sleep 0.5
  done
  echo "Banco de dados conectado!"

  # Executar migrações se necessário
  echo "Executando migrações..."
  python -m alembic upgrade head || echo "Sem migrações ou erro ao executar"
fi

# Iniciar aplicação
echo "Iniciando aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 5000 