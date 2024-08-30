import logging
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.find.find_dao import get_user_by_email_and_phone, get_user_by_phone
from typing import Optional

logger = logging.getLogger(__name__)

async def find_password(email: str, phone: str, db: AsyncSession) -> Optional[str]:
    """
    이메일과 전화번호를 사용하여 사용자의 비밀번호를 찾습니다.
    """
    try:
        # 이메일과 전화번호로 사용자 조회
        user = await get_user_by_email_and_phone(db, email, phone)

        # 사용자가 존재하고 비밀번호가 있는 경우 반환
        if user and user.user_password:
            return user.user_password
        else:
            return None
    except Exception as e:
        # 오류 발생 시 로깅
        logger.error(f"비밀번호를 찾는 중 오류 발생: {e}")
        raise

async def find_email_(phone: str, db: AsyncSession) -> Optional[str]:
    """
    전화번호를 사용하여 사용자의 이메일을 찾습니다.
    """
    try:
        # 전화번호로 이메일 조회
        email = await get_user_by_phone(phone, db)

        # 이메일이 있는 경우 반환
        if email:
            return email
        else:
            return None
    except Exception as e:
        # 오류 발생 시 로깅
        logger.error(f"이메일을 찾는 중 오류 발생: {e}")
        raise
