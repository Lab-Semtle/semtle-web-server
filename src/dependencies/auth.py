from core.status import Status, SU, ER
from fastapi.security import OAuth2PasswordBearer
from core.security import verify_access_token
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# 토큰을 인수로 받아 유효한 토큰인지 검사한 뒤 payload의 사용자 필드를 리턴함
def authenticate(token: str = Depends(oauth2_scheme)) -> str:
	if not token:
		raise ER.INVALID_REQUEST
	decode_token = verify_access_token(token)
	return decode_token["user"]