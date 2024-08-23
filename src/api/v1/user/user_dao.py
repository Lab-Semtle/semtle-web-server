from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from src.database.models import User
from src.api.v1.user.user_dto import UpdateUserInfo, ReadUserInfo
from src.database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from src.lib.status import Status, SU, ER

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 전체 유저 정보를 조회하는 함수
async def get_users(db: AsyncSession) -> list[User]:
    # 모든 유저 정보를 선택하는 쿼리를 실행
    result = await db.execute(select(User))
    # 결과에서 모든 유저 정보를 가져옴
    users_info = result.scalars().all()
    return users_info

# 특정 유저 정보를 조회하는 함수
async def get_user(user_id: str, db: AsyncSession) -> list[User]:
    # 특정 유저 아이디에 해당하는 유저 정보를 선택하는 쿼리 생성
    stmt = select(User).where(User.user_id == user_id)
    # 쿼리를 실행
    result = await db.execute(stmt)
    # 결과에서 해당 유저 정보를 가져옴
    user_info = result.scalars().all()
    return user_info

# 특정 유저를 삭제하는 함수
async def delete_user(user_id: str, db: AsyncSession) -> None:
    # 특정 유저 아이디에 해당하는 유저를 삭제하는 쿼리 생성
    stmt = delete(User).where(User.user_id == user_id)
    # 쿼리를 실행
    await db.execute(stmt)
    # 트랜잭션 커밋
    await db.commit()

# 특정 유저 정보를 업데이트하는 함수
async def update_user(data: str, user_info: UpdateUserInfo, db: AsyncSession) -> None:
    # 제공된 새 비밀번호를 해시화
    fhashed_password = pwd_context.hash(user_info.future_user_password)

    # 데이터베이스에서 사용자의 현재 비밀번호를 조회
    query = select(User).where(User.user_email == data)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    res = user and pwd_context.verify(user_info.present_user_password, user.user_password)
    # 사용자가 존재하고 현재 비밀번호가 일치하는지 확인
    if res:
        # 현재 비밀번호와 미래 비밀번호를 user_info에서 제거
        user_info_dict = user_info.dict(exclude={"present_user_password", "future_user_password"}, exclude_unset=True)
        # 새로 해시화된 비밀번호로 업데이트
        user_info_dict['user_password'] = fhashed_password
        # 업데이트 쿼리 생성
        stmt = update(User).where(User.user_email == data).values(**user_info_dict)
        # 업데이트 쿼리 실행
        await db.execute(stmt)
        # 트랜잭션 커밋
        await db.commit()

    return res