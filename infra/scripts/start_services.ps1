# Parar e remover containers antigos
Write-Host "Parando e removendo containers antigos..."
docker-compose down -v

# Construir imagens
Write-Host "Construindo imagens..."
docker-compose build

# Iniciar serviços
Write-Host "Iniciando serviços..."
docker-compose up -d

# Aguardar serviços estarem prontos
Write-Host "Aguardando serviços estarem prontos..."
Start-Sleep -Seconds 10

# Verificar status dos serviços
Write-Host "Verificando status dos serviços..."
docker-compose ps

Write-Host "Todos os serviços foram iniciados!" 