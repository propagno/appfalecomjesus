"""
Serviço de logs do sistema FaleComJesus.

Este módulo implementa o sistema de logs estruturados da aplicação,
incluindo múltiplos handlers, rotação de arquivos e integração com
ELK Stack (opcional).

Features:
    - Logs estruturados (JSON)
    - Console colorido
    - Arquivo com rotação
    - Integração ELK (opcional)
    - Métricas
    - Filtros 
"""

import os
import sys
import json
import logging
import traceback
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, Response

# Tornar Elasticsearch opcional
elasticsearch_available = False
try:
    from elasticsearch import Elasticsearch
    elasticsearch_available = True
except ImportError:
    # Log será feito sem Elasticsearch
    pass


class LogManager:
    """
    Gerenciador de logs estruturados.

    Features:
        - Logs estruturados (JSON)
        - Console colorido
        - Arquivo com rotação
        - Integração ELK (opcional)
        - Métricas
        - Filtros

    Attributes:
        logger: Logger
        es_client: Cliente Elasticsearch (opcional)
        metrics: Métricas de logs
    """

    def __init__(
        self,
        name: str = "falecomjesus",
        level: int = logging.INFO,
        to_console: bool = True,
        to_file: bool = False,
        to_elk: bool = False,
        es_hosts: Optional[List[str]] = None,
        es_index: str = "logs"
    ):
        """
        Inicializa o gerenciador.

        Args:
            name: Nome do logger
            level: Nível de log
            to_console: Enviar para console
            to_file: Enviar para arquivo
            to_elk: Enviar para ELK
            es_hosts: Hosts do Elasticsearch
            es_index: Índice do Elasticsearch
        """
        # Logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Limpa handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Console
        if to_console:
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(level)
            self.logger.addHandler(console)

        # Arquivo
        if to_file:
            os.makedirs("logs", exist_ok=True)
            file_handler = RotatingFileHandler(
                f"logs/{name}.log",
                maxBytes=10485760,  # 10MB
                backupCount=5,
                encoding="utf-8"
            )
            file_handler.setLevel(level)
            self.logger.addHandler(file_handler)

        # Elasticsearch (opcional)
        self.es_client = None
        self.es_index = es_index
        if to_elk and elasticsearch_available:
            try:
                self.es_client = Elasticsearch(
                    es_hosts or ["http://elasticsearch:9200"])
            except Exception as e:
                self.logger.error(
                    f"Erro ao conectar com Elasticsearch: {str(e)}")

        # Métricas
        self.metrics = {
            "total": 0,
            "info": 0,
            "warn": 0,
            "error": 0,
            "debug": 0
        }

    def info(self, message: str, extra: Optional[Dict] = None) -> None:
        """
        Log info.

        Args:
            message: Mensagem
            extra: Dados extras
        """
        self.metrics["total"] += 1
        self.metrics["info"] += 1

        self.logger.info(message, extra=extra or {})

        # ELK (opcional)
        if self.es_client is not None and elasticsearch_available:
            try:
                doc = {
                    "timestamp": datetime.now().isoformat(),
                    "level": "INFO",
                    "message": message,
                    "extra": extra or {}
                }
                self.es_client.index(index=self.es_index, body=doc)
            except Exception as e:
                self.logger.error(f"Erro ao enviar log para ELK: {str(e)}")

    def error(self, message: str, extra: Optional[Dict] = None) -> None:
        """
        Log error.

        Args:
            message: Mensagem
            extra: Dados extras
        """
        self.metrics["total"] += 1
        self.metrics["error"] += 1

        # Captura stack trace
        stack = traceback.format_exc()
        extras = {"stack": stack}
        if extra:
            extras.update(extra)

        self.logger.error(message, extra=extras)

        # ELK (opcional)
        if self.es_client is not None and elasticsearch_available:
            try:
                doc = {
                    "timestamp": datetime.now().isoformat(),
                    "level": "ERROR",
                    "message": message,
                    "stack": stack,
                    "extra": extra or {}
                }
                self.es_client.index(index=self.es_index, body=doc)
            except Exception as e:
                self.logger.error(f"Erro ao enviar log para ELK: {str(e)}")

    def warn(self, message: str, extra: Optional[Dict] = None) -> None:
        """
        Log warning.

        Args:
            message: Mensagem
            extra: Dados extras
        """
        self.metrics["total"] += 1
        self.metrics["warn"] += 1

        self.logger.warning(message, extra=extra or {})

        # ELK (opcional)
        if self.es_client is not None and elasticsearch_available:
            try:
                doc = {
                    "timestamp": datetime.now().isoformat(),
                    "level": "WARN",
                    "message": message,
                    "extra": extra or {}
                }
                self.es_client.index(index=self.es_index, body=doc)
            except Exception as e:
                self.logger.error(f"Erro ao enviar log para ELK: {str(e)}")

    def debug(self, message: str, extra: Optional[Dict] = None) -> None:
        """
        Log debug.

        Args:
            message: Mensagem
            extra: Dados extras
        """
        self.metrics["total"] += 1
        self.metrics["debug"] += 1

        self.logger.debug(message, extra=extra or {})

        # ELK (opcional)
        if self.es_client is not None and elasticsearch_available:
            try:
                doc = {
                    "timestamp": datetime.now().isoformat(),
                    "level": "DEBUG",
                    "message": message,
                    "extra": extra or {}
                }
                self.es_client.index(index=self.es_index, body=doc)
            except Exception as e:
                self.logger.error(f"Erro ao enviar log para ELK: {str(e)}")

    def get_metrics(self) -> Dict:
        """
        Obtém métricas.

        Returns:
            Dict: Métricas
        """
        return self.metrics

    def close(self) -> None:
        """
        Fecha recursos.
        """
        # ELK (opcional)
        if self.es_client is not None and elasticsearch_available:
            try:
                self.es_client.close()
            except Exception as e:
                self.logger.error(f"Erro ao fechar Elasticsearch: {str(e)}")

    # Para compatibilidade com o middleware que usa o estilo de async_info, etc.
    async def info(self, message: str, extra: Optional[Dict] = None) -> None:
        self.info(message, extra)

    async def error(self, message: str, extra: Optional[Dict] = None) -> None:
        self.error(message, extra)

    async def warn(self, message: str, extra: Optional[Dict] = None) -> None:
        self.warn(message, extra)

    async def debug(self, message: str, extra: Optional[Dict] = None) -> None:
        self.debug(message, extra)


