FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    curl \
    wget \
    python3-dev \
    # Dependências para o WeasyPrint
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fontconfig \
    fonts-liberation

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt \
    # Garantir que WeasyPrint seja instalado corretamente
    && pip install --no-cache-dir weasyprint cffi cairocffi Pillow cairosvg

# Verificar que WeasyPrint foi instalado corretamente
RUN python -c "import weasyprint; print('WeasyPrint instalado com sucesso!')"

# Copiar o código-fonte
COPY . .

# Dar permissão de execução ao entrypoint.sh
RUN chmod +x entrypoint.sh

# Definir o ponto de entrada
ENTRYPOINT ["./entrypoint.sh"]

# Expor a porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/api/study/health || exit 1 