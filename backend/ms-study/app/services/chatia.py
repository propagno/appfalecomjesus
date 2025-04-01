import httpx
from typing import Dict, List
from app.core.config import settings


class ChatIAService:
    @staticmethod
    async def generate_study_plan(
        objectives: List[str],
        bible_experience_level: str,
        content_preferences: List[str],
        preferred_time: str
    ) -> Dict:
        """
        Gera um plano de estudo personalizado usando o MS-ChatIA.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.CHATIA_URL}/api/v1/study/generate",
                json={
                    "objectives": objectives,
                    "bible_experience_level": bible_experience_level,
                    "content_preferences": content_preferences,
                    "preferred_time": preferred_time
                }
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_study_content(
        section_id: str,
        content_type: str
    ) -> Dict:
        """
        Obtém conteúdo específico para uma seção de estudo.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.CHATIA_URL}/api/v1/study/content",
                params={
                    "section_id": section_id,
                    "content_type": content_type
                }
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_study_reflection(
        section_id: str,
        user_id: str
    ) -> Dict:
        """
        Obtém uma reflexão personalizada para uma seção de estudo.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.CHATIA_URL}/api/v1/study/reflection",
                params={
                    "section_id": section_id,
                    "user_id": user_id
                }
            )
            response.raise_for_status()
            return response.json()
