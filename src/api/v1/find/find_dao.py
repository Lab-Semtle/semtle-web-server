import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from var.models import User
from cryptography.fernet import Fernet
from decouple import config

logger = logging.getLogger(__name__)

# 환경 변수에서 암호화 키를 가져와 설정
FERNET_KEY = config("FERNET_KEY")
fernet = Fernet(FERNET_KEY)

async def get_user_by_email_and_phone(db: AsyncSession, email: str, phone: str) -> Optional[User]:
    """
    이메일과 전화번호로 사용자 정보를 조회합니다.
    """
    query = select(User).filter(User.user_email == email, User.user_phone == phone)
    result = await db.execute(query)
    user = result.scalars().first()

    if user and user.user_password:
        try:
            # 비밀번호 복호화
            decrypted_password = fernet.decrypt(user.user_password.encode()).decode()
            user.user_password = decrypted_password
        except Exception as e:
            # 복호화 오류 처리
            logger.error(f"복호화 중 오류 발생: {e}")
    
    return user

async def get_user_by_phone(phone: str, db: AsyncSession) -> Optional[str]:
    """
    전화번호로 사용자 이메일을 조회합니다.
    """
    query = select(User).filter(User.user_phone == phone)
    result = await db.execute(query)
    user = result.scalars().first()

    if user:
        return user.user_email
    return None
