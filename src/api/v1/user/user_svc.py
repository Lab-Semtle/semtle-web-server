from src.api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from src.api.v1.user import user_dao
from fastapi import Request
from src.lib.security import verify_access_token

async def get_users() -> list[ReadUserInfo]:
    '''
    사용자 정보를 가져오는 함수
    '''
    users_info = await user_dao.get_users()
    return users_info

async def get_user(user_id: str) -> list[ReadUserInfo]:
    '''
    특정 사용자의 정보를 가져오는 함수
    '''
    user_info = await user_dao.get_user(user_id)
    return user_info

async def delete_user(user_id: str) -> None:
    '''사용자 정보를 삭제하는 함수'''
    res = await user_dao.delete_user(user_id)
    return res

async def update_user(user_id, user_info: UpdateUserInfo) -> None:
    '''사용자 정보를 업데이트하는 함수'''
    res = await user_dao.update_user(user_id, user_info)
    return res