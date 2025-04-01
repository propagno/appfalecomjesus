#!/bin/bash

# Script de Deploy para Produção do FaleComJesus

# Configurações
ENV_FILE=".env.prod"
DOCKER_COMPOSE_FILE="infra/docker-compose.prod.yml"
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# Verificar se está no diretório raiz do projeto
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    echo "Erro: Execute este script do diretório raiz do projeto"
    exit 1
fi

# Verificar se o arquivo de ambiente existe
if [ ! -f "$ENV_FILE" ]; then
    echo "Erro: Arquivo $ENV_FILE não encontrado"
    exit 1
fi

# Backup antes do deploy
echo "Iniciando backup antes do deploy..."
./infra/scripts/backup/db_backup.sh

# Parar os containers atuais
echo "Parando containers atuais..."
docker-compose -f $DOCKER_COMPOSE_FILE down

# Limpar imagens antigas
echo "Limpando imagens antigas..."
docker system prune -f

# Pull das imagens mais recentes
echo "Atualizando imagens..."
docker-compose -f $DOCKER_COMPOSE_FILE pull

# Iniciar os containers
echo "Iniciando containers..."
docker-compose -f $DOCKER_COMPOSE_FILE up -d

# Verificar status dos containers
echo "Verificando status dos containers..."
docker-compose -f $DOCKER_COMPOSE_FILE ps

# Verificar logs
echo "Verificando logs..."
docker-compose -f $DOCKER_COMPOSE_FILE logs --tail=50

# Verificar saúde dos serviços
echo "Verificando saúde dos serviços..."
for service in ms-auth ms-study ms-chatia ms-bible ms-gamification ms-admin; do
    echo "Verificando $service..."
    curl -s http://localhost:8001/health || echo "$service não está respondendo"
done

# Verificar logs do Nginx
echo "Verificando logs do Nginx..."
docker-compose -f $DOCKER_COMPOSE_FILE logs nginx --tail=50

# Verificar logs do Elasticsearch
echo "Verificando logs do Elasticsearch..."
docker-compose -f $DOCKER_COMPOSE_FILE logs elasticsearch --tail=50

# Verificar logs do Redis
echo "Verificando logs do Redis..."
docker-compose -f $DOCKER_COMPOSE_FILE logs redis --tail=50

# Verificar logs do RabbitMQ
echo "Verificando logs do RabbitMQ..."
docker-compose -f $DOCKER_COMPOSE_FILE logs rabbitmq --tail=50

# Verificar uso de recursos
echo "Verificando uso de recursos..."
docker stats --no-stream

echo "Deploy concluído com sucesso!" 