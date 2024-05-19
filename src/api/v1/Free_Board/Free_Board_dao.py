"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.Free_Board.Free_Board_dto import UpdateBoard, ReadBoard, CreateBoard
from src.var.models import Free_Board
from src.var.session import get_db


# Read
async def get_Free_Board(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[ReadBoard]:  # = Depends(get_db)
    result = await db.execute(select(Free_Board).order_by(Free_Board.Board_no.desc()))
    Total = result.count()
    Board_info = result.offset(skip).limit(limit).all()
    return Total, Board_info


# Create
async def create_Free_Board(Board: CreateBoard, db: AsyncSession) -> None:
    await db.execute(insert(Free_Board).values(Board.dict()))
    await db.commit() # 자동으로 commit되게 설정 변경 필요
    
    
# Update
async def update_Free_Board(Board_no: int, Board_info: UpdateBoard, db: AsyncSession) -> None:
    await db.execute(update(Free_Board).filter(Free_Board.Board_no == Board_no).values(Board_info.dict()))
    await db.commit()
    

# Delete
async def delete_Free_Board(Board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Free_Board).where(Free_Board.Board_no == Board_no))
    await db.commit()