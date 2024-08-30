from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from src.database.models import User
from src.api.v1.user.user_dto import UpdateUserInfo, ReadUserInfo
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.fernet import Fernet
from decouple import config
from src.database.session import rdb

FERNET_KEY = config("FERNET_KEY").encode()
fernet = Fernet(FERNET_KEY)

@rdb.dao()
async def get_users(db: AsyncSession) -> list[User]:
    '''
    모든 유저 정보 가져오는 함수
    '''
    result = await db.execute(select(User))
    users_info = result.scalars().all()
    return users_info

@rdb.dao()
async def get_user(user_id: str, db: AsyncSession) -> list[User]:
    '''
    특정 유저 정보를 조회하는 함수
    '''
    stmt = select(User).where(User.user_email == user_id)
    result = await db.execute(stmt)
    user_info = result.scalars().all()
    return user_info

@rdb.dao(transactional=True)
async def delete_user(user_id: str, db: AsyncSession) -> None:
    '''
    특정 유저를 삭제하는 함수
    '''
    stmt = delete(User).where(User.user_email == user_id)
    await db.execute(stmt)
    await db.commit()

@rdb.dao(transactional=True)
async def update_user(user_id: str, user_info: UpdateUserInfo, db: AsyncSession) -> bool:
    '''
    특정 유저의 정보를 수정하는 함수
    '''
    try:
        query = select(User).where(User.user_email == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:
            # 현재 비밀번호 검증
            try:
                decrypted_password = fernet.decrypt(user.user_password.encode()).decode()
                is_current_password_correct = decrypted_password == user_info.present_user_password

                if is_current_password_correct:
                    encrypted_new_password = fernet.encrypt(user_info.future_user_password.encode()).decode()
                    user_info_dict = user_info.dict(exclude={"present_user_password", "future_user_password"}, exclude_unset=True)
                    user_info_dict['user_password'] = encrypted_new_password
                    stmt = update(User).where(User.user_email == user_id).values(**user_info_dict)
                    await db.execute(stmt)
                    return True
                else:
                    # 현재 비밀번호가 맞지 않는 경우
                    return False
            except Exception as e:
                # 비밀번호 복호화 오류 처리
                return False
        else:
            # 사용자 정보를 찾을 수 없는 경우
            return False
    except Exception as e:
        # 오류 발생 시 로깅
        return False