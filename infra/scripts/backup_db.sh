#!/bin/bash

# Configurações
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_NAME="ms_chatia"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="localhost"
DB_PORT="5432"

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Nome do arquivo de backup
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"

# Executar backup
echo "Iniciando backup do banco de dados $DB_NAME..."
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > $BACKUP_FILE

# Verificar se o backup foi bem sucedido
if [ $? -eq 0 ]; then
    echo "Backup concluído com sucesso!"
    echo "Arquivo de backup: $BACKUP_FILE"
    
    # Compactar o backup
    gzip $BACKUP_FILE
    echo "Backup compactado: ${BACKUP_FILE}.gz"
    
    # Manter apenas os últimos 7 backups
    ls -t $BACKUP_DIR/*.gz | tail -n +8 | xargs -r rm
    echo "Backups antigos removidos"
else
    echo "Erro ao realizar backup!"
    exit 1
fi 