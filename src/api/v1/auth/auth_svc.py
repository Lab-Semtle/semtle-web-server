from src.api.v1.auth import auth_dao
from src.api.v1.auth.auth_dto import CreateUserInfo
import aiosmtplib
from email.message import EmailMessage
import random
import string
# from decouple import config
from src.core import settings


random_string = ""
USERNAME = settings.general.SEND_EMAIL_USERNAME
PASSWARD = settings.general.SEND_EMAIL_PASSWORD

def generate_random_string(length=6) -> str:
    '''
    랜덤 문자열을 생성하는 함수
    '''
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def verify(user_email: str, user_password: str) -> bool:
    '''
    주어진 이메일과 비밀번호로 사용자를 인증하는 함수
    '''
    return await auth_dao.verify(user_email, user_password)

async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str) -> bool:
    '''
    주어진 사용자 정보로 사용자가 존재하는지 확인하는 함수
    '''
    return await auth_dao.is_user(user_id, user_name, user_email, user_phone)

async def post_signup(login_info: CreateUserInfo) -> None:
    '''
    새로운 사용자를 생성하는 함수
    '''
    await auth_dao.post_signup(login_info)

async def send_confirmation_email(user_email: str) -> None:
    '''
    사용자에게 인증 이메일을 전송하는 함수
    '''
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
    except Exception as e:
        ...

async def verify_email(code) -> bool:
    '''
    사용자가 입력한 코드와 저장된 코드를 비교하여 일치 여부를 반환하는 함수
    '''
    global random_string
    if random_string == code:
        return True
    else:
        return False

async def code() -> str:
    '''
    최근 생성된 인증 코드를 반환하는 함수
    '''
    global random_string
    return random_string