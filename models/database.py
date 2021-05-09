from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

POSTGRES_DB_URL = "postgresql+asyncpg://postgres:Mywings@localhost/postgres"

engine = create_async_engine(POSTGRES_DB_URL)

Base = declarative_base()

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
