from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from var.models import User
from api.v1.login.login_dto import CreateUserInfo
from var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

async def verify(user_id: str, user_password: str, db: AsyncSession) -> bool:
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one()
        if user.user_password == user_password:
            return True
        else:
            return False   # 아이디 존재 O, 비번 일치 X
    except:
        return False     # 아이디 존재 X

async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    user_data = login_info.model_dump()
    stmt = insert(User).values(**user_data)
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

