'''
admin/user api : 관리자 페이지-사용자 관리 탭에서 사용되는 라우터
'''
from typing import Annotated, Optional, List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.status import Status, SU, ER
from src.api.v1.admin_user.admin_user_dto import (
    ReadUserInfo,
    ReadFilterUser,
    InfoUserRole,
    InfoUserGrade
)
from src.api.v1.admin_user import admin_user_service
from src.var.session import get_db
import logging

# OTP 검증 로직 임시
from src.api.v1.admin_user.otp_verification import send_otp, verify_otp
from src.api.v1.admin_user.dependencies import email_verification

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/user", tags=["admin_user"])


@router.get(
    "/send-otp",
    summary="OTP 발송",
    description="사용자의 이메일로 OTP를 발송합니다.",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR)
)
async def send_otp_route(email: str = Query(...)):
    send_otp(email)
    return {"detail": "OTP sent"}



@router.get(
    "/",
    summary="승인된 유저 중 특정 조건과 일치하는 유저 조회(전체 조회 포함)",
    description="- admin 페이지의 사용자 관리 탭 클릭 시 전체 유저를 목록 출력\n - 미승인 유저 조회 X\n - 검색(이름/닉네임/이메일) 및 필터 조건을 통해 유저를 목록 출력",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR),
)
async def get_filtered_users(
    query: Optional[str] = Query(None, description="검색어"),
    role: InfoUserRole = Query(None, description="유저 권한"),
    grade: InfoUserGrade = Query(None, description="유저 등급"),
    db: AsyncSession = Depends(get_db),
):
    filter = ReadFilterUser(role=role, grade=grade)
    return await admin_user_service.get_filtered_users(query, filter, db)


@router.get(
    "/join",
    summary="회원가입 신청 완료, 미승인 유저 목록 조회",
    description="- admin 페이지의 사용자 관리 탭에서 회원가입 신청한(미승인된) 유저 목록 출력",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS),
)
async def get_new_users(
    db: AsyncSession = Depends(get_db),
):
    return await admin_user_service.get_new_users(db)


# 미승인 유저 삭제 라우터 추가


@router.put(
    "/activate",
    summary="선택된 유저 계정 활성화/비활성화 처리",
    description="- admin 페이지의 사용자 관리 탭에서 신규 유저 가입 승인/기존 유저 계정 활성화/비활성화 처리",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR, ER.INTERNAL_ERROR)
)
async def update_user_activate(
    user_email: List[EmailStr] = Query(..., description="유저 이메일 목록"),
    activate: bool = Query(..., description="활성화 여부"),
    db: AsyncSession = Depends(get_db)
):
    await admin_user_service.update_user_activate(user_email, activate, db)
    return SU.SUCCESS


@router.put(
    "/role",
    summary="선택된 유저 권한 변경(관리자/사용자)",
    description="- admin 페이지의 사용자 관리 탭에서 기존 유저 관리자/일반유저 권한 변경",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR, ER.INTERNAL_ERROR)
)
async def update_user_role(
    user_email: List[EmailStr] = Query(..., description="유저 이메일 목록"),
    role: InfoUserRole = Query(..., description="유저 권한"),
    db: AsyncSession = Depends(get_db)
):
    await admin_user_service.update_user_role(user_email, role, db)
    return SU.SUCCESS


@router.put(
    "/grade",
    summary="선택된 유저 등급 변경",
    description="- admin 페이지의 사용자 관리 탭에서 기존 유저 등급 임의 변경",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR, ER.INTERNAL_ERROR)
)
async def update_user_grade(
    user_email: List[EmailStr] = Query(..., description="유저 이메일 목록"),
    grade: InfoUserGrade = Query(..., description="유저 등급"),
    db: AsyncSession = Depends(get_db)
):
    await admin_user_service.update_user_grade(user_email, grade, db)
    return SU.SUCCESS