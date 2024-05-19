from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from src.var.models import User
from src.api.v1.user.user_dto import CreateUserInfo, UpdateUserInfo, ReadUserInfo
from src.var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(db: AsyncSession) -> list[User]:  # = Depends(get_db)
    result = await db.execute(select(User))
    users_info = result.scalars().all()
    return users_info


async def create_user(user_info: CreateUserInfo, db: AsyncSession) -> None:
    user_data = user_info.model_dump()
    stmt = insert(User).values(**user_data)
    await db.execute(stmt)
    await db.commit()
