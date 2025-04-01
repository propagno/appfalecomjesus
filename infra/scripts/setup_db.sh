#!/bin/bash

# Executar backup
echo "Executando backup do banco de dados..."
./scripts/backup_db.sh

# Verificar e criar tabelas
echo "Verificando e criando tabelas necessárias..."
./scripts/check_tables.sh

echo "Setup do banco de dados concluído!" 