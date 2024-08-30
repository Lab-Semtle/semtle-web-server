# 모듈 호출
from api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from api.v1.user import user_dao
from fastapi import Request
from core.security import verify_access_token

# 사용되지 않는 모듈은 삭제될 예정입니다.
from sqlalchemy.ext.asyncio import AsyncSession

# 사용자 정보를 가져오는 함수
async def get_users(db: AsyncSession) -> list[ReadUserInfo]:
    # 사용자 정보를 데이터베이스로부터 가져옵니다.
    users_info = await user_dao.get_users(db)
    return users_info

# 특정 사용자의 정보를 가져오는 함수
async def get_user(user_id: str, db: AsyncSession) -> list[ReadUserInfo]:
    # 특정 사용자의 정보를 데이터베이스로부터 가져옵니다.
    user_info = await user_dao.get_user(user_id, db)
    return user_info

# 사용자 정보를 삭제하는 함수
async def delete_user(user_id: str, db: AsyncSession) -> None:
    # 사용자 정보를 데이터베이스에서 삭제합니다.
    await user_dao.delete_user(user_id, db)

# 사용자 정보를 업데이트하는 함수
async def update_user(user_id, user_info: UpdateUserInfo, db: AsyncSession) -> None:
    # 사용자 정보를 업데이트합니다.
    res = await user_dao.update_user(user_id, user_info, db)
    return res