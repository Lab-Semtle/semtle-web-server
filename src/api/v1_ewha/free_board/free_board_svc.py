"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""

# 호출할 모듈 추가
from src.api.v1_ewha.free_board.free_board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.api.v1_ewha.free_board import free_board_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read List
async def get_free_board_list(db: AsyncSession, skip: int) -> list[ReadBoardlist]:
    total, free_board_info = await free_board_dao.get_free_board_list(db, skip)
    free_board_info = [ReadBoard.from_orm(board).dict() for board in free_board_info]
    return total, free_board_info

# Read
async def get_free_board(db: AsyncSession, free_board_no: int) -> ReadBoard:
    free_board_info = await free_board_dao.get_free_board(db, free_board_no)
    return free_board_info

# Create
async def create_free_board(free_board_no: CreateBoard, db: AsyncSession) -> None:
    await free_board_dao.create_free_board(free_board_no, db)
    
    
# Update
async def update_free_board(free_board_no: int, free_board_info: UpdateBoard, db: AsyncSession) -> None:
    await free_board_dao.update_free_board(free_board_no, free_board_info, db)
    

# Delete
async def delete_free_board(free_board_no: int, db: AsyncSession) -> None:
    await free_board_dao.delete_free_board(free_board_no, db)

# sort_Title
async def sort_free_board(db: AsyncSession, skip: int, select: int) -> list[ReadBoardlist]:
    total, free_board_info = await free_board_dao.sort_free_board(db, skip, select)
    free_board_info = [ReadBoard.from_orm(board).dict() for board in free_board_info] 
    return total, free_board_info