# Instância global
log_manager = LogManager()

# Função para obter o logger global


def get_logger(name=None):
    """
    Retorna o logger global configurado.

    Args:
        name: Nome do logger (ignorado, mantido para compatibilidade)

    Returns:
        LogManager: Instância global do gerenciador de logs
    """
    return log_manager


# Para compatibilidade com middleware.py
logger = log_manager


def setup_logging(app: FastAPI) -> None:
    """
    Configura o sistema de logs para a aplicação FastAPI.

    Adiciona middleware para logging de requisições e configura
    handlers para diferentes níveis de log.

    Args:
        app: Aplicação FastAPI
    """
    logger = logging.getLogger("ms-chatia")

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Middleware para logar requisições e respostas"""
        start_time = datetime.now()

        # Log da requisição
        logger.info(
            f"Request {request.method} {request.url.path}",
            extra={
                "client_ip": request.client.host,
                "method": request.method,
                "path": request.url.path,
                "params": str(request.query_params),
            }
        )

        # Processa a requisição
        try:
            response = await call_next(request)
            process_time = (datetime.now() - start_time).total_seconds()

            # Log da resposta
            logger.info(
                f"Response {response.status_code} completed in {process_time:.4f}s",
                extra={
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )

            return response
        except Exception as e:
            # Log de erro
            process_time = (datetime.now() - start_time).total_seconds()
            logger.error(
                f"Error processing request: {str(e)}",
                extra={
                    "error": str(e),
                    "process_time": process_time,
                }
            )
            raise

    logger.info("Sistema de logging configurado com sucesso")
