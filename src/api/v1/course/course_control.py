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
from api.v1.course.course_dto import CourseGrade
from api.v1.course import course_service
from src.lib.security import JWTBearer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/course", tags=["course"])

@router.post(
    "/",
    summary="별점 및 강의평",
    description="- 별점 및 강의평",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    dependencies=[Depends(JWTBearer())],
)
async def course_grade(couse_id: int, star: int, comment: str, request: Request, db: AsyncSession = Depends(get_db)):
    logger.info("----------별점 및 강의평----------")
    await course_service.course_grade(couse_id, star, comment, request, db)
    return SU.SUCCESS

@router.post(
    "/add_like",
    summary="좋아요",
    description="- 좋아요 수",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    dependencies=[Depends(JWTBearer())],
)
async def add_like(id: int, db: AsyncSession = Depends(get_db)):
    logger.info("----------좋아요----------")
    await course_service.add_like(id, db)
    return SU.SUCCESS

@router.post(
    "/add",
    summary="강의 추가",
    description="- 강의 추가",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    # dependencies=[Depends(JWTBearer())],
)
async def add(professor: str, course: str, db: AsyncSession = Depends(get_db)):
    logger.info("----------강의 추가----------")
    await course_service.add(professor, course, db)
    return SU.SUCCESS

@router.get(
    "/",
    summary="강의 목록 전체 조회",
    description="- 강의 목록 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
)
async def get_course(db: AsyncSession = Depends(get_db)):
    logger.info("----------전체 유저 정보 목록 조회----------")
    course_info = await course_service.get_course(db)
    return course_info

