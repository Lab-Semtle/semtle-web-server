"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from fastapi import UploadFile
from typing import Optional

# 호출할 모듈 추가
from src.api.v1_ewha.study_board.study_board_dto import ReadBoard, ReadBoardlist, CreateBoard, UpdateBoard
from src.api.v1_ewha.study_board import study_board_dao
from src.api.v1_ewha.study_board_comment import study_board_comment_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read List
async def get_study_board_list(db: AsyncSession, skip: int = 0) -> list[ReadBoardlist]:
    total, study_board_info = await study_board_dao.get_study_board_list(db, skip)
    study_board_info = [ReadBoard.from_orm(board).dict() for board in study_board_info]
    return total, study_board_info

# Read
async def get_study_board(db: AsyncSession, board_no: int) -> ReadBoard:
    study_board_info = await study_board_dao.get_study_board(db, board_no)
    return study_board_info

# Create
async def create_study_board(study_board_info: Optional[CreateBoard], db: AsyncSession) -> int:
    study_board_no = await study_board_dao.create_study_board(study_board_info, db)
    return study_board_no

# # Create
# async def upload_create_study_board(title: str, content: str, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
#     await study_board_dao.upload_create_study_board(title, content, file_name, db)

# Create
async def upload_file_study_board(study_board_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    await study_board_dao.upload_file_study_board(study_board_no, file_name, db)

# Update
async def update_study_board(study_board_no: int, study_board_info: Optional[UpdateBoard], db: AsyncSession, select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_board_dao.delete_image_study_board(study_board_no, db) # 기존에 저장된 이미지 삭제
    await study_board_dao.update_study_board(study_board_no, study_board_info, db)

# Update
async def upload_update_file_study_board(study_board_no: int, file_name: list[UploadFile], db: AsyncSession, select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_board_dao.delete_image_study_board(study_board_no, db) # 기존에 저장된 이미지 삭제
        await study_board_dao.upload_file_study_board(study_board_no, file_name, db)
    else:
        await study_board_dao.upload_file_add_study_board(study_board_no, file_name, db)
    
# Delete
async def delete_study_board(study_board_no: int, db: AsyncSession) -> None:
    await study_board_dao.delete_image_study_board(study_board_no, db)
    await study_board_comment_dao.all_delete_study_board_comment(study_board_no, db)
    await study_board_dao.delete_study_board(study_board_no, db)

# sort_Title
async def sort_study_board(db: AsyncSession, skip: int = 0, select: int = 0) -> list[ReadBoardlist]:
    total, study_board_info = await study_board_dao.sort_study_board(db, skip, select)
    study_board_info = [ReadBoard.from_orm(board).dict() for board in study_board_info] 
    return total, study_board_info