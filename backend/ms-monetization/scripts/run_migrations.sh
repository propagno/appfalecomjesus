#!/bin/bash

# Ativar ambiente virtual (se estiver usando)
# source venv/bin/activate

# Executar migrations
alembic upgrade head

# Verificar status
alembic current 