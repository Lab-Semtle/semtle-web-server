# 기본적으로 추가
"""
계정 관련 API
- 회원가입
- 로그인
- 로그아웃
- 토큰 발급
- 토큰 재발급
"""
'''
API 수정 시 참고
- 명확하게 하기 위해, import 경로 src 부터 작성하기
- Contrl에서 DB 세션 관련 파라미터 삭제
- API 반환 형식 ResultType으로 감싸기
- 더 이상 디버깅 할 필요 없는 API의 로깅 제거 (서비스 도중 꼭 필요하다면 유지)
'''
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response, Request
from datetime import timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.lib.type import ResultType # 경로
from src.lib.status import Status, SU, ER
from src.lib import security
from src.lib.security import JWTBearer
from src.core import settings
from src.api.v1_master.auth import auth_svc
from src.api.v1_master.auth.auth_dto import CreateUserInfo
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["login"])

ACCESS_TOKEN_EXPIRE_MINUTES = float(settings.jwt.JWT_ACCESS_TOKEN_EXPIRE_MIN)
REFRESH_TOKEN_EXPIRE_MINUTES = float(settings.jwt.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)


# 회원가입 엔드포인트
@router.post(
    "/{signup}",
    summary     = "회원가입",
    description = "- 회원가입 기능만 구현, JWT도 해야함, 생년월일 유효성 검사 코드 X",
    responses   = Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
)
async def signup(user_info: Optional[CreateUserInfo]): # 1. DB 세션 관련 파라미터 삭제
    # 사용자 존재 여부 확인
    if user_info and await auth_svc.is_user( 
        user_info.user_id, 
        user_info.user_name, 
        user_info.user_email, 
        user_info.user_phone
    ):
        logger.warning("이미 존재하는 유저.")
        return ResultType(status='error', message=ER.DUPLICATE_RECORD[1]) # 2. API 봔환 형식 ResultType로 감싸기

    # 회원가입 처리
    await auth_svc.post_signup(user_info) # 3. 다른 메서드 호출 시에도 DB 세션 파라미터 삭제
    logger.info("회원가입 성공.")
    return ResultType(status='success', message=SU.CREATED[1])


# 로그인 엔드포인트
@router.post(
    "/",
    summary="로그인",
    description="- 로그인 기능만 구현, JWT도 해야함",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def login(response: Response, login_form: OAuth2PasswordRequestForm = Depends()):
    # 사용자 인증 확인
    verify = await auth_svc.verify(login_form.username, login_form.password)
    if not verify:
        logger.warning("로그인 실패: 잘못된 사용자명 또는 비밀번호")
        return ResultType(status='error', message=ER.UNAUTHORIZED[1])
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token =await security.create_access_token(data={"sub": login_form.username}, expires_delta=access_token_expires)
    refresh_token =await security.create_refresh_token(data={"sub": login_form.username}, expires_delta=refresh_token_expires)
    
    # 쿠키에 저장
    response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, expires=refresh_token_expires, httponly=True)
    logger.info("로그인 성공")
    return ResultType(status='success', message=SU.SUCCESS[1])


@router.get(
    "/",
    summary="로그아웃",
    description="- 로그아웃",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    dependencies=[Depends(JWTBearer())]
)
async def logout(response: Response, request: Request):
    # 쿠키 삭제
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return ResultType(status='success', message=SU.SUCCESS[1])


@router.get(
    "/refresh",
    summary="토큰 재발급",
    description="- refresh 토큰을 이용해 access 토큰 재발급",
    responses=Status.docs(SU.CREATED, ER.INVALID_REQUEST),
)
async def get_refresh_token(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return ResultType(status='error', message=ER.INVALID_TOKEN[1])
    
        # 리프레시 토큰 검증
        refresh_data =  security.verify_refresh_token(refresh_token)
        # 리프레시 토큰에서 사용자 정보 추출
        user_data = {"sub": refresh_data.get("sub")}
        # 새로운 접근 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = await security.create_access_token(data=user_data, expires_delta=access_token_expires)
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, expires=access_token_expires)
        return ResultType(status='success', message=SU.CREATED[1])
    except:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])
    
    
@router.get(
    "/token",
    summary="토큰 발급",
    description="- 새로운 access 토큰 발급",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    ac = security.verify_access_token(access_token)
    rf = security.verify_refresh_token(refresh_token)
    return ResultType(status='success', message=SU.SUCCESS[1], detail={"access_token": ac, "refresh_token": rf})