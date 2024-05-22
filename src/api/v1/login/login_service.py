# 호출할 모듈 추가
from api.v1.login import login_dao
from api.v1.login.login_dto import CreateUserInfo

# 이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession

async def verify(user_id: str, user_password: str, db: AsyncSession) -> None:
    verify = await login_dao.verify(user_id, user_password, db)
    return verify

async def is_user(user_id: str, user_name: str, user_email: str, user_phone: str, db: AsyncSession) -> None:
    is_user = await login_dao.is_user(user_id, user_name, user_email, user_phone, db)
    return is_user

async def post_signup(login_info: CreateUserInfo, db: AsyncSession) -> None:
    await login_dao.post_signup(login_info, db)