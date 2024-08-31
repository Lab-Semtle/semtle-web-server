# from sqlalchemy import Result, ScalarResult, select, update, insert, delete
# from sqlalchemy.orm import joinedload, query
# from src.database.models import Star, Professor
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.database.session import rdb


# @rdb.dao(transactional=True)
# async def course_grade(course_id: int, star: int, comment: str, data, db: AsyncSession) -> None:
#     new_grade = Star(user_email = data, count_star = star, course_comment = comment, course_id = course_id)
#     db.add(new_grade)
#     await db.refresh(new_grade)

# @rdb.dao(transactional=True)
# async def add_like(id: int, db: AsyncSession) -> None:
#     stmt = (
#         update(Star)
#         .where(Star.id == id)
#         .values(count_like=Star.count_like + 1)
#     )
#     await db.execute(stmt)

# @rdb.dao(transactional=True)
# async def add(professor: str, course: str, db: AsyncSession) -> None:
#     data = Professor(professor = professor, course = course)
#     db.add(data)
#     await db.refresh(data)

# @rdb.dao()
# async def get_course(db: AsyncSession) -> None:
#     result = await db.execute(select(Professor))
#     course_info = result.scalars().all()
#     return course_info

