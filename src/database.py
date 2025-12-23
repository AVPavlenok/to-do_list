
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from settings import logger, settings


DB_URL = f"postgresql+asyncpg://" \
         f"{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_db}"

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


session = async_session()
Base = declarative_base()



