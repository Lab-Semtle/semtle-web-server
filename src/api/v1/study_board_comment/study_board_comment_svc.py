"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""

from fastapi import UploadFile, File
from typing import Optional

# 호출할 모듈 추가
from src.api.v1.study_board_comment.study_board_comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.study_board_comment import study_board_comment_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_study_board_comment(db: AsyncSession, study_board_no: int, skip: int = 0) -> list[ReadCommentlist]:
    total, comment_info = await study_board_comment_dao.get_study_board_comment(db, study_board_no, skip)
    comment_info = [ReadComment.from_orm(Comment).dict() for Comment in comment_info]
    return total, comment_info


# Create
async def create_study_board_comment(study_board_no: int, study_board_comment_info: Optional[CreateComment], db: AsyncSession) -> int:
    study_board_comment_no = await study_board_comment_dao.create_study_board_comment(study_board_no, study_board_comment_info, db)
    return study_board_comment_no


# # Create
# async def upload_create_study_board_comment(study_board_no: int, content: str, file_name: list[UploadFile], db: AsyncSession) -> None:
#     await study_board_comment_dao.upload_create_study_board_comment(study_board_no, content, file_name, db)
    

# Create
async def upload_file_study_board_comment(study_board_comment_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    await study_board_comment_dao.upload_file_study_board_comment(study_board_comment_no, file_name, db)


# Update
async def update_study_board_comment(study_board_comment_no: int, study_board_comment_info: Optional[CreateComment], db: AsyncSession, select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_board_comment_dao.delete_image_study_board_comment(study_board_comment_no, db)
    await study_board_comment_dao.update_study_board_comment(study_board_comment_no, study_board_comment_info, db)


# Update
async def upload_update_file_study_board_comment(study_board_comment_no: int, file_name: list[UploadFile], db: AsyncSession, select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_board_comment_dao.delete_image_study_board_comment(study_board_comment_no, db) # 기존에 저장된 이미지 삭제
        await study_board_comment_dao.upload_file_study_board_comment(study_board_comment_no, file_name, db)
    else:
        await study_board_comment_dao.upload_file_add_study_board_comment(study_board_comment_no, file_name, db)


# # Update
# async def upload_update_study_board_comment(study_board_no: int ,study_board_comment_no: int, content: str, file_name: list[UploadFile], db: AsyncSession) -> None:
#     await study_board_comment_dao.delete_image_study_board_comment(study_board_no, study_board_comment_no, db)
#     await study_board_comment_dao.upload_update_study_board_comment(study_board_no, study_board_comment_no, content, file_name, db)
    

# Delete
async def delete_study_board_comment(study_board_comment_no: int, db: AsyncSession) -> None:
    await study_board_comment_dao.delete_image_study_board_comment(study_board_comment_no, db)
    await study_board_comment_dao.delete_study_board_comment(study_board_comment_no, db)