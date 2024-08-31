# # 기본적으로 추가
# from typing import Annotated, Optional
# from fastapi import APIRouter, Depends, Request
# from src.lib.type import ResultType
# from src.lib.status import Status, SU, ER
# from api.v1.course.course_dto import CourseGrade
# from src.api.v1.course import course_svc
# from src.lib.security import JWTBearer
# import logging
# logger = logging.getLogger(__name__)


# router = APIRouter(prefix="/course", tags=["course"])

# @router.post(
#     "/",
#     summary="별점 및 강의평",
#     description="- 별점 및 강의평",
#     responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
#     dependencies=[Depends(JWTBearer())],
# )
# async def course_grade(couse_id: int, star: int, comment: str, request: Request):
#     logger.info("----------별점 및 강의평----------")
#     await course_svc.course_grade(couse_id, star, comment, request)
#     return SU.SUCCESS

# @router.post(
#     "/add_like",
#     summary="좋아요",
#     description="- 좋아요 수",
#     responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
#     dependencies=[Depends(JWTBearer())],
# )
# async def add_like(id: int):
#     logger.info("----------좋아요----------")
#     await course_svc.add_like(id)
#     return SU.SUCCESS

# @router.post(
#     "/add",
#     summary="강의 추가",
#     description="- 강의 추가",
#     responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
#     # dependencies=[Depends(JWTBearer())],
# )
# async def add(professor: str, course: str):
#     logger.info("----------강의 추가----------")
#     await course_svc.add(professor, course)
#     return SU.SUCCESS

# @router.get(
#     "/",
#     summary="강의 목록 전체 조회",
#     description="- 강의 목록 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
#     responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
# )
# async def get_course():
#     logger.info("----------전체 유저 정보 목록 조회----------")
#     course_info = await course_svc.get_course()
#     return course_info

