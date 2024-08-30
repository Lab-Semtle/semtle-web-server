"""
개인 정보 찾기 API
"""
from fastapi import APIRouter, Depends, Query
from src.lib.type import ResultType
from src.lib.status import Status, SU, ER
from src.api.v1.find.find_svc import find_password, find_email_


router = APIRouter(prefix="/find", tags=["find"])

@router.get(
    "/find-password",
    summary="비밀번호 찾기",
    description="이메일과 전화번호를 통해 비밀번호를 찾습니다.",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def find_pw(
    email: str = Query(..., description="이메일"),
    phone: str = Query(..., description="전화번호")
):
    """
    이메일과 전화번호를 통해 비밀번호를 찾는 API 엔드포인트
    """
    password = await find_password(email, phone)  # 서비스 계층에서 비밀번호 찾기 호출
    
    if not password:
        return ResultType(status='error', message=ER.NOT_FOUND[1])
    
    # 비밀번호가 발견되면 반환
    return {"password": password}

@router.get(
    "/find-email",
    summary="이메일 찾기",
    description="전화번호를 통해 이메일을 찾습니다.",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND)
)
async def find_email(
    phone: str = Query(..., description="전화번호")
):
    """
    전화번호를 통해 이메일을 찾는 API 엔드포인트
    """
    email = await find_email_(phone)  # 서비스 계층에서 이메일 찾기 호출
    
    if not email:
        # 이메일을 찾지 못한 경우 NOT_FOUND 상태 반환
        return ResultType(status='error', message=ER.NOT_FOUND[1])
    
    # 이메일이 발견되면 반환
    return {"email": email}
