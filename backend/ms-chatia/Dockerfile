FROM python:3.10-slim

WORKDIR /app

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    libssl-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro para aproveitar o cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir PyJWT==2.8.0 passlib==1.7.4

# Copiar código
COPY . /app/

# Tornar entrypoint.sh executável
RUN chmod +x /app/entrypoint.sh

# Definir entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1 