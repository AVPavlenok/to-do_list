from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from typing import Optional, List
from settings import logger, settings


DB_URL = f"postgresql+asyncpg://" \
         f"{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_db}"

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


session = async_session()
Base = declarative_base()


async def create_item(model: Base, item):
    async with session.begin():
        try:
            session.add(model(**item))
        except Exception as ex:
            raise Exception(ex)
    return True


async def get_item(model: Base, **kwargs) -> Optional[List[Base]]:
    query = select(model)
    for key, value in kwargs.items():
        query = query.where(getattr(model, key) == value)
    async with session.begin():
        user = await session.execute(query)

    return user.scalars().fetchall()


async def patch_item(model: Base, data: dict, new_values: dict):
    query = update(model).values(**new_values)

    for key, value in data.items():
        query = query.where(getattr(model, key) == value)

    async with session.begin():
        try:
            await session.execute(query)
        except Exception as ex:
            raise Exception(ex)

    return True


async def delete_item(model: Base, **kwargs):
    query = delete(model)
    for key, value in kwargs.items():
        query = query.where(getattr(model, key) == value)

    async with session.begin():
        try:
            await session.execute(query)
        except Exception as ex:
            raise Exception(ex)

    return True
