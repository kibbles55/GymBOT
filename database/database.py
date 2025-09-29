from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone

# SQLite Async
DATABASE_URL = "sqlite+aiosqlite:///database.db"

# Двигун
engine = create_async_engine(DATABASE_URL, echo=True)

# База моделей
Base = declarative_base()


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def utc_now():
    return datetime.now(timezone.utc)
