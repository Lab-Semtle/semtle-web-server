"""
API 수정 시 참고
- 모든 함수에 @rdb.dao(transactional= False / True) 추가하기
- DB 조회만 하는 경우 transactional = False, 그외 삽입,갱신,삭제의 경우 transactional=True 하기
- 참고) transactional 작성안하고 그냥 @rdb.dao() 만 적으면 트랜잭션=False 가 기본값으로 인가됨.
- transactional=True 인 경우 자동으로 commit 되므로 commit 하는 코드 제거
- 주의) 데이터베이스 세션 관련 파라미터는 무조껀 db: AsyncSession 으로 줄 것
"""
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from src.database.models import User
from src.api.v1.auth.auth_dto import CreateUserInfo
from src.database.session import rdb
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@rdb.dao()
async def verify(user_email: str, user_password: str, db: AsyncSession) -> bool:
    ''' 주어진 사용자 email과 비밀번호를 확인하는 함수 '''
    try:
        # 데이터베이스에서 사용자 정보를 조회
        result = await db.execute(select(User).where(User.user_email == user_email))
        user = result.scalar_one()
        # 비밀번호가 일치하는지 확인
        return pwd_context.verify(user_password, user.user_password) # True이면 로그인 성공, False이면 로그인 실패
    except:
        return False  # 아이디가 존재하지 않을 경우

@rdb.dao(transactional=True) # 트랜잭션 True = 자동 커밋됨.
async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    ''' 사용자를 생성하여 데이터베이스에 저장하는 함수 '''
    # 비밀번호를 해시화
    hashed_password = pwd_context.hash(login_info.user_password)
    # 사용자 데이터를 딕셔너리로 변환
    user_data = login_info.model_dump()
    # 해시화된 비밀번호로 업데이트
    user_data['user_password'] = hashed_password
    # 삽입 명령문 생성
    stmt = insert(User).values(**user_data)
    # 데이터베이스에 명령문 실행
    await db.execute(stmt)

@rdb.dao()
async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> bool:
    ''' 사용자가 존재하는지 확인하는 함수 '''
    # 사용자 정보를 조회하는 선택 명령문 생성
    stmt = select(User).where(
        (User.user_id == user_id) |
        (User.user_name == user_name) |
        (User.user_email == user_email) |
        (User.user_phone == user_phone)
    )
    # 데이터베이스에서 명령문 실행
    result = await db.execute(stmt)
    # 사용자가 존재하는지 확인
    user_exists = result.scalars().first() is not None
    return user_exists