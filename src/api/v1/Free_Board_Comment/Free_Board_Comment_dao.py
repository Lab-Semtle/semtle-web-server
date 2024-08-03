"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, select, update, insert, delete, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.api.v1.Free_Board_Comment.Free_Board_Comment_dto import UpdateComment, ReadComment, CreateComment
from src.var.models import Free_Board_Comment
from src.var.session import get_db


# Read
async def get_Free_Board_Comment(Free_Board_no: int, db: AsyncSession) -> list[ReadComment]:
    result = await db.execute(select(Free_Board_Comment).filter(Free_Board_Comment.Board_no == Free_Board_no).order_by(Free_Board_Comment.Create_date.desc()))
    Comment_info = result.scalars().all()
    return Comment_info


# Create
async def create_Free_Board_Comment(Comment_info: CreateComment, db: AsyncSession):
    create_values = Comment_info.dict()
    create_values['Create_date'] = datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
    await db.execute(insert(Free_Board_Comment).values(create_values))
    await db.commit()
    
    
# Update
async def update_Free_Board_Comment(Free_Board_no: int, Comment_no: int, Comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(Free_Board_Comment).filter(Free_Board_Comment.Board_no == Free_Board_no).filter(Free_Board_Comment.Comment_no == Comment_no).values(Comment_info.dict()))
    await db.commit()
    

# Delete
async def delete_Free_Board_Comment(Free_Board_no: int, Comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Free_Board_Comment).filter(Free_Board_Comment.Board_no == Free_Board_no).filter(Free_Board_Comment.Comment_no == Comment_no))
    await db.commit()