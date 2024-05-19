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
from src.api.v1.example.example_dto import ReadExampleInfo, CreateExample, UpdateExample, keyExample
from src.api.v1.example import example_service


# 로깅 및 라우터 객체 생성 - 기본적으로 추가
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/example", tags=["example"])

# 라우터 추가 시 현재는 src.api.v1.__init__.py에 생성하려는 라우터 추가해줘야 함.(수정 예정)


# Read
@router.get(
    "/",
    summary="전체 예제 조회",
    description="- 전체 예제 리스트 반환, 등록된 예제가 없는 경우 `[]` 반환",
    response_model=list[ReadExampleInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
# 함수명 get, post, update, delete 중 1택 + 목적에 맞게 이름 작성
async def get_examples(db: AsyncSession = Depends(get_db)):
    # 개발 중 logging 사용하고 싶을 때 이 코드 추가
    logger.info("----------전체 예제 목록 조회----------")
    examples_info = await example_service.get_examples(db)
    return examples_info


# Create
@router.post(
    "/",
    summary="입력 받은 데이터를 데이터베이스에 추가",
    description="- String-Form / Text-Form / Text-Form / Text-Field",
    # response_model=ResultType, # -> 코드 미완성, 주석처리
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def create_example(
    example: Optional[CreateExample],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------신규 예제 생성----------")
    await example_service.create_example(example, db)
    return SU.CREATED


# Update
@router.put(
    "/",
    summary="입력 받은 데이터로 변경 사항 수정",
    description="- id가 일치하는 데이터의 name, comm1, comm2 수정",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD)
)
async def update_example(
    example_id: str,  # JWT 토큰에서 id 가져오는 방식으로 변경, 이건 임시조치
    example_info: Optional[UpdateExample],
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------기존 예제 수정----------")
    await example_service.update_example(example_id, example_info, db)
    return SU.SUCCESS


# Delete
@router.delete(
    "/",
    summary="예제 삭제",
    description="- id가 일치하는 데이터 삭제",
    responses=Status.docs(SU.SUCCESS, ER.DUPLICATE_RECORD),
)
async def delete_example(
    example_id: str, # JWT 토큰에서 id 가져오는 방식으로 변경, 임시조치
    db: AsyncSession = Depends(get_db)
):
    await example_service.delete_example(example_id, db)
    return SU.SUCCESS