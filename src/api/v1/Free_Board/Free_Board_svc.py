"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.Free_Board.Free_Board_dto import UpdateBoard, ReadBoard, CreateBoard
from src.api.v1.Free_Board import Free_Board_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_Free_Board(db: AsyncSession) -> list[ReadBoard]:
    Board_info = await Free_Board_dao.get_Free_Board(db)
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