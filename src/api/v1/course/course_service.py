# 모듈 호출
from src.api.v1.course.course_dto import CourseGrade
from src.api.v1.course import course_dao
from fastapi import Request
from src.core.security import verify_access_token

# 사용되지 않는 모듈은 삭제될 예정입니다.
from sqlalchemy.ext.asyncio import AsyncSession

async def course_grade(couse_id: int, star: int, comment: str, request: Request, db: AsyncSession) -> None:
    access_token = request.cookies.get("access_token")
    data = verify_access_token(access_token)
    data = data.get('sub')
    await course_dao.course_grade(couse_id, star, comment, data, db)

async def add_like(id: int, db: AsyncSession) -> None:
    await course_dao.add_like(id, db)

async def add(professor: str, course: str, db: AsyncSession) -> None:
    await course_dao.add(professor, course, db)

async def get_course(db: AsyncSession) -> None:
    course_info = await course_dao.get_course(db)
    return course_info