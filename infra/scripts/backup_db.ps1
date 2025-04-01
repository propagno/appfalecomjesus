# Configurações
$backupDir = ".\backups"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$dbName = "ms_chatia"
$dbUser = "postgres"
$dbPassword = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# Criar diretório de backup se não existir
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# Nome do arquivo de backup
$backupFile = Join-Path $backupDir "${dbName}_${timestamp}.sql"

# Executar backup
Write-Host "Executando backup do banco de dados $dbName..."
$env:PGPASSWORD = $dbPassword
pg_dump -h $dbHost -p $dbPort -U $dbUser -d $dbName -f $backupFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup criado com sucesso: $backupFile"
    
    # Comprimir backup
    Compress-Archive -Path $backupFile -DestinationPath "$backupFile.gz" -Force
    
    # Remover arquivo SQL original
    Remove-Item $backupFile
    
    # Manter apenas os últimos 7 backups
    Get-ChildItem -Path $backupDir -Filter "*.gz" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -Skip 7 | 
    ForEach-Object { Remove-Item $_.FullName }
} else {
    Write-Host "Erro ao criar backup!"
    exit 1
} 