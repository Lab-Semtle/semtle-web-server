from src.api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from src.api.v1.user import user_dao
from src.var.models import User

# 이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(db: AsyncSession) -> list[User]:
    users_info = await user_dao.get_users(db)
    return users_info


async def create_user(user_info: CreateUserInfo, db: AsyncSession) -> None:
    # 이후 전화번호, 이메일 등 중복 확인 코드 추가 예정 (dao에도 추가 필요)
    # 우선은 단순 데이터 삽입
    await user_dao.create_user(user_info, db)
