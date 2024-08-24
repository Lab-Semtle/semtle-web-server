from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import query
from var.models import User
from var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from cryptography.fernet import Fernet
from decouple import config

FERNET_KEY = config("FERNET_KEY")  # 여기에 실제 키를 설정하세요.
fernet = Fernet(FERNET_KEY)

async def get_user_by_email_and_phone(db: AsyncSession, email: str, phone: str) -> Optional[User]:
    # 비동기 쿼리 실행
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
            print(f"Decryption error: {e}")
    
    return user

async def get_user_by_phone(phone: str, db: AsyncSession) -> Optional[str]:
    # 비동기 쿼리 실행
    query = select(User).filter(User.user_phone == phone)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user:
        # 사용자 객체가 존재하면 이메일을 반환
        return user.user_email
    else:
        # 사용자 객체가 없으면 None 반환
        return None