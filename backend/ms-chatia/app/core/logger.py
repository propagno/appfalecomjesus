"""
Módulo de logger simples para evitar importação circular.
"""

import logging

# Configuração básica
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Instância global do logger
logger = logging.getLogger("falecomjesus")
