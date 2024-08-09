"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from pydantic import parse_obj_as

# 호출할 모듈 추가
from src.api.v1.Free_Board.Free_Board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.api.v1.Free_Board import Free_Board_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read List
async def get_Free_Board_List(db: AsyncSession, skip: int = 0) -> list[ReadBoardlist]:
    total, Board_info = await Free_Board_dao.get_Free_Board_List(db, skip)
    Board_info = [ReadBoard.from_orm(board).dict() for board in Board_info]
    return total, Board_info

# Read
async def get_Free_Board(db: AsyncSession, Board_no: int) -> ReadBoard:
    Board_info = await Free_Board_dao.get_Free_Board(db, Board_no)
    return Board_info

# Create
async def create_Free_Board(Board: CreateBoard, db: AsyncSession) -> None:
    await Free_Board_dao.create_Free_Board(Board, db)
    
    
# Update
async def update_Free_Board(Board_no: int, Board_info: UpdateBoard, db: AsyncSession) -> None:
    await Free_Board_dao.update_Free_Board(Board_no, Board_info, db)
    

# Delete
async def delete_Free_Board(Board_no: int, db: AsyncSession) -> None:
    await Free_Board_dao.delete_Free_Board(Board_no, db)

# sort_Title
async def Sort_Free_Board(db: AsyncSession, skip: int = 0, select: int = 0) -> list[ReadBoardlist]:
    Total, Board_info = await Free_Board_dao.Sort_Free_Board(db, skip, select)
    Board_info = [ReadBoard.from_orm(board).dict() for board in Board_info] 
    return Total, Board_info