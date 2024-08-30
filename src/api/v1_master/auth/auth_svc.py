'''
API 수정 시 참고
- 명확하게 하기 위해, import 경로 src 부터 작성하기
- 각 함수 db 세션 관련 파라미터 삭제
- 필요 없는 주석 제거, 각 함수마다 "작은따옴표 3개"로 함수 기능 설명 간단히 작성
'''
from src.api.v1_master.auth import auth_dao
from src.api.v1_master.auth.auth_dto import CreateUserInfo


async def verify(user_email: str, user_password: str) -> bool:
    ''' 회원 인증 '''
    verify = await auth_dao.verify(user_email, user_password)
    return verify


async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str) -> bool:
    ''' 유저 존재 유무 확인 '''
    is_user = await auth_dao.is_user(user_id, user_name, user_email, user_phone)
    return is_user


async def post_signup(login_info: CreateUserInfo) -> None:
    ''' 유저 생성 '''
    await auth_dao.post_signup(login_info)