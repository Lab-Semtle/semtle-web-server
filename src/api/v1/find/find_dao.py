from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.database.models import User
from cryptography.fernet import Fernet
from src.database.session import rdb
from src.core import settings

FERNET_KEY = settings.general.FERNET_KEY
fernet = Fernet(FERNET_KEY)

@rdb.dao()
async def get_user_by_email_and_phone(email: str, phone: str, db: AsyncSession) -> Optional[User]:
    '''
    이메일과 전화번호로 사용자 정보를 조회하는 함수
    '''
    try:
        query = select(User).filter(User.user_email == email, User.user_phone == phone)
        result = await db.execute(query)
        user = result.scalars().first()
        if user and user.user_password:
            try:
                # 비밀번호 복호화
                decrypted_password = fernet.decrypt(user.user_password.encode()).decode()
                return decrypted_password
            except Exception as e:
                # 복호화 오류 처리
                return None
    except Exception as e:
        return None

@rdb.dao()
async def get_user_by_phone(phone: str, db: AsyncSession) -> Optional[str]:
    """
    전화번호로 사용자 이메일을 조회하는 함수
    """
    try:
        query = select(User).filter(User.user_phone == phone)
        result = await db.execute(query)
        user = result.scalars().first()
        if user:
            return user.user_email
    except Exception as e:
        return None
