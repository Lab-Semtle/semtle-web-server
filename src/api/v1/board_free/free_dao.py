"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.api.v1_ewha.free_board_comment import free_board_comment_dao
from src.api.v1_ewha.free_board.free_board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.database.models import Free_Board


# Read List
async def get_free_board_list(db: AsyncSession, skip: int) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(Free_Board).order_by(Free_Board.Board_no.desc()).offset(skip*10).limit(10))
    free_board_info = result.scalars().all()
    total = await db.execute(select(func.count(Free_Board.Board_no)))
    total = total.scalar()
    return total, free_board_info

# Read
async def get_free_board(db: AsyncSession, free_board_no: int) -> ReadBoard:
    result = await db.execute(select(Free_Board).filter(Free_Board.Board_no == free_board_no))
    free_board_info = result.scalars().first()
    return free_board_info


# Create
async def create_free_board(free_board_info: CreateBoard, db: AsyncSession):
    create_values = free_board_info.dict()
    create_values['Create_date'] = datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
    await db.execute(insert(Free_Board).values(create_values))

    
    
# Update
async def update_free_board(free_board_no: int, free_board_info: UpdateBoard, db: AsyncSession) -> None:
    await db.execute(update(Free_Board).filter(Free_Board.Board_no == free_board_no).values(free_board_info.dict()))

    

# Delete
async def delete_free_board(free_board_no: int, db: AsyncSession) -> None:
    await free_board_comment_dao.all_delete_free_board_comment(free_board_no, db)
    await db.execute(delete(Free_Board).filter(Free_Board.Board_no == free_board_no))


#sort
async def sort_free_board(db: AsyncSession, skip: int, sel: int) -> tuple[int, list[ReadBoardlist]]:
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
    free_board_info = result.scalars().all()
    total = await db.execute(select(func.count(Free_Board.Board_no)))
    total = total.scalar()
    return total, free_board_info



