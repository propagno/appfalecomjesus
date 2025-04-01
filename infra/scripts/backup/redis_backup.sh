#!/bin/bash

# Script de Backup do Redis do FaleComJesus

# Configurações
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
BACKUP_DIR="/backup/redis"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Função para criar backup
create_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando backup do Redis..." >> $BACKUP_DIR/backup.log
    
    # Parar o Redis para garantir consistência
    docker-compose -f $DOCKER_COMPOSE_FILE stop redis
    
    # Copiar arquivo de dump
    docker-compose -f $DOCKER_COMPOSE_FILE cp redis:/data/dump.rdb $BACKUP_DIR/dump_$DATE.rdb
    
    # Reiniciar o Redis
    docker-compose -f $DOCKER_COMPOSE_FILE start redis
    
    # Verificar se o backup foi criado
    if [ -f "$BACKUP_DIR/dump_$DATE.rdb" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup concluído com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Falha ao criar backup" >> $BACKUP_DIR/backup.log
        echo "ERRO: Falha ao criar backup do Redis" | mail -s "Erro no Backup - Redis" admin@falecomjesus.com
    fi
}

# Função para compactar backup
compress_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactando backup..." >> $BACKUP_DIR/backup.log
    
    # Compactar arquivo de dump
    gzip $BACKUP_DIR/dump_$DATE.rdb
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactação concluída" >> $BACKUP_DIR/backup.log
}

# Função para limpar backups antigos
cleanup_old_backups() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Removendo backups antigos..." >> $BACKUP_DIR/backup.log
    
    # Remover backups antigos
    find $BACKUP_DIR -name "dump_*.rdb.gz" -mtime +$RETENTION_DAYS -delete
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Limpeza de backups antigos concluída" >> $BACKUP_DIR/backup.log
}

# Função para verificar espaço em disco
check_disk_space() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando espaço em disco..." >> $BACKUP_DIR/backup.log
    
    # Verificar espaço disponível
    available_space=$(df -h $BACKUP_DIR | awk 'NR==2 {print $4}' | sed 's/G//')
    
    if (( $(echo "$available_space < 5" | bc -l) )); then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ALERTA: Espaço em disco baixo ($available_space GB)" >> $BACKUP_DIR/backup.log
        echo "ALERTA: Espaço em disco baixo para backups do Redis ($available_space GB)" | mail -s "Alerta de Espaço - Redis" admin@falecomjesus.com
    fi
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Espaço disponível: $available_space GB" >> $BACKUP_DIR/backup.log
}

# Função para verificar integridade do backup
verify_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando integridade do backup..." >> $BACKUP_DIR/backup.log
    
    # Descompactar backup temporariamente
    gunzip -c $BACKUP_DIR/dump_$DATE.rdb.gz > $BACKUP_DIR/temp_dump.rdb
    
    # Verificar se o arquivo é um dump válido do Redis
    if redis-check-rdb $BACKUP_DIR/temp_dump.rdb > /dev/null 2>&1; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup verificado com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Backup inválido" >> $BACKUP_DIR/backup.log
        echo "ERRO: Backup do Redis inválido" | mail -s "Erro na Verificação - Redis" admin@falecomjesus.com
    fi
    
    # Remover arquivo temporário
    rm $BACKUP_DIR/temp_dump.rdb
}

# Executar backup
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando processo de backup do Redis..." >> $BACKUP_DIR/backup.log

check_disk_space
create_backup
verify_backup
compress_backup
cleanup_old_backups

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Processo de backup do Redis concluído" >> $BACKUP_DIR/backup.log 