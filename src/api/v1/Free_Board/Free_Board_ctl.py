"""
API 개발 시 참고 : 프론트엔드에서 http 엔드포인트를 통해 호출되는 메서드
"""
# 기본적으로 추가
from typing import Optional
from fastapi import APIRouter, Depends
from src.lib.status import Status, SU, ER
from src.lib.security import JWTBearer
import logging


# 호출할 모듈 추가
from src.api.v1.free_board.free_board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.api.v1.free_board import free_board_svc


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/free_board", tags=["free_board"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read List
@router.get(
    "/get list",
    summary="자유 게시판 게시물 전체 조회",
    description="- 자유 게시판 게시물 전체 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_free_board_list(page: int = 0):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------자유 게시판 전체 목록 조회----------")
    total, free_board_info = await free_board_svc.get_free_board_list(skip=page)
    return {
        'total': total,
        'Board_info': free_board_info
    }

# Read
@router.get(
    "/get",
    summary="자유 게시판 특정 게시물 조회",
    description="- 자유 게시판 특정 게시물 정보 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoard,
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_free_board(free_board_no: int = 0):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------자유 게시판 특정 게시물 조회----------")
    free_board_info = await free_board_svc.get_free_board(free_board_no)
    return free_board_info


# Create
@router.post(
    "/",
    summary="자유 게시판 신규 게시물 생성",
    description="- 입력 받은 데이터를 데이터베이스에 추가, String-Form / String-Form / Integer-Field",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_free_board(
    free_board_info: Optional[CreateBoard]
):
    logger.info("----------자유 게시판 신규 게시물 생성----------")
    await free_board_svc.create_free_board(free_board_info)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="자유 게시판 기존 게시물 수정",
    description="- 입력 받은 데이터로 변경 사항 수정, no가 일치하는 데이터의 Title, Content 수정",
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_free_board(
    free_board_no: int,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    free_board_info: Optional[UpdateBoard]
):
    logger.info("----------자유 게시판 기존 게시물 수정----------")
    await free_board_svc.update_free_board(free_board_no, free_board_info)
    return SU.SUCCESS


# Delete
@router.delete(
    "/",
    summary="자유 게시판 게시물 삭제",
    description="- Board_no가 일치하는 데이터 삭제",
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_free_board(
    free_board_no: int, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
):
    await free_board_svc.delete_free_board(free_board_no)
    return SU.SUCCESS


# sort Title
@router.get(
    "/sort title",
    summary="자유 게시판 게시물 제목 정렬",
    description="- 자유 게시판 게시물 제목을 가나다순으로 정렬하여 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=ReadBoardlist,
    dependencies=[Depends(JWTBearer())],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def sort_free_board(page: int = 0, select: int = 0):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------자유 게시판 제목 가나다순 정렬----------")
    total, free_board_info = await free_board_svc.sort_free_board(skip=page, select=select)
    return {
        'total': total,
        'Board_info': free_board_info
    }