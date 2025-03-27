from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Функция для получения сессии
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Создаем асинхронный sessionmaker
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

# Зависимость для получения асинхронной сессии
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session