# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from core.type import ResultType
from core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db

# 호출할 모듈 추가
from api.v1.user.user_dto import ReadUserInfo, CreateUserInfo, UpdateUserInfo
from api.v1.user import user_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_users(db: AsyncSession = Depends(get_db)):
    logger.info("----------전체 유저 정보 목록 조회----------")
    users_info = await user_service.get_users(db)
    return users_info

@router.get(
    "/{user_id}",
    summary="특정 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 유저 정보가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    logger.info("----------특정 유저 정보 목록 조회----------")
    user_info = await user_service.get_user(user_id, db)
    return user_info


@router.post(
    "/",
    summary="신규 유저 생성",
    description="- 중복 유저 확인 기능 아직 X, 데이터베이스에 유저 추가",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
)
async def create_user(user_info: Optional[CreateUserInfo], db: AsyncSession = Depends(get_db)):
    logger.info("----------신규 유저 생성----------")
    await user_service.create_user(user_info, db)
    return SU.CREATED

@router.patch(
    "/",
    summary="유저 정보 수정",
    description="- 유저 정보 수정 비번 재확인 과정 구현 x",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
)
async def update_user(user_id: str, user_info: UpdateUserInfo, db: AsyncSession = Depends(get_db)):
    logger.info("----------유저 정보 수정----------")
    await user_service.update_user(user_id, user_info, db)
    return SU.SUCCESS

@router.delete(
    "/",
    summary=" 유저 삭제",
    description="- 유저 삭제",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    logger.info("----------유저 삭제----------")
    await user_service.delete_user(user_id, db)
    return SU.SUCCESS
