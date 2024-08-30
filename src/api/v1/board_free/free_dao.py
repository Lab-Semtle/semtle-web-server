"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.api.v1.comment_free import free_board_comment_dao
from src.api.v1.board_free.free_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.database.models import FreeBoard
from src.database.session import rdb

@rdb.dao()
async def get_free_board_list(db: AsyncSession, skip: int) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(FreeBoard).order_by(FreeBoard.Board_no.desc()).offset(skip*10).limit(10))
    free_board_info = result.scalars().all()
    total = await db.execute(select(func.count(FreeBoard.Board_no)))
    total = total.scalar()
    return total, free_board_info

@rdb.dao()
async def get_free_board(db: AsyncSession, free_board_no: int) -> ReadBoard:
    result = await db.execute(select(FreeBoard).filter(FreeBoard.Board_no == free_board_no))
    free_board_info = result.scalars().first()
    return free_board_info

@rdb.dao(transactional=True)
async def create_free_board(free_board_info: CreateBoard, db: AsyncSession):
    create_values = free_board_info.dict()
    create_values['Create_date'] = datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
    await db.execute(insert(FreeBoard).values(create_values))

@rdb.dao(transactional=True)
async def update_free_board(free_board_no: int, free_board_info: UpdateBoard, db: AsyncSession) -> None:
    await db.execute(update(FreeBoard).filter(FreeBoard.Board_no == free_board_no).values(free_board_info.dict()))

@rdb.dao(transactional=True)
async def delete_free_board(free_board_no: int, db: AsyncSession) -> None:
    await free_board_comment_dao.all_delete_free_board_comment(free_board_no, db)
    await db.execute(delete(FreeBoard).filter(FreeBoard.Board_no == free_board_no))

@rdb.dao()
async def sort_free_board(db: AsyncSession, skip: int, sel: int) -> tuple[int, list[ReadBoardlist]]:
    if sel == 0:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Board_no.desc()).offset(skip*10).limit(10))
    elif sel == 1:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Board_no.asc()).offset(skip*10).limit(10))
    elif sel == 2:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Create_date.desc()).offset(skip*10).limit(10))
    elif sel == 3:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Create_date.asc()).offset(skip*10).limit(10))
    elif sel == 4:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Title.asc()).offset(skip*10).limit(10))
    elif sel == 5:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Title.desc()).offset(skip*10).limit(10))
    elif sel == 6:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Views.desc()).offset(skip*10).limit(10))
    elif sel == 7:
        result = await db.execute(select(FreeBoard).order_by(FreeBoard.Views.asc()).offset(skip*10).limit(10))
    free_board_info = result.scalars().all()
    total = await db.execute(select(func.count(FreeBoard.Board_no)))
    total = total.scalar()
    return total, free_board_info



