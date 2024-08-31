"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.lib.status import Status, SU, ER
import logging
import os


# 호출할 모듈 추가
from src.api.v1.study_board_comment.study_board_comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.study_board_comment import study_board_comment_svc

BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/study_board_comment/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/study_board_comment/')


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/study_board_comment", tags=["study_board_comment"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read
@router.get(
    "/get",
    summary="스터디 게시판 게시물 댓글 조회",
    description="- 스터디 게시판 게시물 댓글 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadCommentlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_study_board_comment(study_board_no: int, page: int = 0):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------스터디 게시판 게시물 댓글 전체 조회----------")
    total, study_board_comment_info = await study_board_comment_svc.get_study_board_comment(study_board_no, skip=page)
    return {
        'total': total,
        'Board_info': study_board_comment_info
    }


# Image 
@router.get(
    "/images",
    summary="스터디 게시판 특정 게시물 댓글 이미지 조회",
    description="- 스터디 게시판 특정 게시물 댓글 이미지 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=list[str],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_Images_study_board_commet(file_name: str = ""):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------스터디 게시판 특정 게시물 댓글 이미지 조회----------")
    return FileResponse(''.join([STATIC_DIR,file_name]))


# Create
@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- String-Form / String-Form / Integer-Field",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def create_study_board_comment(
    study_board_no: int,
    study_board_comment_info: Optional[CreateComment]
):
    logger.info("----------스터디 게시판 신규 게시물 생성----------")
    study_board_comment_no = await study_board_comment_svc.create_study_board_comment(study_board_no, study_board_comment_info)
    return { "status": SU.CREATED, "Study_Board_Comment_No": study_board_comment_no}


# # Create
# @router.post(
#     "/upload",
#     summary="입력 받은 데이터를 데이터베이스에 추가(업로드한 파일 포함)",
#     description="- Integer-Field / String-Form / list[UploadFile]",
#     # response_model=ResultType, # -> 코드 미완성, 주석처리
#     responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
# )
# async def upload_create_study_board_comment(
#     study_board_no: int,
#     content: str,
#     file_name: list[UploadFile] = File(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     logger.info("----------스터디 게시판 게시물 신규 댓글(파일 포함) 생성----------")
#     await study_board_comment_svc.upload_create_study_board_comment(study_board_no, content, file_name)
#     return SU.CREATED


# Create
@router.put(
    "/create upload",
    summary="입력 받은 이미지를 데이터베이스에 추가",
    description="- List[UploadFile]",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD, ER.FIELD_VALIDATION_ERROR)
)
async def upload_file_study_board_comment(
    study_board_comment_no: int,
    file_name: list[UploadFile] = File(...)
):
    logger.info("----------스터디 게시판 신규 게시물 이미지 생성----------")
    await study_board_comment_svc.upload_file_study_board_comment(study_board_comment_no, file_name)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- no가 일치하는 데이터의 title, content, view 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_study_board_comment(
    study_board_comment_no: int,
    study_board_comment_info: Optional[CreateComment],
    select: bool = False
):
    logger.info("----------스터디 게시판 기존 게시물 수정----------")
    await study_board_comment_svc.update_study_board_comment(study_board_comment_no, study_board_comment_info, select=select)
    return SU.SUCCESS


# # Update
# @router.put(
#     "/upload",
#     summary="입력 받은 데이터로 변경 사항 수정(업로드한 파일 포함)",
#     description="- no가 일치하는 데이터의 content 수정",
#     responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
# )
# async def upload_update_study_board_comment(
#     study_board_no: int,
#     study_board_comment_no: int,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
#     content: str,
#     file_name: list[UploadFile] = File(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     logger.info("----------스터디 게시판 게시물 기존 댓글(파일 포함) 수정----------")
#     await study_board_comment_svc.upload_update_study_board_comment(study_board_no, study_board_comment_no, content, file_name)
#     return SU.SUCCESS


# Update
@router.put(
    "/update upload",
    summary="입력 받은 이미지로 이미지 경로 수정",
    description="- List[UploadFile]",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def upload_update_file_study_board_comment(
    study_board_comment_no: int,
    file_name: list[UploadFile] = File(...),
    select: bool = False
):
    logger.info("----------스터디 게시판 기존 게시물 이미지 수정----------")
    await study_board_comment_svc.upload_update_file_study_board_comment(study_board_comment_no, file_name, select=select)
    return SU.SUCCESS


# Delete
@router.delete(
    "/",
    summary="스터디 게시판 게시물 댓글 삭제",
    description="- study_board_comment_no가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_study_board_comment(
    study_board_comment_no: int # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
):
    await study_board_comment_svc.delete_study_board_comment(study_board_comment_no)
    return SU.SUCCESS
