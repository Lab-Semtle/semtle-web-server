import random
import string
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

otp_store = {}  # 임시로 OTP를 저장할 딕셔너리

# .env 파일에서 환경 변수 로드
load_dotenv()

# 이메일 발송 설정
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
FROM_EMAIL = os.getenv('FROM_EMAIL')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email: str):
    otp = generate_otp()
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=5)  # OTP 유효 시간 5분
    }
    # 이메일 전송 로직
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, [email], msg.as_string())
    print(f"Sending OTP {otp} to {email}")  # 로그에 출력

def verify_otp(email: str, otp: str):
    if email in otp_store:
        stored_otp = otp_store[email]
        if stored_otp["otp"] == otp and stored_otp["expires"] > datetime.utcnow():
            del otp_store[email]  # OTP가 유효하면 삭제
            return True
    return False
