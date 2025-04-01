# Configurações
$dbName = "ms_chatia"
$dbUser = "postgres"
$dbPassword = "postgres"
$dbHost = "localhost"
$dbPort = "5432"

# Lista de tabelas necessárias
$tables = @(
    "chat_history"
)

# Função para verificar se uma tabela existe
function Check-Table {
    param($table)
    $env:PGPASSWORD = $dbPassword
    $query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$table');"
    $result = psql -h $dbHost -p $dbPort -U $dbUser -d $dbName -tAc $query
    return $result.Trim() -eq "t"
}

# Função para criar uma tabela
function Create-Table {
    param($table)
    Write-Host "Criando tabela $table..."
    $env:PGPASSWORD = $dbPassword
    psql -h $dbHost -p $dbPort -U $dbUser -d $dbName -f "sql/create_${table}.sql"
}

# Verificar cada tabela
foreach ($table in $tables) {
    Write-Host "Verificando tabela $table..."
    $exists = Check-Table $table
    
    if (-not $exists) {
        Write-Host "Tabela $table não existe. Criando..."
        Create-Table $table
    } else {
        Write-Host "Tabela $table já existe."
    }
}

Write-Host "Verificação de tabelas concluída!" 