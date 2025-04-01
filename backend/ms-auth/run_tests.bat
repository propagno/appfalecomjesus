@echo off
echo Executando testes unitarios...
python -m pytest tests/unit -v

set UNIT_EXIT_CODE=%ERRORLEVEL%

echo Executando testes de integracao...
python -m pytest tests/integration -v

set INTEGRATION_EXIT_CODE=%ERRORLEVEL%

echo Gerando relatorio de cobertura...
python -m pytest --cov=app --cov-report=html --cov-report=term

if %UNIT_EXIT_CODE% NEQ 0 (
    echo Alguns testes unitarios falharam!
    exit /b 1
)

if %INTEGRATION_EXIT_CODE% NEQ 0 (
    echo Alguns testes de integracao falharam!
    exit /b 1
)

echo Todos os testes passaram com sucesso!
exit /b 0 