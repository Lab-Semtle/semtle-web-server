from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from var.models import User
from api.v1.user.user_dto import CreateUserInfo, UpdateUserInfo, ReadUserInfo
from var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(db: AsyncSession) -> list[User]:  # = Depends(get_db)
    result = await db.execute(select(User))
    users_info = result.scalars().all()
    return users_info

async def get_user(user_id: str, db: AsyncSession) -> list[User]:  # = Depends(get_db)
    stmt = select(User).where(User.user_id == user_id)
    result = await db.execute(stmt)
    user_info = result.scalars().all()
    return user_info


async def create_user(user_info: CreateUserInfo, db: AsyncSession) -> None:
    user_data = user_info.model_dump()
    stmt = insert(User).values(**user_data)
    await db.execute(stmt)
    await db.commit()

async def delete_user(user_id: str, db: AsyncSession) -> None:
    stmt = delete(User).where(User.user_id == user_id)
    await db.execute(stmt)
    await db.commit()

async def update_user(user_id: str, user_info: UpdateUserInfo, db: AsyncSession, user_data) -> None:
    stmt = update(User).where(User.user_id == user_id).values(**user_data)
    await db.execute(stmt)
    await db.commit()

async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    stmt = select(User).where(
        (User.user_id == user_id) |
        (User.user_name == user_name) |
        (User.user_email == user_email) |
        (User.user_phone == user_phone)
    )
    result = await db.execute(stmt)
    user_exists = result.scalars().first() is not None
    return user_exists

