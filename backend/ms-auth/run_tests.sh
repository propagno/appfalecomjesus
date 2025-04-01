#!/bin/bash

# Cores para saída no terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Limpa relatórios anteriores
rm -rf .coverage htmlcov

echo -e "${BLUE}Executando testes unitários...${NC}"
python -m pytest tests/unit -v

UNIT_EXIT_CODE=$?

echo -e "${BLUE}Executando testes de integração...${NC}"
python -m pytest tests/integration -v

INTEGRATION_EXIT_CODE=$?

# Gera relatório de cobertura
echo -e "${BLUE}Gerando relatório de cobertura...${NC}"
python -m pytest --cov=app --cov-report=html --cov-report=term

# Verifica se algum dos testes falhou
if [ $UNIT_EXIT_CODE -ne 0 ] || [ $INTEGRATION_EXIT_CODE -ne 0 ]; then
    echo -e "${RED}Alguns testes falharam!${NC}"
    exit 1
else
    echo -e "${GREEN}Todos os testes passaram com sucesso!${NC}"
    exit 0
fi 