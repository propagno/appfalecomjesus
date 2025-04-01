FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte
COPY . /app/

# Definir variáveis de ambiente padrão
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expor porta
EXPOSE 5000

# Comando padrão (pode ser substituído no docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"] 