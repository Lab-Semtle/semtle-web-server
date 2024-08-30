"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from fastapi import UploadFile
from typing import Optional
from src.api.v1.board_study.study_dto import ReadBoard, ReadBoardlist, CreateBoard, UpdateBoard
from src.api.v1.board_study import study_dao
from src.api.v1.comment_study import comm_study_dao


async def get_study_board_list(skip: int = 0) -> list[ReadBoardlist]:
    total, study_board_info = await study_dao.get_study_board_list(skip)
    study_board_info = [ReadBoard.from_orm(board).dict() for board in study_board_info]
    return total, study_board_info

async def get_study_board(board_no: int) -> ReadBoard:
    study_board_info = await study_dao.get_study_board(board_no)
    return study_board_info

async def create_study_board(study_board_info: Optional[CreateBoard]) -> int:
    study_board_no = await study_dao.create_study_board(study_board_info)
    return study_board_no

async def upload_file_study_board(study_board_no: int, file_name: Optional[list[UploadFile]]) -> None:
    await study_dao.upload_file_study_board(study_board_no, file_name)

async def update_study_board(study_board_no: int, study_board_info: Optional[UpdateBoard], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_dao.delete_image_study_board(study_board_no) # 기존에 저장된 이미지 삭제
    await study_dao.update_study_board(study_board_no, study_board_info)

async def upload_update_file_study_board(study_board_no: int, file_name: list[UploadFile], select: bool) -> None:
    if not select: # defalt: 기존 이미지 삭제
        await study_dao.delete_image_study_board(study_board_no) # 기존에 저장된 이미지 삭제
        await study_dao.upload_file_study_board(study_board_no, file_name)
    else:
        await study_dao.upload_file_add_study_board(study_board_no, file_name)
    
async def delete_study_board(study_board_no: int, ) -> None:
    await study_dao.delete_image_study_board(study_board_no)
    await comm_study_dao.all_delete_study_board_comment(study_board_no)
    await study_dao.delete_study_board(study_board_no)

async def sort_study_board(skip: int = 0, select: int = 0) -> list[ReadBoardlist]:
    total, study_board_info = await study_dao.sort_study_board(skip, select)
    study_board_info = [ReadBoard.from_orm(board).dict() for board in study_board_info] 
    return total, study_board_info