"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File
from src.core.type import ResultType
from src.core.status import Status, SU, ER
import logging
import os

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.var.session import get_db

# 호출할 모듈 추가
from src.api.v1.Study_Board_Comment.Study_Board_Comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.Study_Board_Comment import Study_Board_Comment_svc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/Study_Board_Comment", tags=["Study_Board_Comment"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read
@router.get(
    "/Get",
    summary="자유 게시판 게시물 댓글 조회",
    description="- 자유 게시판 게시물 댓글 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadCommentlist,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_Study_Board_Comment(Free_Board_no: int, page: int = 0, db: AsyncSession = Depends(get_db)):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------자유 게시판 게시물 댓글 전체 조회----------")
    total, Study_Board_Comment_info = await Study_Board_Comment_svc.get_Study_Board_Comment(db, Free_Board_no, skip=page)
    return {
        'total': total,
        'Board_info': Study_Board_Comment_info
    }


# Create
@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- Integer-Field / Integer-Field / String-Form / datetime-Field / Integer-Field",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_Study_Board_Comment(
    Free_Board_no: int,
    Content: str,
    File_name: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------자유 게시판 게시물 신규 댓글 생성----------")
    await Study_Board_Comment_svc.create_Study_Board_Comment(Free_Board_no, Content, File_name, db)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- no가 일치하는 데이터의 Content 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_Study_Board_Comment(
    Free_Board_no: int,
    Study_Board_Comment_no: int,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    Content: str,
    File_name: list[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------자유 게시판 게시물 기존 댓글 수정----------")
    await Study_Board_Comment_svc.update_Study_Board_Comment(Free_Board_no, Study_Board_Comment_no, Content, File_name, db)
    return SU.SUCCESS


# Delete
@router.delete(
    "/",
    summary="자유 게시판 게시물 댓글 삭제",
    description="- Study_Board_Comment_no가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_Study_Board_Comment(
    Free_Board_no: int,
    Study_Board_Comment_no: int, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
    db: AsyncSession = Depends(get_db)
):
    await Study_Board_Comment_svc.delete_Study_Board_Comment(Free_Board_no, Study_Board_Comment_no, db)
    return SU.SUCCESS
