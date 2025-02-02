from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings


sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)


session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def create_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = [
    'sync_engine',
    'async_engine',
    'session_factory',
    'async_session_factory',
    'Base',
    'create_db'
]
