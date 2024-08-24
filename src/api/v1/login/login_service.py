# 호출할 모듈 추가
from api.v1.login import login_dao
from api.v1.login.login_dto import CreateUserInfo
import aiosmtplib
from email.message import EmailMessage
import random
import string

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession

import logging

logger = logging.getLogger(__name__)

random_string = ""

def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


# 사용자를 인증하는 서비스 함수
async def verify(user_email: str, user_password: str, db: AsyncSession) -> bool:
    # 데이터 접근 객체(DAO)를 사용하여 사용자 인증 확인
    verify = await login_dao.verify(user_email, user_password, db)
    return verify

# 사용자가 존재하는지 확인하는 서비스 함수
async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    # 데이터 접근 객체(DAO)를 사용하여 사용자 존재 여부 확인
    is_user = await login_dao.is_user(user_id, user_name, user_email, user_phone, db)
    return is_user

# 사용자를 생성하는 서비스 함수
async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    # 데이터 접근 객체(DAO)를 사용하여 사용자 생성
    await login_dao.post_signup(login_info, db)

async def send_confirmation_email(user_email: str):
    global random_string
    random_string = generate_random_string()
    message = EmailMessage()
    message["From"] = "LabSebtle@gmail.com"
    message["To"] = user_email
    message["Subject"] = "안녕하세요! 아치 셈틀 홈페이지에 회원가입 하신 것을 축하드립니다!"
    message.set_content(f'인증 번호는 {random_string} 입니다.')

    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username="",
            password="",
        )
        logger.info(f"Confirmation email sent to {user_email}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {user_email}: {e}")

async def verify_email(code, user_email, db: AsyncSession):
    if random_string == code:
        await login_dao.verify_email(user_email, db)
        return True
    else:
        return False