import os
from typing import Optional, List, Dict, Any
import openai
import logging
from fastapi import Depends
import asyncio

from app.core.config import get_settings, Settings

logger = logging.getLogger("openai_service")


class OpenAIService:
    """
    Serviço para interação com a API da OpenAI.
    """

    def __init__(self, api_key: str, model: str):
        self.client = openai.AsyncClient(api_key=api_key)
        self.default_model = model
        logger.info(f"OpenAI service initialized with model: {model}")

    async def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Gera uma resposta a partir de um prompt usando o modelo de IA da OpenAI.

        Args:
            prompt: O texto do prompt para gerar a resposta
            context: Contexto opcional para a geração (mensagens anteriores)
            model: Modelo a ser usado (se None, usa o modelo padrão)
            temperature: Temperatura para controlar a aleatoriedade (0.0 a 1.0)
            max_tokens: Número máximo de tokens na resposta
            response_format: Formato da resposta (ex: {"type": "json_object"})

        Returns:
            str: Resposta gerada pelo modelo
        """
        try:
            messages = []

            # Adicionar sistema de instruções
            messages.append({
                "role": "system",
                "content": "Você é um conselheiro cristão sábio e acolhedor, especializado em orientações baseadas na Bíblia. Mantenha suas respostas breves, claras e fundamentadas em princípios bíblicos."
            })

            # Adicionar contexto se fornecido
            if context and len(context) > 0:
                logger.info(
                    f"Adicionando {len(context)} mensagens de contexto")
                for msg in context:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })

            # Adicionar o prompt do usuário
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Parâmetros para a chamada da API
            params = {
                "model": model or self.default_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Adicionar response_format se fornecido
            if response_format:
                params["response_format"] = response_format

            logger.info(f"Chamando API OpenAI com modelo: {params['model']}")

            # Implementar retry com backoff exponencial
            max_retries = 3
            retry_count = 0
            retry_delay = 1  # segundos

            while retry_count < max_retries:
                try:
                    # Chamada à API
                    response = await self.client.chat.completions.create(**params)

                    # Extrair e retornar o conteúdo da resposta
                    content = response.choices[0].message.content
                    return content.strip() if content else ""

                except (openai.RateLimitError, openai.APITimeoutError) as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(
                            f"Erro após {max_retries} tentativas: {str(e)}")
                        raise

                    # Backoff exponencial
                    wait_time = retry_delay * (2 ** (retry_count - 1))
                    logger.warning(
                        f"Rate limit atingido, tentando novamente em {wait_time}s. Tentativa {retry_count}/{max_retries}")
                    await asyncio.sleep(wait_time)

                except Exception as e:
                    # Outros erros não são retentados
                    logger.error(f"Erro chamando OpenAI: {str(e)}")
                    raise

        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            raise


def get_openai_service(settings: Settings = Depends(get_settings)) -> OpenAIService:
    """
    Provedor do serviço OpenAI para injeção de dependência.

    Args:
        settings: Configurações da aplicação

    Returns:
        OpenAIService: Instância do serviço OpenAI
    """
    return OpenAIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model
    )
