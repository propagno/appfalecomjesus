@echo off
REM Script para recarregar o Nginx e reiniciar o ms-auth no ambiente Windows

echo Verificando se o container Nginx está rodando...
docker ps --filter "name=infra-nginx" --format "{{.Names}}" > temp.txt
set /p NGINX_RUNNING=<temp.txt
del temp.txt

if "%NGINX_RUNNING%"=="" (
    echo Container do Nginx não está rodando. Iniciando os serviços...
    cd /d %~dp0\..\infra
    docker-compose -f docker-compose.dev.yml up -d nginx
) else (
    echo Reiniciando o serviço ms-auth...
    docker restart infra-ms-auth
    
    echo Esperando 5 segundos para o ms-auth inicializar...
    timeout /t 5 /nobreak > nul
    
    echo Recarregando configuração do Nginx...
    docker restart infra-nginx
)

echo.
echo ✅ Serviços reiniciados com sucesso!
echo O proxy reverso agora aponta para os nomes dos serviços, com timeouts aumentados.
echo MS-Auth foi reiniciado para resolver problemas de conexão.
echo Acesse o frontend através de http://localhost
echo.

pause 