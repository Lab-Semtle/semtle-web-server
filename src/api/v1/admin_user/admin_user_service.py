from typing import List, Optional
from src.api.v1.admin_user import admin_user_dao
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.admin_user.admin_user_dto import (
    ReadUserInfo,
)


async def get_all_users(db: AsyncSession) -> List[ReadUserInfo]:
    ''' 승인된 모든 유저 정보를 DB에서 가져오는 함수 '''
    users_info = await admin_user_dao.get_all_users(db)
    return users_info


async def search_users(query: str, db: AsyncSession) -> List[ReadUserInfo]:
    ''' 검색어와 일치하는 유저 정보를 DB에서 가져오는 함수 '''
    users_info = await admin_user_dao.search_users(query, db)
    return users_info


async def filter_users(role: str, grade: str, db: AsyncSession) -> List[ReadUserInfo]:
    ''' 등급/권한과 일치하는 유저 정보를 DB에서 가져오는 함수 '''
    users_info = await admin_user_dao.filter_users(role, grade, db)
    return users_info


async def get_new_users(db: AsyncSession) -> List[ReadUserInfo]:
    ''' 회원가입 신청 완료, 미승인 유저 정보를 가져오는 함수 '''
    users_info = await admin_user_dao.get_new_users(db)
    return users_info


async def update_user_activate(user_email: List[str], activate: bool, db: AsyncSession) -> None:
    ''' 선택된 유저 계정을 활성화/비활성화하는 함수 '''
    await admin_user_dao.update_user_activate(user_email, activate, db)


async def update_user_role(user_email: List[str], role: str, db: AsyncSession) -> None:
    ''' 선택된 유저 권한을 변경하는 함수 '''
    await admin_user_dao.update_user_role(user_email, role, db)


async def update_user_grade(user_email: List[str], grade: str, db: AsyncSession) -> None:
    ''' 선택된 유저 등급을 변경하는 함수 '''
    await admin_user_dao.update_user_grade(user_email, grade, db)