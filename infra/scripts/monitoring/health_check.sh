#!/bin/bash

# Script de Monitoramento de Saúde do FaleComJesus

# Configurações
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
ALERT_EMAIL="admin@falecomjesus.com"
LOG_FILE="/var/log/falecomjesus/health_check.log"
DATE=$(date +%Y-%m-%d\ %H:%M:%S)

# Criar diretório de logs se não existir
mkdir -p /var/log/falecomjesus

# Função para verificar se um serviço está rodando
check_service() {
    local service=$1
    local status=$(docker-compose -f $DOCKER_COMPOSE_FILE ps $service --format json | jq -r '.[0].State')
    
    if [ "$status" != "running" ]; then
        echo "[$DATE] ALERTA: Serviço $service não está rodando (Status: $status)" >> $LOG_FILE
        echo "ALERTA: Serviço $service não está rodando (Status: $status)" | mail -s "Alerta de Saúde - FaleComJesus" $ALERT_EMAIL
    fi
}

# Função para verificar uso de recursos
check_resources() {
    local service=$1
    local cpu=$(docker stats $service --no-stream --format "{{.CPUPerc}}" | sed 's/%//')
    local memory=$(docker stats $service --no-stream --format "{{.MemUsage}}" | sed 's/MiB//')
    
    if (( $(echo "$cpu > 80" | bc -l) )); then
        echo "[$DATE] ALERTA: Alto uso de CPU no serviço $service ($cpu%)" >> $LOG_FILE
        echo "ALERTA: Alto uso de CPU no serviço $service ($cpu%)" | mail -s "Alerta de Recursos - FaleComJesus" $ALERT_EMAIL
    fi
    
    if (( $(echo "$memory > 1000" | bc -l) )); then
        echo "[$DATE] ALERTA: Alto uso de memória no serviço $service ($memory MiB)" >> $LOG_FILE
        echo "ALERTA: Alto uso de memória no serviço $service ($memory MiB)" | mail -s "Alerta de Recursos - FaleComJesus" $ALERT_EMAIL
    fi
}

# Função para verificar logs de erro
check_errors() {
    local service=$1
    local errors=$(docker-compose -f $DOCKER_COMPOSE_FILE logs $service --tail=100 | grep -i "error\|exception\|fail")
    
    if [ ! -z "$errors" ]; then
        echo "[$DATE] ALERTA: Erros encontrados nos logs do serviço $service" >> $LOG_FILE
        echo "ALERTA: Erros encontrados nos logs do serviço $service:\n$errors" | mail -s "Alerta de Logs - FaleComJesus" $ALERT_EMAIL
    fi
}

# Verificar serviços principais
services=("ms-auth" "ms-study" "ms-chatia" "ms-bible" "ms-gamification" "ms-admin")

for service in "${services[@]}"; do
    echo "[$DATE] Verificando serviço: $service" >> $LOG_FILE
    
    # Verificar status
    check_service $service
    
    # Verificar recursos
    check_resources $service
    
    # Verificar logs
    check_errors $service
done

# Verificar serviços de infraestrutura
infra_services=("nginx" "redis" "rabbitmq" "elasticsearch" "logstash" "kibana")

for service in "${infra_services[@]}"; do
    echo "[$DATE] Verificando serviço de infraestrutura: $service" >> $LOG_FILE
    
    # Verificar status
    check_service $service
    
    # Verificar recursos
    check_resources $service
    
    # Verificar logs
    check_errors $service
done

# Verificar espaço em disco
disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if (( $(echo "$disk_usage > 80" | bc -l) )); then
    echo "[$DATE] ALERTA: Alto uso de disco ($disk_usage%)" >> $LOG_FILE
    echo "ALERTA: Alto uso de disco ($disk_usage%)" | mail -s "Alerta de Disco - FaleComJesus" $ALERT_EMAIL
fi

# Verificar conexões com o banco de dados
databases=("auth_db" "study_db" "chat_db" "bible_db" "gamification_db" "admin_db")

for db in "${databases[@]}"; do
    echo "[$DATE] Verificando banco de dados: $db" >> $LOG_FILE
    
    # Tentar conectar ao banco
    if ! docker-compose -f $DOCKER_COMPOSE_FILE exec -T $db psql -U postgres -c "SELECT 1;" > /dev/null 2>&1; then
        echo "[$DATE] ALERTA: Não foi possível conectar ao banco de dados $db" >> $LOG_FILE
        echo "ALERTA: Não foi possível conectar ao banco de dados $db" | mail -s "Alerta de Banco de Dados - FaleComJesus" $ALERT_EMAIL
    fi
done

# Rotacionar logs antigos (manter últimos 7 dias)
find /var/log/falecomjesus -name "health_check.log" -mtime +7 -delete

echo "[$DATE] Verificação de saúde concluída" >> $LOG_FILE 