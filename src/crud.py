from sqlalchemy import update, delete
from sqlalchemy.future import select

from typing import Optional, List


async def create_item(model, session, item: dict):
    async with session.begin():
        try:
            session.add(model(**item))
        except Exception as ex:
            raise Exception(ex)
    return True


async def get_item(model, session, **kwargs) -> Optional[list]:
    query = select(model)
    for key, value in kwargs.items():
        query = query.where(getattr(model, key) == value)
    async with session.begin():
        user = await session.execute(query)

    return user.scalars().fetchall()


async def patch_item(model, session, data: dict, new_values: dict):
    query = update(model).values(**new_values)

    for key, value in data.items():
        query = query.where(getattr(model, key) == value)

    async with session.begin():
        try:
            await session.execute(query)
        except Exception as ex:
            raise Exception(ex)

    return True


async def delete_item(model, session, **kwargs):
    query = delete(model)
    for key, value in kwargs.items():
        query = query.where(getattr(model, key) == value)

    async with session.begin():
        try:
            await session.execute(query)
        except Exception as ex:
            raise Exception(ex)

    return True
