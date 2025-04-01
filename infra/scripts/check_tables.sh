#!/bin/bash

# Configurações
DB_NAME="ms_chatia"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# Lista de tabelas necessárias
TABLES=(
    "chat_history"
)

# Função para verificar se uma tabela existe
check_table() {
    local table=$1
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$table');"
}

# Função para criar uma tabela
create_table() {
    local table=$1
    echo "Criando tabela $table..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "sql/create_${table}.sql"
}

# Verificar cada tabela
for table in "${TABLES[@]}"; do
    echo "Verificando tabela $table..."
    exists=$(check_table "$table")
    
    if [ "$exists" = "f" ]; then
        echo "Tabela $table não existe. Criando..."
        create_table "$table"
    else
        echo "Tabela $table já existe."
    fi
done

echo "Verificação de tabelas concluída!" 