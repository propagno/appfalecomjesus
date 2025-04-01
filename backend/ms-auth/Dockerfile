FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar bcrypt específico para compatibilidade com passlib
RUN pip install --no-cache-dir bcrypt==4.0.1

# Copiar código da aplicação
COPY . .

# Criar diretório de logs e ajustar permissões
RUN mkdir -p /app/logs && \
    chown -R nobody:nogroup /app/logs

# Expor porta da aplicação
EXPOSE 5000

# Mudar para usuário não-root
USER nobody

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/auth/health || exit 1

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--log-level", "info"] 