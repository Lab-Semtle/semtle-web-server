"""
족보 공유 게시판 API
"""
import os
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.lib.status import Status, SU, ER
from src.api.v1.board_exam.exam_dto import ReadBoard, ReadBoardlist, CreateBoard, UpdateBoard
from src.api.v1.board_exam import exam_svc
import logging
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/exam_sharing_board/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/exam_sharing_board/')

router = APIRouter(prefix="/exam_sharing_board", tags=["exam_sharing_board"])

@router.get(
    "/get list",
    summary="족보 게시판 게시물 전체 조회",
    description="- 족보 게시판 게시물 전체 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_exam_sharing_board_list(page: int = 0):
    logger.info("----------족보 게시판 전체 목록 조회----------")
    total, exam_sharing_board_info = await exam_svc.get_exam_sharing_board_list(skip=page)
    return {
        'total': total,
        'Board_info': exam_sharing_board_info
    }

@router.get(
    "/get",
    summary="족보 게시판 특정 게시물 조회",
    description="- 족보 게시판 특정 게시물 정보 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoard,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_exam_sharing_board(exam_sharing_board_no: int = 0):
    logger.info("----------족보 게시판 특정 게시물 조회----------")
    exam_sharing_board_info = await exam_svc.get_exam_sharing_board(exam_sharing_board_no)
    return exam_sharing_board_info

@router.get(
    "/images",
    summary="족보 게시판 특정 게시물 이미지 조회",
    description="- 족보 게시판 특정 게시물 이미지 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=list[str],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def get_exam_sharing_board(file_name: str = ""):
    logger.info("----------족보 게시판 특정 게시물 이미지 조회----------")
    return FileResponse(''.join([STATIC_DIR,file_name]))

@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- String-Form / String-Form / Integer-Form",
    # response_model=ResultType
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def create_exam_sharing_board(
    exam_sharing_board_info: Optional[CreateBoard],
):
    logger.info("----------족보 게시판 신규 게시물 생성----------")
    exam_sharing_board_no = await exam_svc.create_exam_sharing_board(exam_sharing_board_info)
    return { "status": SU.CREATED, "Exam_Sharing_Board_No": exam_sharing_board_no}

@router.put(
    "/create upload",
    summary="입력 받은 이미지를 데이터베이스에 추가",
    description="- List[UploadFile]",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def upload_file_exam_sharing_board(
    exam_sharing_board_no: int,
    file_name: list[UploadFile] = File(...),
):
    logger.info("----------족보 게시판 신규 게시물 이미지 생성----------")
    await exam_svc.upload_file_exam_sharing_board(exam_sharing_board_no, file_name)
    return SU.CREATED

@router.put(
    "/",
    summary="입력 받은 데이터로 기존 게시글 제목 및 내용 수정",
    description="- no가 일치하는 데이터의 title, content, view 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_exam_sharing_board(
    exam_sharing_board_no: int,
    exam_sharing_board_info: Optional[UpdateBoard],
    select: bool = False
):
    logger.info("----------족보 게시판 기존 게시물 수정----------")
    await exam_svc.update_exam_sharing_board(exam_sharing_board_no, exam_sharing_board_info, select=select)
    return SU.SUCCESS

@router.put(
    "/update upload",
    summary="입력 받은 파일로 파일 경로 수정",
    description="- no가 일치하는 데이터의 file_name 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def upload_update_file_exam_sharing_board(
    exam_sharing_board_no: int,
    file_name: list[UploadFile] = File(...),
    select: bool = False
):
    logger.info("----------족보 게시판 기존 게시물 파일 수정----------")
    await exam_svc.upload_update_file_exam_sharing_board(exam_sharing_board_no, file_name, select=select)
    return SU.SUCCESS

@router.delete(
    "/",
    summary="족보 게시판 게시물 삭제",
    description="- exam_sharing_board_no가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_exam_sharing_board(
    exam_sharing_board_no: int, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
):
    await exam_svc.delete_exam_sharing_board(exam_sharing_board_no)
    return SU.SUCCESS

@router.get(
    "/sort title",
    summary="족보 게시판 게시물 제목 정렬",
    description="- 족보 게시판 게시물 제목을 가나다순으로 정렬하여 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def sort_exam_sharing_board(page: int = 0, select: int = 0):
    logger.info("----------족보 게시판 제목 가나다순 정렬----------")
    total, exam_sharing_board_info = await exam_svc.sort_exam_sharing_board(skip=page, select=select)
    return {
        'total': total,
        'Board_info': exam_sharing_board_info
    }