# Criar banco de dados
Write-Host "Criando banco de dados..."
.\scripts\create_db.ps1

# Executar backup
Write-Host "Executando backup do banco de dados..."
.\scripts\backup_db.ps1

# Verificar e criar tabelas
Write-Host "Verificando e criando tabelas necessárias..."
.\scripts\check_tables.ps1

Write-Host "Setup do banco de dados concluído!" 