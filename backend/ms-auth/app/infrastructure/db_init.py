from sqlalchemy import inspect
from app.domain.auth.models import User
from app.infrastructure.database import Base, engine, session_factory


def init_db():
    """Initialize the database."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Check if users table exists and has data
    inspector = inspect(engine)
    if 'users' in inspector.get_table_names():
        db = session_factory()
        user_count = db.query(User).count()
        db.close()
        if user_count > 0:
            print("Database already initialized with data.")
            return

    print("Initialized the database.")
