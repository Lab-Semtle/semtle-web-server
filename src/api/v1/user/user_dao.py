from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from var.models import User
from api.v1.user.user_dto import UpdateUserInfo, ReadUserInfo
from var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from core.status import Status, SU, ER
from cryptography.fernet import Fernet
from decouple import config

FERNET_KEY = config("FERNET_KEY").encode()  # 여기에 실제 키를 설정하세요.
fernet = Fernet(FERNET_KEY)

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

async def update_user(data: str, user_info: UpdateUserInfo, db: AsyncSession) -> bool:
    try:
        # 데이터베이스에서 사용자의 현재 비밀번호를 조회
        query = select(User).where(User.user_email == data)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:
            # 현재 비밀번호 검증
            try:
                decrypted_password = fernet.decrypt(user.user_password.encode()).decode()
                is_current_password_correct = decrypted_password == user_info.present_user_password

                if is_current_password_correct:
                    # 새 비밀번호 암호화
                    encrypted_new_password = fernet.encrypt(user_info.future_user_password.encode()).decode()

                    # 현재 비밀번호와 미래 비밀번호를 user_info에서 제거
                    user_info_dict = user_info.dict(exclude={"present_user_password", "future_user_password"}, exclude_unset=True)
                    
                    # 새로 암호화된 비밀번호로 업데이트
                    user_info_dict['user_password'] = encrypted_new_password

                    # 업데이트 쿼리 생성
                    stmt = update(User).where(User.user_email == data).values(**user_info_dict)
                    
                    # 업데이트 쿼리 실행
                    await db.execute(stmt)
                    
                    # 트랜잭션 커밋
                    await db.commit()

                    return True
                else:
                    # 현재 비밀번호가 맞지 않는 경우
                    return False
            except Exception as e:
                # 비밀번호 복호화 오류 처리
                logger.error(f"Error decrypting password: {e}")
                return False
        else:
            # 사용자 정보를 찾을 수 없는 경우
            return False
    except Exception as e:
        # 오류 발생 시 로깅
        logger.error(f"Error updating user: {e}")
        return False