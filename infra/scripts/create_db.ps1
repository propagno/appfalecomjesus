# Configurações
$dbName = "ms_chatia"
$dbUser = "postgres"
$dbPassword = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# Criar banco de dados
Write-Host "Criando banco de dados $dbName..."
$env:PGPASSWORD = $dbPassword
createdb -h $dbHost -p $dbPort -U $dbUser $dbName

if ($LASTEXITCODE -eq 0) {
    Write-Host "Banco de dados $dbName criado com sucesso!"
} else {
    Write-Host "Erro ao criar banco de dados!"
    exit 1
} 