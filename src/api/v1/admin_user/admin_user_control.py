'''
admin/user api : 관리자 페이지-사용자 관리 탭에서 사용되는 라우터
'''
from typing import Optional, List
from pydantic import EmailStr
from fastapi import APIRouter, Depends, Query
from src.core.status import Status, SU, ER
from src.api.v1.admin_user.admin_user_dto import (
    UserRole,
    UserGrade,
    ReadUserInfo,
    UpdateUserActivate,
    UpdateUserRole,
    UpdateUserGrade,
    # SearchUserDTO,
    # FilterUserDTO
)
from src.api.v1.admin_user import admin_user_service
from sqlalchemy.ext.asyncio import AsyncSession
from src.var.session import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin/user", tags=["admin_user"])


@router.get(
    "/",
    summary="승인된 모든 유저 목록 조회",
    description="- admin 페이지의 사용자 관리 탭 클릭 시 전체 유저를 목록 출력\n - 미승인 유저 조회 X",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR),
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await admin_user_service.get_all_users(db)


@router.get(
    "/search",
    summary="이름/닉네임/이메일이 일치하는 유저 목록 조회",
    description="- admin 페이지의 사용자 관리 탭에서 검색창을 통해 이름/닉네임/이메일 검색 시 일치하는 유저를 목록 출력",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR),
)
async def get_search_user(
    query: Optional[str] = Query(None, description="검색어 (이름, 닉네임, 이메일)"),
    db: AsyncSession = Depends(get_db)
):
    return await admin_user_service.search_users(query, db)


@router.get(
    "/filter",
    summary="등급/권한이 일치하는 유저 목록 조회",
    description="- admin 페이지의 사용자 관리 탭에서 등급/권한 선택 시 일치하는 유저를 목록 출력",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR)
)
async def get_filter_user(
    role: Optional[UserRole] = Query(None, description="유저 권한"),
    grade: Optional[UserGrade] = Query(None, description="유저 등급"),
    db: AsyncSession = Depends(get_db)
):
    return await admin_user_service.filter_users(role, grade, db)


@router.get(
    "/new",
    summary="회원가입 신청 완료, 미승인 유저 목록 조회",
    description="- admin 페이지의 사용자 관리 탭에서 회원가입 신청한(미승인된) 유저 목록 출력",
    response_model=List[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS)
)
async def get_new_users(db: AsyncSession = Depends(get_db)):
    return await admin_user_service.get_new_users(db)
    

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
    return await admin_user_service.update_user_activate(user_email, activate, db)


@router.put(
    "/role",
    summary="선택된 유저 권한 변경(관리자/사용자)",
    description="- admin 페이지의 사용자 관리 탭에서 기존 유저 관리자/일반유저 권한 변경",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR, ER.INTERNAL_ERROR)
)
async def update_user_role(
    user_email: List[EmailStr] = Query(..., description="유저 이메일 목록"),
    role: UserRole = Query(..., description="유저 권한"),
    db: AsyncSession = Depends(get_db)
):
    return await admin_user_service.update_user_role(user_email, role, db)



@router.put(
    "/grade",
    summary="선택된 유저 등급 변경",
    description="- admin 페이지의 사용자 관리 탭에서 기존 유저 등급 임의 변경",
    responses=Status.docs(SU.SUCCESS, ER.FIELD_VALIDATION_ERROR, ER.INTERNAL_ERROR)
)
async def update_user_grade(
    user_email: List[EmailStr] = Query(..., description="유저 이메일 목록"),
    grade: UserGrade = Query(..., description="유저 등급"),
    db: AsyncSession = Depends(get_db)
):
    return await admin_user_service.update_user_grade(user_email, grade, db)