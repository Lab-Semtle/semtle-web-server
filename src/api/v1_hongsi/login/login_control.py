from typing import Optional
from fastapi import APIRouter, Depends, Response, Request, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from decouple import config
import logging

from core.status import Status, SU, ER
from var.session import get_db
from api.v1_hongsi.login import login_service
from core.security import JWTBearer, create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from api.v1_hongsi.login.login_dto import CreateUserInfo

# 환경 변수에서 토큰 만료 시간 설정
ACCESS_TOKEN_EXPIRE_MINUTES = float(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = float(config("REFRESH_TOKEN_EXPIRE_MINUTES"))

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 로그인 엔드포인트
@router.post(
    "/login",
    summary="로그인",
    description="사용자 인증 후 JWT 토큰을 발급합니다.",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def post_login(
    response: Response,
    login_form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------로그인----------")
    # 사용자 인증 확인
    verify = await login_service.verify(login_form.username, login_form.password, db)
    if not verify:
        logger.warning("로그인 실패: 잘못된 사용자명 또는 비밀번호")
        return ER.UNAUTHORIZED
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": login_form.username}, expires_delta=access_token_expires)
    refresh_token = await create_refresh_token(data={"sub": login_form.username}, expires_delta=refresh_token_expires)
    
    # 쿠키에 저장
    response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, expires=refresh_token_expires, httponly=True)
    logger.info("로그인 성공")
    return SU.SUCCESS

# 회원가입 엔드포인트
@router.post(
    "/signup",
    summary="회원가입",
    description="새 사용자 계정을 생성합니다.",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
)
async def post_signup(
    login_info: Optional[CreateUserInfo],
    code: str,
    db: AsyncSession = Depends(get_db)
):
    logger.info("----------회원가입----------")
    
    # 사용자 존재 여부 확인
    if login_info and await login_service.is_user(login_info.user_id, login_info.user_name, login_info.user_email, code, db):
        logger.warning("이미 존재하는 유저.")
        return ER.DUPLICATE_RECORD
    if not await login_service.verify_email(code):
        logger.warning("이메일 인증 실패")
        return ER.INVALID_REQUEST

    # 회원가입 처리
    await login_service.post_signup(login_info, db)
    logger.info("회원가입 성공.")
    return SU.CREATED

# 로그아웃 엔드포인트
@router.get(
    "/logout",
    summary="로그아웃",
    description="사용자의 인증 쿠키를 삭제하여 로그아웃합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    dependencies=[Depends(JWTBearer())]
)
async def get_logout(response: Response):
    # 쿠키 삭제
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return SU.SUCCESS

# 리프레시 토큰을 이용해 새로운 접근 토큰을 발급하는 엔드포인트
@router.get(
    "/refresh",
    summary="Access 토큰 재발급",
    description="Refresh 토큰을 사용하여 새로운 Access 토큰을 발급합니다.",
    responses=Status.docs(SU.CREATED, ER.INVALID_REQUEST),
)
async def refresh_token(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="리프레시 토큰이 없습니다")
        
        # 리프레시 토큰 검증
        refresh_data = verify_refresh_token(refresh_token)
        user_data = {"sub": refresh_data.get("sub")}
        
        # 새로운 접근 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = await create_access_token(data=user_data, expires_delta=access_token_expires)
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, expires=access_token_expires)
        return SU.CREATED
    except Exception as e:
        logger.error(f"토큰 재발급 중 오류 발생: {e}")
        return ER.INVALID_REQUEST

# 토큰 검증 엔드포인트
@router.get(
    "/token",
    summary="토큰 상태 확인",
    description="Access 및 Refresh 토큰의 상태를 확인합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    ac = verify_access_token(access_token)
    rf = verify_refresh_token(refresh_token)
    return {"access_token": ac, "refresh_token": rf}

# 이메일 전송 엔드포인트
@router.get(
    "/send",
    summary="이메일 전송",
    description="사용자에게 인증 이메일을 전송합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def verify_email(user_email: str = Query(..., description="사용자 이메일")):
    await login_service.send_confirmation_email(user_email)
    return SU.SUCCESS

# 코드 확인 엔드포인트
@router.get(
    "/code",
    summary="코드 확인",
    description="이메일 인증 코드를 확인합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def code():
    res = await login_service.code()
    return res
