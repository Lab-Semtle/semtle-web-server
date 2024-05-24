from jose import jwt, JWTError
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from core.status import Status, SU, ER

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰을 검증하는 함수
def verify_access_token(token: str):
	try:
	    # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
		data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # 여기서부터 인증된 사용자의 토큰이 만료되었는지 체크한다.
		expires = data.get("exp")
		if expires is None:
			raise ER.FORBIDDEN
		if datetime.utcnow() > datetime.utcfromtimestamp(expires):
			raise ER.INVALID_REQUEST
        # 정상 토큰이라면 사용자 데이터를 리턴한다.
		return data
	except JWTError:
		ER.FORBIDDEN