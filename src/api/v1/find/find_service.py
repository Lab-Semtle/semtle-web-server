import logging
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.find.find_dao import get_user_by_email_and_phone, get_user_by_phone
from api.v1.find.find_dto import FindPWRequest
from typing import Optional

logger = logging.getLogger(__name__)

async def find_password(email: str, phone: str, db: AsyncSession) -> Optional[str]:
    try:
        # 이메일과 전화번호로 사용자 조회
        user = await get_user_by_email_and_phone(db, email, phone)

        if user and user.user_password:
            # 사용자 존재 시 복호화된 비밀번호 반환
            return user.user_password
        else:
            # 사용자 정보가 없거나 비밀번호가 없는 경우 None 반환
            return None
    except Exception as e:
        # 오류 발생 시 로깅 및 예외 처리
        logger.error(f"Error finding password: {e}")
        raise

async def find_email_(phone: str, db: AsyncSession) -> Optional[str]:
    try:
        # 전화번호로 이메일 조회
        email = await get_user_by_phone(phone, db)

        if email:
            return email
        else:
            # 전화번호에 해당하는 사용자가 없는 경우
            return None
    except Exception as e:
        # 오류 발생 시 로깅 및 예외 처리
        logger.error(f"Error getting email by phone: {e}")
        raise