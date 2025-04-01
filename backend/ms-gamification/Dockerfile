FROM python:3.11-slim

WORKDIR /app

# Copiar apenas requirements primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Configurar as variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8004

# Expor a porta da aplicação
EXPOSE 8004

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"] 