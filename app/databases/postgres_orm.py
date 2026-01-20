from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

engine = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


def init_engine(dsn: str) -> None:
    global engine, AsyncSessionLocal

    engine = create_async_engine(
        dsn,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("Database engine is not initialized")

    async with AsyncSessionLocal() as session:
        yield session
