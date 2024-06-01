from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query, selectinload
from src.var.models import User, Grade
from src.var.session import get_db
from fastapi import Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User).options(selectinload(User.grade)).filter(User.user_activate == True))
    return result.scalars().all()


async def search_users(query: str, db: AsyncSession) -> List[User]:
    result = await db.execute(select(User).filter(
        (User.user_name.contains(query)) |
        (User.user_nickname.contains(query)) |
        (User.user_email.contains(query))
    ).options(selectinload(User.grade)))
    return result.scalars().all()
    

async def filter_users(role: Optional[str], grade: Optional[str], db: AsyncSession) -> List[User]:
    filters = []
    if role:
        filters.append(User.user_role == role)
    if grade:
        filters.append(Grade.grade_grade == grade)
    result = await db.execute(select(User).join(Grade).filter(*filters).options(selectinload(User.grade)))
    return result.scalars().all()


async def get_new_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User).filter(User.user_activate == False))
    return result.scalars().all()


async def update_user_activate(user_email: List[str], activate: bool, db: AsyncSession):
    result = await db.execute(select(User).filter(User.user_email.in_(user_email)))
    users = result.scalars().all()
    for user in users:
        user.user_activate = activate
    await db.commit()
    

async def update_user_role(user_email: List[str], role: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.user_email.in_(user_email)))
    users = result.scalars().all()
    for user in users:
        user.user_role = role
    await db.commit()


async def update_user_grade(user_email: List[str], grade: str, db: AsyncSession):
    grade_obj = await db.execute(select(Grade).filter(Grade.grade_grade == grade))
    grade_obj = grade_obj.scalar_one_or_none()
    result = await db.execute(select(User).filter(User.user_email.in_(user_email)))
    users = result.scalars().all()
    for user in users:
        user.grade_id = grade_obj.grade_id
    await db.commit()