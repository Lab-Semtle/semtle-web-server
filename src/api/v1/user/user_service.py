from src.api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from src.api.v1.user import user_dao
from src.var.models import User
from fastapi import Depends


async def get_users_info() -> list[User]:
    users_info = await user_dao.get_users_info()
    return users_info
