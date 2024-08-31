# from api.v1.course.course_dto import CourseGrade
# from api.v1.course import course_dao
# from fastapi import Request
# from src.lib.security import verify_access_token


# async def course_grade(couse_id: int, star: int, comment: str, request: Request) -> None:
#     access_token = request.cookies.get("access_token")
#     data = verify_access_token(access_token)
#     data = data.get('sub')
#     await course_dao.course_grade(couse_id, star, comment, data)

# async def add_like(id: int) -> None:
#     await course_dao.add_like(id)

# async def add(professor: str, course: str) -> None:
#     await course_dao.add(professor, course)

# async def get_course() -> None:
#     course_info = await course_dao.get_course()
#     return course_info