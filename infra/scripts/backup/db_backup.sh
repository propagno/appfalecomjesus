#!/bin/bash

# Script de Backup para Bancos de Dados do FaleComJesus

# Configurações
BACKUP_DIR="/backup/databases"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Função para backup de um banco específico
backup_database() {
    local DB_NAME=$1
    local DB_USER=$2
    local DB_PASSWORD=$3
    local DB_HOST=$4
    local DB_PORT=$5

    echo "Iniciando backup do banco $DB_NAME..."

    # Backup do banco
    PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -F c -f "$BACKUP_DIR/${DB_NAME}_${DATE}.backup"

    if [ $? -eq 0 ]; then
        echo "Backup do banco $DB_NAME concluído com sucesso!"
    else
        echo "Erro ao fazer backup do banco $DB_NAME"
        exit 1
    fi
}

# Backup dos bancos
backup_database "auth_db" "auth_user" "$AUTH_DB_PASSWORD" "auth-db" "5432"
backup_database "study_db" "study_user" "$STUDY_DB_PASSWORD" "study-db" "5432"
backup_database "chat_db" "chat_user" "$CHAT_DB_PASSWORD" "chat-db" "5432"
backup_database "bible_db" "bible_user" "$BIBLE_DB_PASSWORD" "bible-db" "5432"
backup_database "gamification_db" "gamification_user" "$GAMIFICATION_DB_PASSWORD" "gamification-db" "5432"
backup_database "admin_db" "admin_user" "$ADMIN_DB_PASSWORD" "admin-db" "5432"

# Compactar backups
echo "Compactando backups..."
tar -czf "$BACKUP_DIR/backup_${DATE}.tar.gz" "$BACKUP_DIR"/*.backup

# Remover arquivos .backup após compactação
rm "$BACKUP_DIR"/*.backup

# Remover backups antigos
echo "Removendo backups mais antigos que $RETENTION_DAYS dias..."
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Verificar espaço em disco
echo "Verificando espaço em disco..."
df -h $BACKUP_DIR

echo "Backup concluído com sucesso!" 