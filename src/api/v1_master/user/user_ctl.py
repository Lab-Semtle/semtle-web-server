# 기본적으로 추가
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Request
from core.type import ResultType
from core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db

# 호출할 모듈 추가
from api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from src.api.v1.user import user_svc
from src.lib.security import JWTBearer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])

# 전체 유저 정보 목록 조회 엔드포인트
@router.get(
    "/",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    logger.info("----------전체 유저 정보 목록 조회----------")
    users_info = await user_svc.get_users(db)
    return users_info

# 특정 유저 정보 조회 엔드포인트
@router.get(
    "/{user_id}",
    summary="특정 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 유저 정보가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    logger.info("----------특정 유저 정보 목록 조회----------")
    user_info = await user_svc.get_user(user_id, db)
    return user_info

# 유저 정보 수정 엔드포인트
@router.patch(
    "/",
    summary="유저 정보 수정",
    description="- ",
    responses=Status.docs(SU.ACCEPTED, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def update_user(request: Request, user_info: UpdateUserInfo, db: AsyncSession = Depends(get_db)):
    logger.info("----------유저 정보 수정----------")
    res = await user_svc.update_user(request, user_info, db)
    if res:
        return SU.ACCEPTED
    else:
        return ER.NOT_FOUND

# 유저 삭제 엔드포인트
@router.delete(
    "/",
    summary="유저 삭제",
    description="- 유저 삭제",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    logger.info("----------유저 삭제----------")
    await user_svc.delete_user(user_id, db)
    return SU.SUCCESS
