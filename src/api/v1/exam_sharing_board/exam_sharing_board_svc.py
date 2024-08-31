"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from fastapi import UploadFile
from typing import Optional

# 호출할 모듈 추가
from src.api.v1.exam_sharing_board.exam_sharing_board_dto import ReadBoard, ReadBoardlist, CreateBoard, UpdateBoard
from src.api.v1.exam_sharing_board import exam_sharing_board_dao
from src.api.v1.exam_sharing_board_comment import exam_sharing_board_comment_dao


# Read List
async def get_exam_sharing_board_list(skip: int) -> list[ReadBoardlist]:
    total, exam_sharing_board_info = await exam_sharing_board_dao.get_exam_sharing_board_list(skip)
    exam_sharing_board_info = [ReadBoard.from_orm(board).dict() for board in exam_sharing_board_info]
    return total, exam_sharing_board_info

# Read
async def get_exam_sharing_board(board_no: int) -> ReadBoard:
    exam_sharing_board_info = await exam_sharing_board_dao.get_exam_sharing_board(board_no)
    return exam_sharing_board_info

# Create
async def create_exam_sharing_board(exam_sharing_board_info: Optional[CreateBoard]) -> int:
    exam_sharing_board_no = await exam_sharing_board_dao.create_exam_sharing_board(exam_sharing_board_info)
    return exam_sharing_board_no

# # Create
# async def create_exam_sharing_board(title: str, content: str, file_name: Optional[list[UploadFile]]) -> None:
#     await exam_sharing_board_dao.create_exam_sharing_board(title, content, file_name)

# Create
async def upload_file_exam_sharing_board(exam_sharing_board_no: int, file_name: Optional[list[UploadFile]]) -> None:
    await exam_sharing_board_dao.upload_file_exam_sharing_board(exam_sharing_board_no, file_name)

# # Update
# async def update_exam_sharing_board(exam_sharing_board_no: int, title: str, content: str, file_name: list[UploadFile]) -> None:
#     await exam_sharing_board_dao.delete_image_exam_sharing_board(exam_sharing_board_no) # 기존에 저장된 파일 삭제
#     await exam_sharing_board_dao.upload_file_exam_sharing_board(exam_sharing_board_no, file_name)

# Update
async def update_exam_sharing_board(exam_sharing_board_no: int, exam_sharing_board_info: Optional[UpdateBoard], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await exam_sharing_board_dao.delete_file_exam_sharing_board(exam_sharing_board_no) # 기존에 저장된 이미지 삭제
    await exam_sharing_board_dao.update_exam_sharing_board(exam_sharing_board_no, exam_sharing_board_info)

# Update
async def upload_update_file_exam_sharing_board(exam_sharing_board_no: int, file_name: list[UploadFile], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await exam_sharing_board_dao.delete_file_exam_sharing_board(exam_sharing_board_no) # 기존에 저장된 이미지 삭제
        await exam_sharing_board_dao.upload_file_exam_sharing_board(exam_sharing_board_no, file_name)
    else:
        await exam_sharing_board_dao.upload_file_add_exam_sharing_board(exam_sharing_board_no, file_name)
    
# Delete
async def delete_exam_sharing_board(exam_sharing_board_no: int) -> None:
    await exam_sharing_board_dao.delete_file_exam_sharing_board(exam_sharing_board_no)
    await exam_sharing_board_comment_dao.all_delete_exam_sharing_board_comment(exam_sharing_board_no)
    await exam_sharing_board_dao.delete_exam_sharing_board(exam_sharing_board_no)

# sort_Title
async def sort_exam_sharing_board(skip: int, select: int) -> list[ReadBoardlist]:
    total, exam_sharing_board_info = await exam_sharing_board_dao.sort_exam_sharing_board(skip, select)
    exam_sharing_board_info = [ReadBoard.from_orm(board).dict() for board in exam_sharing_board_info] 
    return total, exam_sharing_board_info