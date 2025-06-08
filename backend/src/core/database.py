"""
Database configuration and connection management.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

# Create declarative base for models
Base = declarative_base()

# Global variables for engine and session factory
engine = None
AsyncSessionLocal = None


def get_engine():
    """Get or create the database engine."""
    global engine
    if engine is None:
        # Use SQLite for testing if no DATABASE_URL is provided or if TESTING is set
        database_url = settings.DATABASE_URL
        if os.getenv("TESTING") == "true" or not database_url:
            database_url = "sqlite+aiosqlite:///./test.db"

        engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            future=True,
            pool_pre_ping=True if not database_url.startswith("sqlite") else False,
        )
    return engine


def get_session_factory():
    """Get or create the session factory."""
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = sessionmaker(
            get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    current_engine = get_engine()
    async with current_engine.begin() as conn:
        # Import all models here to ensure they are registered with SQLAlchemy
        from ..models import user  # noqa: F401

        await conn.run_sync(Base.metadata.create_all)
