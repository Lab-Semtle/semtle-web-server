"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""

# 호출할 모듈 추가
from src.api.v1.board_free.free_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.api.v1.board_free import free_dao


# Read List
async def get_free_board_list(skip: int) -> list[ReadBoardlist]:
    total, free_board_info = await free_dao.get_free_board_list(skip)
    free_board_info = [ReadBoard.from_orm(board).dict() for board in free_board_info]
    return total, free_board_info

# Read
async def get_free_board(free_board_no: int) -> ReadBoard:
    free_board_info = await free_dao.get_free_board(free_board_no)
    return free_board_info

# Create
async def create_free_board(free_board_no: CreateBoard) -> None:
    await free_dao.create_free_board(free_board_no)
    
    
# Update
async def update_free_board(free_board_no: int, free_board_info: UpdateBoard) -> None:
    await free_dao.update_free_board(free_board_no, free_board_info)
    

# Delete
async def delete_free_board(free_board_no: int) -> None:
    await free_dao.delete_free_board(free_board_no)

# sort_Title
async def sort_free_board(skip: int, select: int) -> list[ReadBoardlist]:
    total, free_board_info = await free_dao.sort_free_board(skip, select)
    free_board_info = [ReadBoard.from_orm(board).dict() for board in free_board_info] 
    return total, free_board_info