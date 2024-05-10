from fastapi import APIRouter
from src.api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from src.api.v1.user import user_service


router = APIRouter(
    prefix="/user",
)


@router.get(
    "/",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo]
)
async def get_users_info():
    users_info = await user_service.get_users_info()
    return users_info
