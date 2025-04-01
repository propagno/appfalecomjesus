import logging
import sys
from typing import Any, Dict, Optional

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    # Remove todos os handlers existentes
    logging.root.handlers = []

    # Configura o nível de log
    logging.root.setLevel(logging.INFO)

    # Remove handlers do loguru
    logger.remove()

    # Adiciona handler para interceptar logs do logging
    logging.root.addHandler(InterceptHandler())

    # Configura o loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": "INFO",
                "serialize": True,
            }
        ]
    )
