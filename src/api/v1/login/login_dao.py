from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.fernet import Fernet
from api.v1.login.login_dto import CreateUserInfo
from var.models import User
from decouple import config
import logging

logger = logging.getLogger(__name__)

FERNET_KEY = config("FERNET_KEY").encode()
fernet = Fernet(FERNET_KEY)

# 사용자 인증 함수
async def verify(user_email: str, user_password: str, db: AsyncSession) -> bool:
    """
    주어진 이메일과 비밀번호로 사용자를 인증합니다.
    """
    try:
        # 데이터베이스에서 사용자 정보를 조회
        result = await db.execute(select(User).where(User.user_email == user_email))
        user = result.scalar_one_or_none()

        if not user:
            # 사용자 정보를 찾을 수 없는 경우
            return False

        try:
            # 비밀번호 복호화 및 확인
            decrypted_password = fernet.decrypt(user.user_password.encode()).decode()
            return decrypted_password == user_password
        except Exception as e:
            # 비밀번호 복호화 오류 처리
            logger.error(f"비밀번호 복호화 오류: {e}")
            return False
    except Exception as e:
        # 오류 발생 시 로깅
        logger.error(f"사용자 인증 오류: {e}")
        return False

# 회원가입 함수
async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    """
    새로운 사용자를 데이터베이스에 생성합니다.
    """
    try:
        # 비밀번호를 암호화
        encrypted_password = fernet.encrypt(login_info.user_password.encode()).decode()

        # 사용자 데이터를 딕셔너리로 변환 후 암호화된 비밀번호로 설정
        user_data = login_info.model_dump()
        user_data['user_password'] = encrypted_password

        # 사용자 데이터를 데이터베이스에 삽입
        stmt = insert(User).values(**user_data)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        logger.error(f"회원가입 오류: {e}")

# 사용자 존재 여부 확인 함수
async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    """
    주어진 사용자 정보로 사용자가 존재하는지 확인합니다.
    """
    try:
        # 사용자 정보를 조회하는 선택 명령문 생성
        stmt = select(User).where(
            (User.user_id == user_id) |
            (User.user_name == user_name) |
            (User.user_email == user_email) |
            (User.user_phone == user_phone)
        )
        # 데이터베이스에서 명령문 실행 및 사용자가 존재하는지 확인
        result = await db.execute(stmt)
        return result.scalars().first() is not None
    except Exception as e:
        logger.error(f"사용자 존재 여부 확인 오류: {e}")
        return False
