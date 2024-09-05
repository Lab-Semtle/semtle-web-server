"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""

from fastapi import UploadFile, File
from typing import Optional

# 호출할 모듈 추가
from src.api.v1.comment_study.comm_study_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.comment_study import comm_study_dao



# Read
async def get_study_board_comment(study_board_no: int, skip: int) -> list[ReadCommentlist]:
    total, comment_info = await comm_study_dao.get_study_board_comment(study_board_no, skip)
    comment_info = [ReadComment.from_orm(Comment).dict() for Comment in comment_info]
    return total, comment_info


# Create
async def create_study_board_comment(study_board_no: int, study_board_comment_info: Optional[CreateComment]) -> int:
    study_board_comment_no = await comm_study_dao.create_study_board_comment(study_board_no, study_board_comment_info)
    return study_board_comment_no


# # Create
# async def upload_create_study_board_comment(study_board_no: int, content: str, file_name: list[UploadFile]) -> None:
#     await comm_study_dao.upload_create_study_board_comment(study_board_no, content, file_name)
    

# Create
async def upload_file_study_board_comment(study_board_comment_no: int, file_name: Optional[list[UploadFile]]) -> None:
    await comm_study_dao.upload_file_study_board_comment(study_board_comment_no, file_name)


# Update
async def update_study_board_comment(study_board_comment_no: int, study_board_comment_info: Optional[CreateComment], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await comm_study_dao.delete_image_study_board_comment(study_board_comment_no)
    await comm_study_dao.update_study_board_comment(study_board_comment_no, study_board_comment_info)


# Update
async def upload_update_file_study_board_comment(study_board_comment_no: int, file_name: list[UploadFile], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await comm_study_dao.delete_image_study_board_comment(study_board_comment_no) # 기존에 저장된 이미지 삭제
        await comm_study_dao.upload_file_study_board_comment(study_board_comment_no, file_name)
    else:
        await comm_study_dao.upload_file_add_study_board_comment(study_board_comment_no, file_name)


# # Update
# async def upload_update_study_board_comment(study_board_no: int ,study_board_comment_no: int, content: str, file_name: list[UploadFile]) -> None:
#     await comm_study_dao.delete_image_study_board_comment(study_board_no, study_board_comment_no)
#     await comm_study_dao.upload_update_study_board_comment(study_board_no, study_board_comment_no, content, file_name)
    

# Delete
async def delete_study_board_comment(study_board_comment_no: int) -> None:
    await comm_study_dao.delete_image_study_board_comment(study_board_comment_no)
    await comm_study_dao.delete_study_board_comment(study_board_comment_no)