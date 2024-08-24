from typing import Optional
from fastapi import APIRouter, Depends, Query
from core.type import ResultType
from core.status import Status, SU, ER
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db
from api.v1.find.find_service import find_password, find_email_
from api.v1.find.find_dto import FindPWRequest, FindPWResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/find", tags=["find"])

@router.get(
    "/find-password",
    summary="비밀번호 찾기",
    description="이메일과 전화번호를 통해 비밀번호를 찾습니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST, ER.NOT_FOUND)
)
async def find_pw(
    email: str = Query(..., description="이메일"),
    phone: str = Query(..., description="전화번호"),
    db: AsyncSession = Depends(get_db)
):
    # 서비스 계층을 통해 비밀번호 찾기
    password = await find_password(email, phone, db)
    
    if not password:
        # 비밀번호를 찾지 못한 경우 NOT_FOUND 상태 반환
        return ER.NOT_FOUND
    
    # 비밀번호가 발견되면 반환
    return {"password": password}

@router.get(
    "/find-email",
    summary="이메일 찾기",
    description="전화번호를 통해 비밀번호를 찾습니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST, ER.NOT_FOUND)
)
async def find_email(
    phone: str = Query(..., description="전화번호"),
    db: AsyncSession = Depends(get_db)
):
    # 서비스 계층을 통해 비밀번호 찾기
    email = await find_email_(phone, db)
    
    if not email:
        # 비밀번호를 찾지 못한 경우 NOT_FOUND 상태 반환
        return ER.NOT_FOUND
    
    # 비밀번호가 발견되면 반환
    return {"email": email}
