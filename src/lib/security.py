from jose import jwt, JWTError
from datetime import timedelta, datetime
from decouple import config
from fastapi import HTTPException, status, Request
from core.status import Status, SU, ER
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_ACCESS_KEY = config("JWT_SECRET_ACCESS_KEY")
SECRET_REFRESH_KEY = config("JWT_SECRET_REFRESH_KEY")
ALGORITHM = config("JWT_ALGORITHM")

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰을 검증하는 함수
def verify_access_token(token: str):
	try:
	    # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
		data = jwt.decode(token, SECRET_ACCESS_KEY, algorithms=ALGORITHM)
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

def verify_refresh_token(token: str):
	try:
	    # 토큰을 decode한 값을 data에 저장한다.
        # 이 단계에서 decode되지 않으면 당연히 검증된 토큰이 아니다.
		data = jwt.decode(token, SECRET_REFRESH_KEY, algorithms=ALGORITHM)
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


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="유효하지 않은 인증 방식입니다.")
            if not self.verify_jwt_access(credentials.credentials):
                raise HTTPException(status_code=403, detail="유효하지 않거나 만료된 토큰입니다.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="유효하지 않은 인증 코드입니다.")

    def verify_jwt_access(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = verify_access_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid

    async def get_user(self, request: Request):
        access_token = request.cookies.get("access_token")
        data = verify_access_token(access_token)
        data = data.get('sub')
        return data