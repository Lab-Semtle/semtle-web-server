# 호출할 모듈 추가
from api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from api.v1.user import user_dao

# 이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(db: AsyncSession) -> list[ReadUserInfo]:
    users_info = await user_dao.get_users(db)
    return users_info

async def get_user(user_id: str, db: AsyncSession) -> list[ReadUserInfo]:
    user_info = await user_dao.get_user(user_id, db)
    return user_info

async def delete_user(user_id: str, db: AsyncSession) -> None:
    await user_dao.delete_user(user_id, db)

async def update_user(user_id: str, user_info: UpdateUserInfo, db: AsyncSession) -> None:
    user_data = user_info.dict(exclude_unset=True)
    await user_dao.update_user(user_id, user_info, db, user_data)





