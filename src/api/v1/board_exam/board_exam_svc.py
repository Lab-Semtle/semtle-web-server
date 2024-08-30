"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from fastapi import UploadFile
from typing import Optional

# 호출할 모듈 추가
from src.api.v1.exam_sharing_board.exam_sharing_board_dto import ReadBoard, ReadBoardlist
from src.api.v1.exam_sharing_board import exam_sharing_board_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read List
async def get_exam_sharing_board_list(db: AsyncSession, skip: int = 0) -> list[ReadBoardlist]:
    total, exam_sharing_board_info = await exam_sharing_board_dao.get_exam_sharing_board_list(db, skip)
    exam_sharing_board_info = [ReadBoard.from_orm(board).dict() for board in exam_sharing_board_info]
    return total, exam_sharing_board_info

# Read
async def get_exam_sharing_board(db: AsyncSession, board_no: int) -> ReadBoard:
    exam_sharing_board_info = await exam_sharing_board_dao.get_exam_sharing_board(db, board_no)
    return exam_sharing_board_info

# Create
async def create_exam_sharing_board(title: str, content: str, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    await exam_sharing_board_dao.create_exam_sharing_board(title, content, file_name, db)
   
# Update
async def update_exam_sharing_board(exam_sharing_board_no: int, title: str, content: str, file_name: list[UploadFile], db: AsyncSession) -> None:
    await exam_sharing_board_dao.delete_image_exam_sharing_board(exam_sharing_board_no, db) # 기존에 저장된 파일 삭제
    await exam_sharing_board_dao.update_exam_sharing_board(exam_sharing_board_no, title, content, file_name, db)
    
# Delete
async def delete_exam_sharing_board(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await exam_sharing_board_dao.delete_exam_sharing_board(exam_sharing_board_no, db)

# sort_Title
async def sort_exam_sharing_board(db: AsyncSession, skip: int = 0, select: int = 0) -> list[ReadBoardlist]:
    total, exam_sharing_board_info = await exam_sharing_board_dao.sort_exam_sharing_board(db, skip, select)
    exam_sharing_board_info = [ReadBoard.from_orm(board).dict() for board in exam_sharing_board_info] 
    return total, exam_sharing_board_info