# 기본적으로 추가
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response, Request
from core.type import ResultType
from core.status import Status, SU, ER
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import timedelta
import logging

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db

# 호출할 모듈 추가
from api.v1.login import login_service
from core import security
from api.v1.login.login_dto import CreateUserInfo
from dependencies.auth import authenticate


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["login"])

# 로그인 엔드포인트
@router.post(
    "/",
    summary="로그인",
    description="- 로그인 기능만 구현, JWT도 해야함",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def post_login(response: Response, login_form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    logger.info("----------로그인----------")
    # 사용자 인증 확인
    verify = await login_service.verify(login_form.username, login_form.password, db)
    if not verify:
        logger.warning("로그인 실패: 잘못된 사용자명 또는 비밀번호")
        return ER.UNAUTHORIZED
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"user": login_form.username}, expires_delta=access_token_expires)
    # 쿠키에 저장
    response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
    logger.info("로그인 성공")
    return SU.SUCCESS

# 회원가입 엔드포인트
@router.post(
    "/{signup}",
    summary="회원가입",
    description="- 회원가입 기능만 구현, JWT도 해야함, 생년월일 유효성 검사 코드 X",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
)
async def post_signup(login_info: Optional[CreateUserInfo], db: AsyncSession = Depends(get_db)):
    logger.info("----------회원가입----------")
    
    # 사용자 존재 여부 확인
    if login_info and await login_service.is_user(login_info.user_id, login_info.user_name, login_info.user_email, login_info.user_phone, db):
        logger.warning("이미 존재하는 유저.")
        return ER.DUPLICATE_RECORD

    # 회원가입 처리
    await login_service.post_signup(login_info, db)
    logger.info("회원가입 성공.")
    return SU.CREATED

@router.get(
    "/",
    summary="로그아웃",
    description="- 로그아웃",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def get_logout(response: Response, request: Request):
    # 쿠키 삭제
    response.delete_cookie(key="access_token")

    return SU.SUCCESS

@router.get(
    "/{token}",
    summary="token",
    description="- token",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    auth = authenticate(access_token)
    return {"auth": auth}
