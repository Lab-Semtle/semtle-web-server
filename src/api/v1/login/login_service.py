from api.v1.login import login_dao
from api.v1.login.login_dto import CreateUserInfo
import aiosmtplib
from email.message import EmailMessage
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from decouple import config

logger = logging.getLogger(__name__)

random_string = ""

USERNAME = config("username")
PASSWARD = config("password")

# 랜덤 문자열 생성
def generate_random_string(length=6) -> str:
    """
    주어진 길이의 랜덤 문자열을 생성합니다.
    영문 대소문자와 숫자를 포함합니다.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 사용자 인증 서비스 함수
async def verify(user_email: str, user_password: str, db: AsyncSession) -> bool:
    """
    주어진 이메일과 비밀번호로 사용자를 인증합니다.
    """
    return await login_dao.verify(user_email, user_password, db)

# 사용자 존재 여부 확인 서비스 함수
async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    """
    주어진 사용자 정보로 사용자가 존재하는지 확인합니다.
    """
    return await login_dao.is_user(user_id, user_name, user_email, user_phone, db)

# 사용자 생성 서비스 함수
async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    """
    새로운 사용자를 생성합니다.
    """
    await login_dao.post_signup(login_info, db)

async def send_confirmation_email(user_email: str) -> None:
    """
    사용자에게 인증 이메일을 전송합니다.
    """
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
            hostname = "smtp.gmail.com",
            port = 587,
            start_tls = True,
            username = USERNAME,
            password = PASSWARD,
        )
        logger.info(f"{user_email}으로 이메일 전송 완료.")
    except Exception as e:
        logger.error(f"{user_email}으로 이메일 전송 실패 : {e}")

# 이메일 인증 코드 검증 서비스 함수
async def verify_email(code) -> bool:
    """
    사용자가 입력한 코드와 저장된 코드를 비교하여 일치 여부를 반환합니다.
    """
    global random_string
    if random_string == code:
        return True
    else:
        return False

# 최근 생성된 코드 반환
async def code() -> str:
    """
    최근 생성된 인증 코드를 반환합니다.
    """
    global random_string
    return random_string