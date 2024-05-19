"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from src.core.type import ResultType
from src.core.status import Status, SU, ER
import logging

# (db 세션 관련)이후 삭제 예정, 개발을 위해 일단 임시로 추가
from sqlalchemy.ext.asyncio import AsyncSession
from src.var.session import get_db

# 호출할 모듈 추가
from src.api.v1.Free_Board.Free_Board_dto import UpdateBoard, ReadBoard, CreateBoard
from src.api.v1.Free_Board import Free_Board_svc


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/Free_Board", tags=["Free_Board"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read
@router.get(
    "/Get",
    summary="자유 게시판 게시물 전체 조회",
    description="- 자유 게시판 게시물 전체 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoard,
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_Free_Board(db: AsyncSession = Depends(get_db), page: int = 0, size: int = 10):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------자유 게시판 전체 목록 조회----------")
    Total, Board_info = await Free_Board_svc.get_Free_Board(db, skip=page*size, limit=size)
    return {
        'Total': Total,
        'Board_info': Board_info
    }


# Create
@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- Integer-Field / String-Form / String-Form / datetime-Field / Integer-Field",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_Free_Board(
    Free_Board: Optional[CreateBoard],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------자유 게시판 신규 게시물 생성----------")
    await Free_Board_svc.create_Free_Board(Free_Board, db)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- no가 일치하는 데이터의 Title, Content 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_Free_Board(
    Free_Board_no: int,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    Free_Board_info: Optional[UpdateBoard],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------자유 게시판 기존 게시물 수정----------")
    await Free_Board_svc.update_Free_Board(Free_Board_no, Free_Board_info, db)
    return SU.SUCCESS


# Delete
@router.delete(
    "/",
    summary="자유 게시판 게시물 삭제",
    description="- Board_no가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_Free_Board(
    Free_Board_no: int, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
    db: AsyncSession = Depends(get_db)
):
    await Free_Board_svc.delete_Free_Board(Free_Board_no, db)
    return SU.SUCCESS