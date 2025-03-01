from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.settings import settings


engine = create_async_engine(
    settings.DB_CONNECTION_STRING,
    echo=settings.DB_LOG_QUERIES,
    future=True,
)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
