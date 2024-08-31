from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from cryptography.fernet import Fernet
from src.api.v1.login.login_dto import CreateUserInfo
from src.database.models import User
from decouple import config
from src.database.session import rdb

FERNET_KEY = config("FERNET_KEY").encode()
fernet = Fernet(FERNET_KEY)

@rdb.dao()
async def verify(user_email: str, user_password: str, db: AsyncSession) -> bool:
    """
    주어진 이메일과 비밀번호로 사용자를 인증하는 함수
    """
    try:
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
            return False
    except Exception as e:
        return False

@rdb.dao(transactional=True)
async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> bool:
    """
    새로운 사용자를 데이터베이스에 생성하는 함수.
    """
    try:
        # 비밀번호를 암호화
        encrypted_password = fernet.encrypt(login_info.user_password.encode()).decode()

        user_data = login_info.model_dump()
        user_data['user_password'] = encrypted_password
        stmt = insert(User).values(**user_data)
        await db.execute(stmt)
        return True
    except Exception as e:
        return False

@rdb.dao()
async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    """
    주어진 사용자 정보로 사용자가 존재하는지 확인하는 함수
    """
    try:
        stmt = select(User).where(
            (User.user_id == user_id) |
            (User.user_name == user_name) |
            (User.user_email == user_email) |
            (User.user_phone == user_phone)
        )
        result = await db.execute(stmt)
        return result.scalars().first() is not None
    except Exception as e:
        return False
