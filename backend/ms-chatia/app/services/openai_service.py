from typing import Dict, List, Optional, Any
import logging
from uuid import UUID
from datetime import datetime
import json
import os
import tiktoken

from openai import AsyncOpenAI, APIError
from fastapi import HTTPException, status

from app.core.config import get_settings
from app.core.logging import get_logger, log_manager
from app.schemas.chat import (
    ChatMessageResponse,
    StudyPlanRequest,
    StudyPlanResponse
)

logger = log_manager
settings = get_settings()

# Configuração do cliente OpenAI
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    """
    Serviço para integração com OpenAI.

    Responsável por:
    - Gerar respostas do chat
    - Criar planos de estudo
    - Gerar reflexões espirituais
    - Controlar uso da API

    Attributes:
        api_key: Chave da API da OpenAI
        model: Modelo GPT a ser usado
    """

    def __init__(self):
        """
        Inicializa o serviço da OpenAI.

        Configura API key e modelo.
        """
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.token_encoder = tiktoken.encoding_for_model(self.model)
        logger.info(f"OpenAIService inicializado com modelo: {self.model}")

    async def generate_response(
        self,
        message: str,
        history: Optional[List[Dict]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Gera resposta para mensagem.

        Args:
            message: Mensagem do usuário
            history: Histórico de mensagens
            context: Contexto adicional

        Returns:
            Dict com resposta da IA

        Raises:
            HTTPException: Se erro na geração
        """
        try:
            # Monta prompt base
            system_prompt = """
            Você é um mentor espiritual cristão acolhedor e sábio.
            Responda sempre com base na Bíblia, incluindo versículos relevantes.
            Seja gentil, empático e evite julgamentos.
            Foque em orientação prática e edificação espiritual.
            """

            # Adiciona contexto se disponível
            if context:
                if context.get("study_section_id"):
                    system_prompt += "\nVocê está ajudando com dúvidas sobre a seção de estudo atual."
                if context.get("verse_id"):
                    system_prompt += "\nVocê está explicando um versículo específico."

            # Monta mensagens
            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Adiciona histórico se disponível
            if history:
                messages.extend(history)

            # Adiciona mensagem atual
            messages.append({"role": "user", "content": message})

            # Calcular tokens
            input_tokens = self._count_tokens(messages)
            if input_tokens > (4096 - self.max_tokens):
                logger.warning(f"Input muito grande: {input_tokens} tokens")
                # Truncar mensagens se necessário
                messages = self._truncate_messages(
                    messages, 4096 - self.max_tokens)

            # Chama API
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return {
                "text": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }

        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao gerar resposta"
            )
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao processar resposta"
            )

    async def generate_study_plan(
        self,
        user_id: UUID,
        preferences: Dict
    ) -> Dict:
        """
        Gera plano de estudo personalizado.

        Args:
            user_id: ID do usuário
            preferences: Preferências do usuário com objetivos, nível, etc.

        Returns:
            Dict com plano gerado estruturado em seções e conteúdos

        Raises:
            HTTPException: Se erro na geração
        """
        try:
            # Verificar que todas as preferências necessárias estão presentes
            required_keys = ["objectives", "bible_experience_level",
                             "content_preferences", "preferred_time"]
            for key in required_keys:
                if key not in preferences:
                    logger.warning(
                        f"Preferência ausente: {key}. Usando valor padrão.")

            # Construir um prompt estruturado para um resultado mais consistente
            system_prompt = """
            Você é um especialista em teologia e educação cristã, especializado em criar planos de estudo bíblico personalizados.
            
            Crie um plano de estudo completo, estruturado, com o seguinte formato:
            
            {
                "title": "Título inspirador para o plano",
                "description": "Descrição detalhada do objetivo do plano",
                "sections": [
                    {
                        "title": "Título da sessão do dia 1",
                        "duration_minutes": 20,
                        "contents": [
                            {
                                "type": "text",
                                "content": "Texto introdutório sobre a reflexão do dia",
                                "position": 1
                            },
                            {
                                "type": "verse",
                                "content": "Versículo completo com texto e referência",
                                "position": 2
                            },
                            {
                                "type": "reflection",
                                "content": "Reflexão sobre o versículo, aplicações práticas",
                                "position": 3
                            },
                            {
                                "type": "prayer",
                                "content": "Sugestão de oração relacionada ao tema",
                                "position": 4
                            }
                        ]
                    },
                    {
                        "title": "Título da sessão do dia 2",
                        "duration_minutes": 20,
                        "contents": [...]
                    }
                    // ... (continuar para os demais dias)
                ]
            }
            
            REGRAS IMPORTANTES:
            1. O plano deve ter exatamente 7 dias de estudo
            2. Cada sessão diária deve ser inspiradora e ter conteúdo original
            3. Use versículos específicos e relevantes aos objetivos do usuário
            4. A duração de cada sessão deve ser de 15-30 minutos
            5. Adapte a complexidade ao nível de conhecimento bíblico informado
            6. Inclua reflexões práticas e aplicáveis ao cotidiano
            7. Retorne APENAS JSON válido no formato especificado, sem comentários extras
            """

            # Criar um prompt de usuário com as preferências específicas
            user_prompt = f"""
            Crie um plano de estudo bíblico personalizado com estas especificações:
            
            1. OBJETIVOS ESPIRITUAIS: {', '.join(preferences.get('objectives', ['crescimento espiritual']))}
            
            2. NÍVEL DE CONHECIMENTO BÍBLICO: {preferences.get('bible_experience_level', 'iniciante')}
            
            3. FORMATOS DE CONTEÚDO PREFERIDOS: {', '.join(preferences.get('content_preferences', ['texto']))}
            
            4. HORÁRIO PREFERIDO PARA ESTUDO: {preferences.get('preferred_time', 'qualquer')}
            
            Gere um plano de 7 dias estruturado como JSON. Cada dia deve conter conteúdos relevantes aos objetivos.
            Adapte a linguagem e profundidade ao nível do usuário.
            Lembre-se de retornar apenas JSON válido no formato solicitado.
            """

            # Chamar a OpenAI com controle de temperatura para maior consistência
            logger.info(
                f"Gerando plano para usuário {user_id} com objetivos: {preferences.get('objectives', [])}")

            # Calcular tokens
            input_tokens = self._count_tokens([{"role": "system", "content": system_prompt}, {
                                              "role": "user", "content": user_prompt}])
            if input_tokens > (4096 - self.max_tokens):
                logger.warning(f"Input muito grande: {input_tokens} tokens")
                # Truncar mensagens se necessário
                system_prompt = system_prompt[:self._truncate_messages([{"role": "system", "content": system_prompt}, {
                                                                       "role": "user", "content": user_prompt}], 4096 - self.max_tokens)[0]["content"]]
                user_prompt = user_prompt[:self._truncate_messages([{"role": "system", "content": system_prompt}, {
                                                                   "role": "user", "content": user_prompt}], 4096 - self.max_tokens)[1]["content"]]

            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,  # Reduzido para maior consistência estrutural
                max_tokens=3000,  # Aumentado para comportar planos completos
                top_p=0.95,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                # Para garantir resposta em JSON
                response_format={"type": "json_object"}
            )

            # Extrair e parsear a resposta
            plan_text = response.choices[0].message.content

            try:
                # Tentar parsear como JSON
                plan_data = json.loads(plan_text)

                # Validar estrutura mínima
                if "title" not in plan_data or "description" not in plan_data or "sections" not in plan_data:
                    logger.error(
                        f"Plano gerado faltando campos obrigatórios: {plan_data.keys()}")
                    # Criar estrutura básica se estiver faltando
                    if "title" not in plan_data:
                        plan_data["title"] = "Plano de Estudo Personalizado"
                    if "description" not in plan_data:
                        plan_data["description"] = "Plano gerado com base nas suas preferências espirituais."
                    if "sections" not in plan_data:
                        plan_data["sections"] = []

                logger.info(
                    f"Plano gerado com sucesso: {plan_data['title']} com {len(plan_data['sections'])} sessões")

                # Adicionar metadados sobre uso de tokens
                plan_data["tokens_used"] = response.usage.total_tokens

                return plan_data

            except json.JSONDecodeError:
                logger.error(
                    f"Falha ao parsear JSON da resposta: {plan_text[:200]}...")
                # Criar uma estrutura básica caso falhe o parsing
                return {
                    "title": "Plano de Estudo Personalizado",
                    "description": "Plano baseado em suas preferências espirituais.",
                    "sections": [],
                    "error": "Erro ao estruturar o plano. Por favor, tente novamente."
                }

        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Erro ao gerar plano: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error generating plan: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao processar plano: {str(e)}"
            )

    async def generate_reflection(
        self,
        verse_text: str,
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Gera reflexão sobre versículo.

        Args:
            verse_text: Texto do versículo
            user_context: Contexto do usuário

        Returns:
            Dict com reflexão gerada

        Raises:
            HTTPException: Se erro na geração
        """
        try:
            # Monta prompt
            system_prompt = """
            Você é um mentor espiritual especializado em reflexões bíblicas.
            Gere uma reflexão profunda e aplicável sobre o versículo fornecido.
            Inclua:
            - Contexto histórico breve
            - Significado espiritual
            - Aplicação prática atual
            - Sugestão de oração
            """

            # Adiciona contexto se disponível
            if user_context:
                system_prompt += f"\nConsidere que o usuário está: {user_context.get('situation', 'buscando crescimento')}"

            # Chama API
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Gere uma reflexão sobre: {verse_text}"}
                ],
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            return {
                "reflection": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason
            }

        except APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao gerar reflexão"
            )
        except Exception as e:
            logger.error(f"Error generating reflection: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao processar reflexão"
            )

    # Métodos auxiliares

    def extract_verses(self, content: str) -> List[str]:
        """
        Extrai referências bíblicas do texto.

        Args:
            content: Texto da resposta

        Returns:
            Lista de referências (ex: ["João 3:16", "Salmos 23:1"])
        """
        # TODO: Implementar extração de versículos
        return []

    def generate_suggestions(self, content: str) -> List[str]:
        """
        Gera sugestões de próximas perguntas.

        Args:
            content: Texto da resposta

        Returns:
            Lista de sugestões
        """
        # TODO: Implementar geração de sugestões
        return []

    def parse_study_plan(self, content: str) -> Dict:
        """
        Converte resposta da IA em plano estruturado.

        Args:
            content: Texto do plano

        Returns:
            Dicionário com título, descrição e sessões
        """
        # TODO: Implementar parser de plano
        return {
            "title": "Plano Temporário",
            "description": "Descrição temporária",
            "sessions": []
        }

    def _count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """
        Conta o número de tokens em uma lista de mensagens.

        Args:
            messages: Lista de mensagens

        Returns:
            int: Número total de tokens
        """
        total = 0
        for message in messages:
            total += len(self.token_encoder.encode(message["content"]))
        return total

    def _truncate_messages(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int
    ) -> List[Dict[str, str]]:
        """
        Trunca a lista de mensagens para caber no limite de tokens.

        Args:
            messages: Lista original de mensagens
            max_tokens: Limite máximo de tokens

        Returns:
            List: Lista truncada de mensagens
        """
        # Manter o prompt do sistema e a última mensagem do usuário
        system_message = messages[0]
        user_message = messages[-1]

        # Inicializar lista truncada
        truncated = [system_message]
        remaining_tokens = max_tokens - \
            self._count_tokens([system_message, user_message])

        # Adicionar mensagens do histórico até atingir o limite
        if remaining_tokens > 0 and len(messages) > 2:
            for message in messages[1:-1]:
                message_tokens = len(
                    self.token_encoder.encode(message["content"]))
                if message_tokens <= remaining_tokens:
                    truncated.append(message)
                    remaining_tokens -= message_tokens
                else:
                    break

        # Adicionar a mensagem do usuário
        truncated.append(user_message)

        return truncated
