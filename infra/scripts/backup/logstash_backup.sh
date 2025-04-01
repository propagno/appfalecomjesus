#!/bin/bash

# Script de Backup do Logstash do FaleComJesus

# Configurações
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
BACKUP_DIR="/backup/logstash"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Função para criar backup
create_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando backup do Logstash..." >> $BACKUP_DIR/backup.log
    
    # Parar o Logstash para garantir consistência
    docker-compose -f $DOCKER_COMPOSE_FILE stop logstash
    
    # Copiar arquivos de configuração e dados
    docker-compose -f $DOCKER_COMPOSE_FILE cp logstash:/usr/share/logstash/config $BACKUP_DIR/config_$DATE
    docker-compose -f $DOCKER_COMPOSE_FILE cp logstash:/usr/share/logstash/pipeline $BACKUP_DIR/pipeline_$DATE
    docker-compose -f $DOCKER_COMPOSE_FILE cp logstash:/var/log/logstash $BACKUP_DIR/logs_$DATE
    
    # Reiniciar o Logstash
    docker-compose -f $DOCKER_COMPOSE_FILE start logstash
    
    # Verificar se o backup foi criado
    if [ -d "$BACKUP_DIR/config_$DATE" ] && [ -d "$BACKUP_DIR/pipeline_$DATE" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup concluído com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Falha ao criar backup" >> $BACKUP_DIR/backup.log
        echo "ERRO: Falha ao criar backup do Logstash" | mail -s "Erro no Backup - Logstash" admin@falecomjesus.com
    fi
}

# Função para compactar backup
compress_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactando backup..." >> $BACKUP_DIR/backup.log
    
    # Compactar diretórios de backup
    tar -czf $BACKUP_DIR/logstash_backup_$DATE.tar.gz -C $BACKUP_DIR config_$DATE pipeline_$DATE logs_$DATE
    
    # Remover diretórios originais após compactação
    rm -rf $BACKUP_DIR/config_$DATE $BACKUP_DIR/pipeline_$DATE $BACKUP_DIR/logs_$DATE
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Compactação concluída" >> $BACKUP_DIR/backup.log
}

# Função para limpar backups antigos
cleanup_old_backups() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Removendo backups antigos..." >> $BACKUP_DIR/backup.log
    
    # Remover backups antigos
    find $BACKUP_DIR -name "logstash_backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Limpeza de backups antigos concluída" >> $BACKUP_DIR/backup.log
}

# Função para verificar espaço em disco
check_disk_space() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando espaço em disco..." >> $BACKUP_DIR/backup.log
    
    # Verificar espaço disponível
    available_space=$(df -h $BACKUP_DIR | awk 'NR==2 {print $4}' | sed 's/G//')
    
    if (( $(echo "$available_space < 5" | bc -l) )); then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ALERTA: Espaço em disco baixo ($available_space GB)" >> $BACKUP_DIR/backup.log
        echo "ALERTA: Espaço em disco baixo para backups do Logstash ($available_space GB)" | mail -s "Alerta de Espaço - Logstash" admin@falecomjesus.com
    fi
    
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Espaço disponível: $available_space GB" >> $BACKUP_DIR/backup.log
}

# Função para verificar integridade do backup
verify_backup() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Verificando integridade do backup..." >> $BACKUP_DIR/backup.log
    
    # Descompactar backup temporariamente
    mkdir -p $BACKUP_DIR/temp_verify
    tar -xzf $BACKUP_DIR/logstash_backup_$DATE.tar.gz -C $BACKUP_DIR/temp_verify
    
    # Verificar arquivos essenciais
    if [ -f "$BACKUP_DIR/temp_verify/config_$DATE/logstash.yml" ] && \
       [ -f "$BACKUP_DIR/temp_verify/pipeline_$DATE/logstash.conf" ]; then
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup verificado com sucesso" >> $BACKUP_DIR/backup.log
    else
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Backup inválido" >> $BACKUP_DIR/backup.log
        echo "ERRO: Backup do Logstash inválido" | mail -s "Erro na Verificação - Logstash" admin@falecomjesus.com
    fi
    
    # Remover diretório temporário
    rm -rf $BACKUP_DIR/temp_verify
}

# Executar backup
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Iniciando processo de backup do Logstash..." >> $BACKUP_DIR/backup.log

check_disk_space
create_backup
verify_backup
compress_backup
cleanup_old_backups

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Processo de backup do Logstash concluído" >> $BACKUP_DIR/backup.log 