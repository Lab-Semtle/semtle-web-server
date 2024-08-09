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

from src.api.v1.Free_Board.Free_Board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.var.models import Free_Board
from src.var.session import get_db


# Read List
async def get_Free_Board_List(db: AsyncSession, skip: int = 0) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(Free_Board).order_by(Free_Board.Board_no.desc()).offset(skip*10).limit(10))
    Board_info = result.scalars().all()
    total = await db.execute(select(func.count(Free_Board.Board_no)))
    total = total.scalar()
    return total, Board_info

# Read
async def get_Free_Board(db: AsyncSession, Board_no: int) -> ReadBoard:
    result = await db.execute(select(Free_Board).filter(Free_Board.Board_no == Board_no))
    Board_info = result.scalars().first()
    return Board_info


# Create
async def create_Free_Board(Board: CreateBoard, db: AsyncSession):
    create_values = Board.dict()
    create_values['Create_date'] = datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
    await db.execute(insert(Free_Board).values(create_values))
    await db.commit()
    
    
# Update
async def update_Free_Board(Board_no: int, Board_info: UpdateBoard, db: AsyncSession) -> None:
    await db.execute(update(Free_Board).filter(Free_Board.Board_no == Board_no).values(Board_info.dict()))
    await db.commit()
    

# Delete
async def delete_Free_Board(Board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Free_Board).filter(Free_Board.Board_no == Board_no))
    await db.commit()

#sort
async def Sort_Free_Board(db: AsyncSession, skip: int = 0, sel: int = 0) -> tuple[int, list[ReadBoardlist]]:
    if sel == 0:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Board_no.desc()).offset(skip*10).limit(10))
    elif sel == 1:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Board_no.asc()).offset(skip*10).limit(10))
    elif sel == 2:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Create_date.desc()).offset(skip*10).limit(10))
    elif sel == 3:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Create_date.asc()).offset(skip*10).limit(10))
    elif sel == 4:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Title.asc()).offset(skip*10).limit(10))
    elif sel == 5:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Title.desc()).offset(skip*10).limit(10))
    elif sel == 6:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Views.desc()).offset(skip*10).limit(10))
    elif sel == 7:
        result = await db.execute(select(Free_Board).order_by(Free_Board.Views.asc()).offset(skip*10).limit(10))
    Board_info = result.scalars().all()
    Total = await db.execute(select(func.count(Free_Board.Board_no)))
    Total = Total.scalar()
    return Total, Board_info



