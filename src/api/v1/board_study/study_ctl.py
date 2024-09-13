"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.lib.status import Status, SU, ER
import logging
import os
from src.api.v1.board_study.study_dto import ReadBoard, ReadBoardlist, CreateBoard, UpdateBoard
from src.api.v1.board_study import study_svc
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/study_board/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/study_board/')

router = APIRouter(prefix="/study_board", tags=["study_board"])

@router.get(
    "/get_list",
    summary="스터디 게시판 게시물 전체 조회",
    description="- 스터디 게시판 게시물 전체 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_study_board_list(page: int = 0):
    logger.info("----------스터디 게시판 전체 목록 조회----------")
    total, study_board_info = await study_svc.get_study_board_list(skip=page)
    return {
        'total': total,
        'Board_info': study_board_info
    }

@router.get(
    "/get",
    summary="스터디 게시판 특정 게시물 조회",
    description="- 스터디 게시판 특정 게시물 정보 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoard,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_study_board(study_board_no: int = 0):
    logger.info("----------스터디 게시판 특정 게시물 조회----------")
    study_board_info = await study_svc.get_study_board(study_board_no)
    return study_board_info

@router.get(
    "/images",
    summary="스터디 게시판 특정 게시물 이미지 조회",
    description="- 스터디 게시판 특정 게시물 이미지 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=list[str],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_Images_study_board(file_name: str = ""):
    logger.info("----------스터디 게시판 특정 게시물 이미지 조회----------")
    return FileResponse(''.join([STATIC_DIR,file_name]))

@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- String-Form / String-Form / Integer-Field",
    # response_model=ResultType, 
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def create_study_board(
    study_board_info: Optional[CreateBoard],
):
    logger.info("----------스터디 게시판 신규 게시물 생성----------")
    study_board_no = await study_svc.create_study_board(study_board_info)
    return { "status": SU.CREATED, "Study_Board_No": study_board_no}

@router.put(
    "/create_upload",
    summary="입력 받은 이미지을 데이터베이스에 추가",
    description="- List[UploadFile]",
    # response_model=ResultType,
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def upload_file_study_board(
    study_board_no: int,
    file_name: list[UploadFile] = File(...),
):
    logger.info("----------스터디 게시판 신규 게시물 이미지 생성----------")
    await study_svc.upload_file_study_board(study_board_no, file_name)
    return SU.CREATED

@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- no가 일치하는 데이터의 title, content, view 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_study_board(
    study_board_no: int,
    study_board_info: Optional[UpdateBoard],
    select: bool = False
):
    logger.info("----------스터디 게시판 기존 게시물 수정----------")
    await study_svc.update_study_board(study_board_no, study_board_info, select=select)
    return SU.SUCCESS

@router.put(
    "/update_upload",
    summary="입력 받은 이미지로 이미지 경로 수정",
    description="- List[UploadFile]",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def upload_update_file_study_board(
    study_board_no: int,
    file_name: list[UploadFile] = File(...),
        select: bool = False
):
    logger.info("----------스터디 게시판 기존 게시물 이미지 수정----------")
    await study_svc.upload_update_file_study_board(study_board_no, file_name, select=select)
    return SU.SUCCESS

@router.delete(
    "/",
    summary="스터디 게시판 게시물 삭제",
    description="- study_board_no가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_study_board(
    study_board_no: int, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
):
    await study_svc.delete_study_board(study_board_no)
    return SU.SUCCESS

@router.get(
    "/sort_title",
    summary="스터디 게시판 게시물 제목 정렬",
    description="- 스터디 게시판 게시물 제목을 가나다순으로 정렬하여 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def sort_study_board(page: int = 0, select: int = 0):
    logger.info("----------스터디 게시판 제목 가나다순 정렬----------")
    total, study_board_info = await study_svc.sort_study_board(skip=page, select=select)
    return {
        'total': total,
        'Board_info': study_board_info
    }