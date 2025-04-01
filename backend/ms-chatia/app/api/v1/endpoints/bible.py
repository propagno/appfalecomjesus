from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.logging import get_logger
from app.schemas.bible import (
    Book,
    Chapter,
    Verse,
    SearchResult
)
from app.services.bible_service import BibleService

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/books",
    response_model=List[Book],
    summary="Listar livros",
    description="""
    Lista todos os livros da Bíblia.
    
    Retorna:
    - 66 livros no total
    - 39 do Antigo Testamento
    - 27 do Novo Testamento
    
    Cada livro inclui:
    - Nome em português
    - Abreviação
    - Testamento (antigo/novo)
    - Total de capítulos
    """
)
async def list_books(
    db: Session = Depends(get_db)
) -> List[Book]:
    """
    Lista todos os livros da Bíblia.

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de Book

    Raises:
        HTTPException: Se erro na listagem
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.list_books()
    except Exception as e:
        logger.error(f"Error listing books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar livros"
        )


@router.get(
    "/books/{book_id}/chapters",
    response_model=List[Chapter],
    summary="Listar capítulos",
    description="""
    Lista todos os capítulos de um livro específico.
    
    Cada capítulo inclui:
    - Número
    - Total de versículos
    - Primeiro versículo (prévia)
    """
)
async def list_chapters(
    book_id: UUID,
    db: Session = Depends(get_db)
) -> List[Chapter]:
    """
    Lista todos os capítulos de um livro.

    Args:
        book_id: ID do livro
        db: Sessão do banco de dados

    Returns:
        Lista de Chapter

    Raises:
        HTTPException: Se livro não encontrado
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.list_chapters(book_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing chapters: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar capítulos"
        )


@router.get(
    "/chapters/{chapter_id}/verses",
    response_model=List[Verse],
    summary="Listar versículos",
    description="""
    Lista todos os versículos de um capítulo específico.
    
    Cada versículo inclui:
    - Número
    - Texto completo
    - Referência (livro, capítulo)
    """
)
async def list_verses(
    chapter_id: UUID,
    db: Session = Depends(get_db)
) -> List[Verse]:
    """
    Lista todos os versículos de um capítulo.

    Args:
        chapter_id: ID do capítulo
        db: Sessão do banco de dados

    Returns:
        Lista de Verse

    Raises:
        HTTPException: Se capítulo não encontrado
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.list_verses(chapter_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing verses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar versículos"
        )


@router.get(
    "/search",
    response_model=List[SearchResult],
    summary="Buscar na Bíblia",
    description="""
    Pesquisa versículos por palavra-chave ou tema.
    
    Permite buscar por:
    - Palavra ou frase exata
    - Tema (ex: amor, fé, esperança)
    - Livro específico
    - Testamento (antigo/novo)
    
    Retorna versículos ordenados por relevância.
    """
)
async def search_bible(
    query: str = Query(..., description="Termo de busca"),
    book_id: UUID = None,
    testament: str = None,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db)
) -> List[SearchResult]:
    """
    Pesquisa versículos na Bíblia.

    Args:
        query: Termo de busca
        book_id: Filtro por livro (opcional)
        testament: Filtro por testamento (opcional)
        limit: Limite de resultados
        db: Sessão do banco de dados

    Returns:
        Lista de SearchResult

    Raises:
        HTTPException: Se erro na busca
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.search(
            query=query,
            book_id=book_id,
            testament=testament,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Error searching Bible: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao pesquisar na Bíblia"
        )


@router.get(
    "/random",
    response_model=Verse,
    summary="Versículo aleatório",
    description="""
    Retorna um versículo aleatório da Bíblia.
    
    Pode ser filtrado por:
    - Livro específico
    - Testamento
    - Tema
    
    Ideal para mensagem do dia ou inspiração.
    """
)
async def random_verse(
    book_id: UUID = None,
    testament: str = None,
    theme: str = None,
    db: Session = Depends(get_db)
) -> Verse:
    """
    Retorna um versículo aleatório.

    Args:
        book_id: Filtro por livro (opcional)
        testament: Filtro por testamento (opcional)
        theme: Filtro por tema (opcional)
        db: Sessão do banco de dados

    Returns:
        Verse aleatório

    Raises:
        HTTPException: Se erro na busca
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.random_verse(
            book_id=book_id,
            testament=testament,
            theme=theme
        )
    except Exception as e:
        logger.error(f"Error getting random verse: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar versículo aleatório"
        )


@router.get(
    "/themes",
    response_model=List[str],
    summary="Listar temas",
    description="""
    Lista todos os temas disponíveis para busca.
    
    Inclui temas como:
    - Amor
    - Fé
    - Esperança
    - Sabedoria
    - Família
    - Ansiedade
    """
)
async def list_themes(
    db: Session = Depends(get_db)
) -> List[str]:
    """
    Lista todos os temas disponíveis.

    Args:
        db: Sessão do banco de dados

    Returns:
        Lista de temas

    Raises:
        HTTPException: Se erro na listagem
    """
    try:
        bible_service = BibleService(db)
        return await bible_service.list_themes()
    except Exception as e:
        logger.error(f"Error listing themes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar temas"
        )
