from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from var.models import Star, Professor
from var.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

async def course_grade(course_id: int, star: int, comment: str, data, db: AsyncSession) -> None:
    new_grade = Star(user_email = data, count_star = star, course_comment = comment, course_id = course_id)
    db.add(new_grade)
    await db.commit()
    await db.refresh(new_grade)

async def add_like(id: int, db: AsyncSession) -> None:
    stmt = (
        update(Star)
        .where(Star.id == id)
        .values(count_like=Star.count_like + 1)
    )
    await db.execute(stmt)
    await db.commit()

async def add(professor: str, course: str, db: AsyncSession) -> None:
    data = Professor(professor = professor, course = course)
    db.add(data)
    await db.commit()
    await db.refresh(data)

async def get_course(db: AsyncSession) -> None:
    result = await db.execute(select(Professor))
    course_info = result.scalars().all()
    return course_info

