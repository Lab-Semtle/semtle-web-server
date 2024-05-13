from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends

from api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from api.v1.user import user_service
from core.type import ResultType
from core.status import Status, SU, ER

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db

router = APIRouter(prefix="/user")


@router.get(
    "/",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_users(db: AsyncSession = Depends(get_db)):
    users_info = await user_service.get_users(db)
    return users_info


@router.post(
    "/",
    summary="신규 유저 생성",
    description="- 중복 유저 확인 기능 아직 X, 데이터베이스에 유저 추가",
    response_model=ResultType,
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
    # status_code=Status.docs(SU.CREATED)
)
async def create_user(user_info: Optional[CreateUserInfo], db: AsyncSession = Depends(get_db)):
    await user_service.create_user(user_info, db)
    return SU.CREATED

@router.delete(
    "/{user_id}",
    summary=" 유저 삭제",
    description="- 유저 삭제 but 보안기능이 없다...",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    await user_service.delete_user_by_id(user_id, db)
    return SU.SUCCESS



@router.patch(
    "/{user_id}",
    summary="유저 정보 수정",
    description="- 유저 정보 수정 비번 재확인 과정 구현 x",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
)
async def patch_user(user_id: str, user_info: UpdateUserInfo, db: AsyncSession = Depends(get_db)):
    await user_service.update_user_by_id(user_id, user_info, db)
    return SU.SUCCESS
