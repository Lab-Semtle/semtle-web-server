from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.status import Status, SU, ER
from core.security import JWTBearer
import logging
from api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from api.v1.user import user_service
from var.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])

# 전체 유저 정보 목록 조회 엔드포인트
@router.get(
    "/view_all",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    logger.info("전체 유저 정보 목록 조회")
    users_info = await user_service.get_users(db)
    return users_info

# 특정 유저 정보 조회 엔드포인트
@router.get(
    "/view_one",
    summary="특정 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 유저 정보가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_user(user_id: Annotated[str,Depends(JWTBearer().get_user)], db: AsyncSession = Depends(get_db)):
    logger.info(f"특정 유저 정보 조회: {user_id}")
    user_info = await user_service.get_user(user_id, db)
    return user_info

# 유저 정보 수정 엔드포인트
@router.patch(
    "/user_info_modify",
    summary="유저 정보 수정",
    description="- ",
    responses=Status.docs(SU.ACCEPTED, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def update_user(user_id: Annotated[str,Depends(JWTBearer().get_user)], user_info: UpdateUserInfo, db: AsyncSession = Depends(get_db)):
    logger.info(f"유저 정보 수정: {user_id}")
    res = await user_service.update_user(user_id, user_info, db)
    if res:
        return SU.ACCEPTED
    else:
        return ER.NOT_FOUND

# 유저 삭제 엔드포인트
@router.delete(
    "/user_delete",
    summary="유저 삭제",
    description="- 유저 삭제",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def delete_user(user_id: Annotated[str,Depends(JWTBearer().get_user)], db: AsyncSession = Depends(get_db)):
    logger.info(f"유저 삭제: {user_id}")
    await user_service.delete_user(user_id, db)
    return SU.SUCCESS