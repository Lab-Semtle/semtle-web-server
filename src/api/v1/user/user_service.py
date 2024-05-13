from api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from api.v1.user import user_dao
from var.models import User

# 이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(db: AsyncSession) -> list[User]:
    users_info = await user_dao.get_users(db)
    return users_info


async def create_user(user_info: CreateUserInfo, db: AsyncSession) -> None:
    # 이후 전화번호, 이메일 등 중복 확인 코드 추가 예정 (dao에도 추가 필요)
    # 우선은 단순 데이터 삽입
    await user_dao.create_user(user_info, db)

async def delete_user_by_id(user_id: str, db: AsyncSession) -> None:
    await user_dao.delete_user_by_id(user_id, db)



async def update_user_by_id(user_id: str, user_info: UpdateUserInfo, db: AsyncSession) -> None:
    user_data = user_info.dict(exclude_unset=True)
    await user_dao.update_user_by_id(user_id,user_info, db, user_data)




