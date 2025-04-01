#!/bin/bash

# Script de Backup do Elasticsearch do FaleComJesus

# Configurações
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
BACKUP_DIR="/backup/elasticsearch"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Função para criar backup
create_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando backup do Elasticsearch..." >> $BACKUP_DIR/backup.log
    
    # Parar o Elasticsearch para garantir consistência
    docker-compose -f $DOCKER_COMPOSE_FILE stop elasticsearch
    
    # Copiar arquivos de configuração e dados
    docker-compose -f $DOCKER_COMPOSE_FILE cp elasticsearch:/usr/share/elasticsearch/config $BACKUP_DIR/config_$DATE
    docker-compose -f $DOCKER_COMPOSE_FILE cp elasticsearch:/usr/share/elasticsearch/data $BACKUP_DIR/data_$DATE
    
    # Reiniciar o Elasticsearch
    docker-compose -f $DOCKER_COMPOSE_FILE start elasticsearch
    
    # Verificar se o backup foi criado
    if [ -d "$BACKUP_DIR/config_$DATE" ] && [ -d "$BACKUP_DIR/data_$DATE" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup concluído com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Falha ao criar backup" >> $BACKUP_DIR/backup.log
        echo "ERRO: Falha ao criar backup do Elasticsearch" | mail -s "Erro no Backup - Elasticsearch" admin@falecomjesus.com
    fi
}

# Função para compactar backup
compress_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactando backup..." >> $BACKUP_DIR/backup.log
    
    # Compactar diretórios de backup
    tar -czf $BACKUP_DIR/elasticsearch_backup_$DATE.tar.gz -C $BACKUP_DIR config_$DATE data_$DATE
    
    # Remover diretórios originais após compactação
    rm -rf $BACKUP_DIR/config_$DATE $BACKUP_DIR/data_$DATE
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactação concluída" >> $BACKUP_DIR/backup.log
}

# Função para limpar backups antigos
cleanup_old_backups() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Removendo backups antigos..." >> $BACKUP_DIR/backup.log
    
    # Remover backups antigos
    find $BACKUP_DIR -name "elasticsearch_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Limpeza de backups antigos concluída" >> $BACKUP_DIR/backup.log
}

# Função para verificar espaço em disco
check_disk_space() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando espaço em disco..." >> $BACKUP_DIR/backup.log
    
    # Verificar espaço disponível
    available_space=$(df -h $BACKUP_DIR | awk 'NR==2 {print $4}' | sed 's/G//')
    
    if (( $(echo "$available_space < 5" | bc -l) )); then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ALERTA: Espaço em disco baixo ($available_space GB)" >> $BACKUP_DIR/backup.log
        echo "ALERTA: Espaço em disco baixo para backups do Elasticsearch ($available_space GB)" | mail -s "Alerta de Espaço - Elasticsearch" admin@falecomjesus.com
    fi
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Espaço disponível: $available_space GB" >> $BACKUP_DIR/backup.log
}

# Função para verificar integridade do backup
verify_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando integridade do backup..." >> $BACKUP_DIR/backup.log
    
    # Descompactar backup temporariamente
    mkdir -p $BACKUP_DIR/temp_verify
    tar -xzf $BACKUP_DIR/elasticsearch_backup_$DATE.tar.gz -C $BACKUP_DIR/temp_verify
    
    # Verificar arquivos essenciais
    if [ -f "$BACKUP_DIR/temp_verify/config_$DATE/elasticsearch.yml" ] && \
       [ -d "$BACKUP_DIR/temp_verify/data_$DATE/nodes" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup verificado com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Backup inválido" >> $BACKUP_DIR/backup.log
        echo "ERRO: Backup do Elasticsearch inválido" | mail -s "Erro na Verificação - Elasticsearch" admin@falecomjesus.com
    fi
    
    # Remover diretório temporário
    rm -rf $BACKUP_DIR/temp_verify
}

# Executar backup
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando processo de backup do Elasticsearch..." >> $BACKUP_DIR/backup.log

check_disk_space
create_backup
verify_backup
compress_backup
cleanup_old_backups

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Processo de backup do Elasticsearch concluído" >> $BACKUP_DIR/backup.log 