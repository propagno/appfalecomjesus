#!/bin/bash

# Script de Limpeza e Manutenção do FaleComJesus

# Configurações
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
BACKUP_DIR="/backup"
LOG_DIR="/var/log/falecomjesus"
RETENTION_DAYS=7
DATE=$(date +%Y-%m-%d\ %H:%M:%S)

# Criar diretório de logs se não existir
mkdir -p $LOG_DIR

# Função para limpar logs antigos
cleanup_logs() {
    echo "[$DATE] Iniciando limpeza de logs..." >> $LOG_DIR/cleanup.log
    
    # Limpar logs do Nginx
    find /var/log/nginx -type f -name "*.log" -mtime +$RETENTION_DAYS -delete
    
    # Limpar logs do Docker
    find /var/lib/docker/containers -type f -name "*.log" -mtime +$RETENTION_DAYS -delete
    
    # Limpar logs da aplicação
    find $LOG_DIR -type f -name "*.log" -mtime +$RETENTION_DAYS -delete
    
    echo "[$DATE] Limpeza de logs concluída" >> $LOG_DIR/cleanup.log
}

# Função para limpar backups antigos
cleanup_backups() {
    echo "[$DATE] Iniciando limpeza de backups..." >> $LOG_DIR/cleanup.log
    
    # Limpar backups antigos
    find $BACKUP_DIR -type f -name "*.backup" -mtime +$RETENTION_DAYS -delete
    find $BACKUP_DIR -type f -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    echo "[$DATE] Limpeza de backups concluída" >> $LOG_DIR/cleanup.log
}

# Função para limpar imagens Docker não utilizadas
cleanup_docker() {
    echo "[$DATE] Iniciando limpeza do Docker..." >> $LOG_DIR/cleanup.log
    
    # Remover containers parados
    docker container prune -f
    
    # Remover imagens não utilizadas
    docker image prune -f
    
    # Remover volumes não utilizados
    docker volume prune -f
    
    # Remover networks não utilizadas
    docker network prune -f
    
    echo "[$DATE] Limpeza do Docker concluída" >> $LOG_DIR/cleanup.log
}

# Função para verificar e limpar cache do Redis
cleanup_redis() {
    echo "[$DATE] Iniciando limpeza do Redis..." >> $LOG_DIR/cleanup.log
    
    # Limpar cache expirado
    docker-compose -f $DOCKER_COMPOSE_FILE exec redis redis-cli FLUSHALL
    
    echo "[$DATE] Limpeza do Redis concluída" >> $LOG_DIR/cleanup.log
}

# Função para verificar e limpar filas do RabbitMQ
cleanup_rabbitmq() {
    echo "[$DATE] Iniciando limpeza do RabbitMQ..." >> $LOG_DIR/cleanup.log
    
    # Limpar filas vazias
    docker-compose -f $DOCKER_COMPOSE_FILE exec rabbitmq rabbitmqctl purge_queue study_events_queue
    docker-compose -f $DOCKER_COMPOSE_FILE exec rabbitmq rabbitmqctl purge_queue notification_queue
    
    echo "[$DATE] Limpeza do RabbitMQ concluída" >> $LOG_DIR/cleanup.log
}

# Função para verificar e limpar índices antigos do Elasticsearch
cleanup_elasticsearch() {
    echo "[$DATE] Iniciando limpeza do Elasticsearch..." >> $LOG_DIR/cleanup.log
    
    # Remover índices antigos
    docker-compose -f $DOCKER_COMPOSE_FILE exec elasticsearch curl -X DELETE "localhost:9200/logs-*?pretty" -H 'Content-Type: application/json'
    
    echo "[$DATE] Limpeza do Elasticsearch concluída" >> $LOG_DIR/cleanup.log
}

# Função para verificar e limpar tabelas temporárias dos bancos de dados
cleanup_databases() {
    echo "[$DATE] Iniciando limpeza dos bancos de dados..." >> $LOG_DIR/cleanup.log
    
    databases=("auth_db" "study_db" "chat_db" "bible_db" "gamification_db" "admin_db")
    
    for db in "${databases[@]}"; do
        echo "[$DATE] Limpando banco de dados: $db" >> $LOG_DIR/cleanup.log
        
        # Limpar tabelas temporárias
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T $db psql -U postgres -c "
            DROP TABLE IF EXISTS temp_sessions;
            DROP TABLE IF EXISTS temp_uploads;
            DROP TABLE IF EXISTS temp_cache;
        "
    done
    
    echo "[$DATE] Limpeza dos bancos de dados concluída" >> $LOG_DIR/cleanup.log
}

# Executar todas as funções de limpeza
echo "[$DATE] Iniciando processo de limpeza e manutenção..." >> $LOG_DIR/cleanup.log

cleanup_logs
cleanup_backups
cleanup_docker
cleanup_redis
cleanup_rabbitmq
cleanup_elasticsearch
cleanup_databases

# Verificar espaço em disco após limpeza
echo "[$DATE] Verificando espaço em disco após limpeza..." >> $LOG_DIR/cleanup.log
df -h >> $LOG_DIR/cleanup.log

echo "[$DATE] Processo de limpeza e manutenção concluído" >> $LOG_DIR/cleanup.log 