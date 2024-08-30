from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query, selectinload
from src.database.models import User, Grade
from src.database.session import get_db
from fastapi import Depends
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.admin_user.admin_user_dto import (
    ReadUserInfo,
    ReadFilterUser
)

async def get_all_users(db: AsyncSession) -> List[ReadUserInfo]:
    ''' 모든 유저 조회(조건: 승인됨)'''
    result = await db.execute(select(User).options(selectinload(User.grade)).filter(User.user_activate == True))
    return result.scalars().all()


async def get_search_users(query: str, db: AsyncSession) -> List[ReadUserInfo]:
    ''' query에 따라 필터링된 유저 조회 '''
    result = await db.execute(select(User).options(selectinload(User.grade)).filter(
        User.user_activate == True,
        (User.user_name.contains(query)) |
        (User.user_nickname.contains(query)) |
        (User.user_email.contains(query))
    ))
    return result.scalars().all()


async def get_filter_users_by_role(role: str, db: AsyncSession) -> List[ReadUserInfo]:
    ''' role에 따라 필터링된 유저 조회 '''
    result = await db.execute(select(User).options(selectinload(User.grade)).filter(User.user_role == role, User.user_activate == True))
    return result.scalars().all()


async def get_filter_users_by_grade(grade: str, db: AsyncSession) -> List[ReadUserInfo]:
    ''' grade에 따라 필터링된 유저 조회 '''
    result = await db.execute(select(User).join(Grade).options(selectinload(User.grade)).filter(Grade.grade_grade == grade, User.user_activate == True))
    return result.scalars().all()


async def get_new_users(db: AsyncSession) -> List[ReadUserInfo]:
    ''' 미승인된 모든 유저 조회 '''
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
