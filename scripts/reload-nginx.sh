#!/bin/bash
# Reload script para Nginx no ambiente de desenvolvimento

# Verifica se o container nginx está rodando
NGINX_RUNNING=$(docker ps --filter "name=infra-nginx" --format "{{.Names}}")

if [ -z "$NGINX_RUNNING" ]; then
  echo "Container do Nginx não está rodando. Iniciando os serviços..."
  cd "$(dirname "$0")/../infra" || exit
  docker-compose -f docker-compose.dev.yml up -d nginx
else
  echo "Recarregando configuração do Nginx..."
  docker exec infra-nginx nginx -s reload
fi

echo "✅ Configuração do Nginx atualizada com sucesso!"
echo "O proxy reverso agora aponta para os nomes dos serviços, não para IPs fixos."
echo "Acesse o frontend através de http://localhost" 