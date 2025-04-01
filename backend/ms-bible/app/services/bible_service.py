from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import logging
from fastapi import HTTPException, status
import random
from datetime import datetime, date

from ..models import Book, Chapter, Verse, Favorite
from ..schemas.bible import SearchResult, VerseDetail, BooksResponse, ChaptersResponse, VersesResponse, SearchResponse, VerseOfDayResponse, Testament

logger = logging.getLogger(__name__)


class BibleService:
    def __init__(self, db: Session):
        self.db = db

    # Métodos para Books
    def get_books(self) -> List[Book]:
        """Retorna todos os livros da Bíblia, ordenados por posição"""
        try:
            return self.db.query(Book).order_by(Book.position).all()
        except Exception as e:
            logger.error(f"Erro ao buscar livros: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar livros da Bíblia"
            )

    def get_book_by_id(self, book_id: int) -> Book:
        """Retorna um livro específico pelo ID"""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Livro com ID {book_id} não encontrado"
            )
        return book

    # Métodos para Chapters
    def get_chapters_by_book(self, book_id: int) -> List[Chapter]:
        """Retorna todos os capítulos de um livro específico"""
        book = self.get_book_by_id(book_id)  # Verifica se o livro existe
        try:
            return self.db.query(Chapter).filter(Chapter.book_id == book_id).order_by(Chapter.number).all()
        except Exception as e:
            logger.error(
                f"Erro ao buscar capítulos do livro {book_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar capítulos do livro {book_id}"
            )

    def get_chapter(self, chapter_id: int) -> Chapter:
        """Retorna um capítulo específico pelo ID"""
        chapter = self.db.query(Chapter).filter(
            Chapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Capítulo com ID {chapter_id} não encontrado"
            )
        return chapter

    # Métodos para Verses
    def get_verses_by_chapter(self, chapter_id: int) -> List[Verse]:
        """Retorna todos os versículos de um capítulo específico"""
        chapter = self.get_chapter(chapter_id)  # Verifica se o capítulo existe
        try:
            return self.db.query(Verse).filter(Verse.chapter_id == chapter_id).order_by(Verse.number).all()
        except Exception as e:
            logger.error(
                f"Erro ao buscar versículos do capítulo {chapter_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar versículos do capítulo {chapter_id}"
            )

    def get_verse(self, verse_id: int) -> Verse:
        """Retorna um versículo específico pelo ID"""
        verse = self.db.query(Verse).filter(Verse.id == verse_id).first()
        if not verse:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Versículo com ID {verse_id} não encontrado"
            )
        return verse

    # Métodos para Search
    def search_verses(self, query: str) -> List[SearchResult]:
        """Busca versículos que contenham o texto da query"""
        if not query or len(query.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A busca deve conter pelo menos 3 caracteres"
            )

        try:
            # Busca por texto no versículo
            query_filter = Verse.text.ilike(f"%{query}%")

            # Junção com Chapter e Book para obter informações completas
            results = (
                self.db.query(
                    Book.name.label("book_name"),
                    Chapter.number.label("chapter_number"),
                    Verse.number.label("verse_number"),
                    Verse.text.label("verse_text"),
                    Verse.id.label("verse_id")
                )
                .join(Verse.chapter)
                .join(Chapter.book)
                .filter(query_filter)
                .limit(50)  # Limitar resultados para performance
                .all()
            )

            # Converter para o esquema SearchResult
            search_results = []
            for result in results:
                search_results.append(
                    SearchResult(
                        book_name=result.book_name,
                        chapter_number=result.chapter_number,
                        verse_number=result.verse_number,
                        verse_text=result.verse_text,
                        verse_id=result.verse_id
                    )
                )

            return search_results
        except Exception as e:
            logger.error(
                f"Erro ao buscar versículos com query '{query}': {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao realizar busca na Bíblia"
            )

    # Métodos para Favorites
    def add_favorite(self, user_id: str, verse_id: int) -> Favorite:
        """Adiciona um versículo aos favoritos do usuário"""
        # Verifica se o versículo existe
        verse = self.get_verse(verse_id)

        # Verifica se já é favorito
        existing = self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.verse_id == verse_id
        ).first()

        if existing:
            return existing

        try:
            # Criar novo favorito
            favorite = Favorite(user_id=user_id, verse_id=verse_id)
            self.db.add(favorite)
            self.db.commit()
            self.db.refresh(favorite)
            return favorite
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao adicionar favorito: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar versículo aos favoritos"
            )

    def remove_favorite(self, user_id: str, verse_id: int) -> None:
        """Remove um versículo dos favoritos do usuário"""
        favorite = self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.verse_id == verse_id
        ).first()

        if not favorite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorito não encontrado"
            )

        try:
            self.db.delete(favorite)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao remover favorito: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao remover versículo dos favoritos"
            )

    def get_user_favorites(self, user_id: str) -> List[dict]:
        """Retorna todos os versículos favoritos de um usuário com informações completas"""
        try:
            results = (
                self.db.query(
                    Book.name.label("book_name"),
                    Chapter.number.label("chapter_number"),
                    Verse.number.label("verse_number"),
                    Verse.text.label("verse_text"),
                    Verse.id.label("verse_id"),
                    Favorite.id.label("favorite_id"),
                    Favorite.added_at.label("added_at")
                )
                .join(Favorite.verse)
                .join(Verse.chapter)
                .join(Chapter.book)
                .filter(Favorite.user_id == user_id)
                .order_by(Favorite.added_at.desc())
                .all()
            )

            favorites = []
            for result in results:
                favorites.append({
                    "favorite_id": result.favorite_id,
                    "verse_id": result.verse_id,
                    "book_name": result.book_name,
                    "chapter_number": result.chapter_number,
                    "verse_number": result.verse_number,
                    "verse_text": result.verse_text,
                    "added_at": result.added_at
                })

            return favorites
        except Exception as e:
            logger.error(
                f"Erro ao buscar favoritos do usuário {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar versículos favoritos"
            )

    def is_favorite(self, user_id: str, verse_id: int) -> bool:
        """Verifica se um versículo é favorito do usuário"""
        favorite = self.db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.verse_id == verse_id
        ).first()

        return favorite is not None

    # Mock data for testing
    _books = [
        {"id": 1, "name": "Gênesis", "abbreviation": "gn",
            "testament": Testament.OLD, "position": 1, "chapters_count": 50},
        {"id": 2, "name": "Êxodo", "abbreviation": "ex",
            "testament": Testament.OLD, "position": 2, "chapters_count": 40},
        {"id": 3, "name": "Levítico", "abbreviation": "lv",
            "testament": Testament.OLD, "position": 3, "chapters_count": 27},
        {"id": 40, "name": "Mateus", "abbreviation": "mt",
            "testament": Testament.NEW, "position": 40, "chapters_count": 28},
        {"id": 41, "name": "Marcos", "abbreviation": "mc",
            "testament": Testament.NEW, "position": 41, "chapters_count": 16},
        {"id": 42, "name": "Lucas", "abbreviation": "lc",
            "testament": Testament.NEW, "position": 42, "chapters_count": 24},
        {"id": 43, "name": "João", "abbreviation": "jo",
            "testament": Testament.NEW, "position": 43, "chapters_count": 21},
    ]

    @staticmethod
    async def get_books(testament: Optional[str] = None) -> BooksResponse:
        """
        Get list of Bible books, optionally filtered by testament.

        Args:
            testament: Filter by testament ("old" or "new")

        Returns:
            BooksResponse with list of books
        """
        books = BibleService._books

        if testament:
            books = [book for book in books if book["testament"] == testament]

        # Convert to Book objects
        book_items = [Book(**book) for book in books]

        return BooksResponse(
            items=book_items,
            total=len(book_items)
        )

    @staticmethod
    async def get_book(book_id: int) -> Book:
        """
        Get a specific Bible book by ID.

        Args:
            book_id: The ID of the book

        Returns:
            Book object

        Raises:
            HTTPException: If book not found
        """
        for book in BibleService._books:
            if book["id"] == book_id:
                return Book(**book)

        # If we get here, book was not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    @staticmethod
    async def get_chapters(book_id: int) -> ChaptersResponse:
        """
        Get chapters for a specific Bible book.

        Args:
            book_id: The ID of the book

        Returns:
            ChaptersResponse with list of chapters

        Raises:
            HTTPException: If book not found
        """
        # Get book info first
        book = await BibleService.get_book(book_id)

        # Generate chapter data
        chapters = [
            Chapter(
                id=(book_id * 1000) + i,
                book_id=book_id,
                number=i,
                verses_count=random.randint(20, 40)  # Random verse count
            )
            for i in range(1, book.chapters_count + 1)
        ]

        return ChaptersResponse(
            book_id=book.id,
            book_name=book.name,
            testament=book.testament,
            items=chapters,
            total=len(chapters)
        )

    @staticmethod
    async def get_verses(chapter_id: int) -> VersesResponse:
        """
        Get verses for a specific Bible chapter.

        Args:
            chapter_id: The ID of the chapter

        Returns:
            VersesResponse with list of verses

        Raises:
            HTTPException: If chapter not found
        """
        # In a real implementation, we would query the database
        # For mock purposes, we'll extract the book_id from the chapter_id
        book_id = chapter_id // 1000
        chapter_number = chapter_id % 1000

        # Get book info
        try:
            book = await BibleService.get_book(book_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )

        # Check if chapter exists
        if chapter_number < 1 or chapter_number > book.chapters_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )

        # Generate sample verses
        verses_count = random.randint(20, 40)
        verses = [
            Verse(
                id=(chapter_id * 1000) + i,
                chapter_id=chapter_id,
                book_id=book_id,
                chapter_number=chapter_number,
                verse_number=i,
                text=f"Este é o texto do versículo {i} do capítulo {chapter_number} de {book.name}."
            )
            for i in range(1, verses_count + 1)
        ]

        return VersesResponse(
            chapter_id=chapter_id,
            book_id=book_id,
            book_name=book.name,
            chapter_number=chapter_number,
            items=verses,
            total=len(verses)
        )

    @staticmethod
    async def search_bible(query: str, testament: Optional[str] = None, book_id: Optional[int] = None) -> SearchResponse:
        """
        Search the Bible for a specific text.

        Args:
            query: The search text
            testament: Optional filter by testament
            book_id: Optional filter by book

        Returns:
            SearchResponse with matching verses
        """
        # In a real implementation, we would use a text search engine
        # For mock purposes, we'll generate some random matches

        # Generate some random matches
        matches = []
        books = BibleService._books

        if testament:
            books = [book for book in books if book["testament"] == testament]

        if book_id:
            books = [book for book in books if book["id"] == book_id]

        # Generate between 5 and 15 matches
        match_count = random.randint(5, 15)

        for _ in range(match_count):
            # Pick a random book
            book = random.choice(books)

            # Generate a random chapter and verse
            chapter_number = random.randint(1, book["chapters_count"])
            verse_number = random.randint(1, 30)

            # Create a verse with the search term embedded
            words = query.split()
            text_parts = [
                "Este é um versículo que contém as palavras",
                *words,
                "em seu texto, demonstrando como funciona a busca."
            ]

            matches.append(
                VerseDetail(
                    id=(book["id"] * 1000000) +
                    (chapter_number * 1000) + verse_number,
                    chapter_id=(book["id"] * 1000) + chapter_number,
                    book_id=book["id"],
                    chapter_number=chapter_number,
                    verse_number=verse_number,
                    text=" ".join(text_parts),
                    book_name=book["name"],
                    book_abbreviation=book["abbreviation"],
                    testament=book["testament"]
                )
            )

        return SearchResponse(
            query=query,
            items=matches,
            total=len(matches)
        )

    @staticmethod
    async def get_random_verse() -> VerseDetail:
        """
        Get a random verse from the Bible.

        Returns:
            VerseDetail object
        """
        # Pick a random book
        book = random.choice(BibleService._books)

        # Generate a random chapter and verse
        chapter_number = random.randint(1, book["chapters_count"])
        verse_number = random.randint(1, 30)

        return VerseDetail(
            id=(book["id"] * 1000000) + (chapter_number * 1000) + verse_number,
            chapter_id=(book["id"] * 1000) + chapter_number,
            book_id=book["id"],
            chapter_number=chapter_number,
            verse_number=verse_number,
            text=f"Este é um versículo aleatório do capítulo {chapter_number} de {book['name']}.",
            book_name=book["name"],
            book_abbreviation=book["abbreviation"],
            testament=book["testament"]
        )

    @staticmethod
    async def get_verse_of_day() -> VerseOfDayResponse:
        """
        Get the verse of the day.

        Returns:
            VerseOfDayResponse with verse and additional information
        """
        # In a real implementation, this would be precomputed or stored
        # For mock purposes, we'll determine based on today's date

        # Get today's date
        today = date.today()
        day_of_year = today.timetuple().tm_yday

        # Use the day of year to seed our random generator for consistency
        random.seed(day_of_year)

        # Pick a random book
        book = random.choice(BibleService._books)

        # Generate a random chapter and verse
        chapter_number = random.randint(1, book["chapters_count"])
        verse_number = random.randint(1, 30)

        # Generate a verse
        verse = VerseDetail(
            id=(book["id"] * 1000000) + (chapter_number * 1000) + verse_number,
            chapter_id=(book["id"] * 1000) + chapter_number,
            book_id=book["id"],
            chapter_number=chapter_number,
            verse_number=verse_number,
            text=f"Este é o versículo do dia {today.strftime('%d/%m/%Y')} do capítulo {chapter_number} de {book['name']}.",
            book_name=book["name"],
            book_abbreviation=book["abbreviation"],
            testament=book["testament"]
        )

        # Generate a theme and reflection
        themes = [
            "Fé", "Esperança", "Amor", "Paciência", "Perseverança",
            "Gratidão", "Humildade", "Perdão", "Salvação", "Graça"
        ]

        theme = random.choice(themes)
        reflection = f"Reflita sobre o tema de {theme} em sua vida diária. Como este versículo se aplica à sua situação atual?"

        # Reset random seed
        random.seed()

        return VerseOfDayResponse(
            verse=verse,
            theme=theme,
            reflection=reflection
        )
