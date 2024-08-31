"""
계정 권한 API
"""
from typing import Optional
from fastapi import APIRouter, Depends, Response, Request, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
# from decouple import config
from src.lib.type import ResultType
from src.lib.status import Status, SU, ER
from src.api.v1.auth import auth_svc
from src.lib.security import JWTBearer, create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from src.api.v1.auth.auth_dto import CreateUserInfo
from src.core import settings


# 환경 변수에서 토큰 만료 시간 설정
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt.JWT_ACCESS_TOKEN_EXPIRE_MIN
REFRESH_TOKEN_EXPIRE_MINUTES = settings.jwt.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/login", tags=["login"])

'''
로그인 엔드포인트
'''
@router.post(
    "/login",
    summary="로그인",
    description="사용자 인증 후 JWT 토큰을 발급합니다.",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def post_login(
    response: Response,
    login_form: OAuth2PasswordRequestForm = Depends()
):
    # 사용자 인증 확인
    verify = await auth_svc.verify(login_form.username, login_form.password)
    if not verify:
        return ResultType(status='error', message=ER.UNAUTHORIZED[1])
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": login_form.username}, expires_delta=access_token_expires)
    refresh_token = await create_refresh_token(data={"sub": login_form.username}, expires_delta=refresh_token_expires)
    
    # 쿠키에 저장
    response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, expires=refresh_token_expires, httponly=True)
    return ResultType(status='success', message=SU.SUCCESS[1])

'''
회원가입 엔드포인트
'''
@router.post(
    "/signup",
    summary="회원가입",
    description="새 사용자 계정을 생성합니다.",
    responses=Status.docs(SU.CREATED, ER.INVALID_REQUEST, ER.DUPLICATE_RECORD),
)
async def post_signup(
    login_info: Optional[CreateUserInfo],
    code: str
):
    # 사용자 존재 여부 확인
    if login_info and await auth_svc.is_user(login_info.user_id, login_info.user_name, login_info.user_email, code):
        return ResultType(status='error', message=ER.DUPLICATE_RECORD[1])
    if not await auth_svc.verify_email(code):
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

    # 회원가입 처리
    await auth_svc.post_signup(login_info)
    return ResultType(status='success', message=SU.CREATED[1])

'''
로그아웃 엔드포인트
'''
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
    return ResultType(status='success', message=SU.SUCCESS[1])

'''
리프레시 토큰을 이용해 새로운 접근 토큰을 발급하는 엔드포인트
'''
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
        return ResultType(status='success', message=SU.CREATED[1])
    except Exception as e:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

'''
토큰 검증 엔드포인트
'''
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
    return ResultType(status='success', message=SU.SUCCESS[1], detail={"access_token": ac, "refresh_token": rf})

'''
이메일 전송 엔드포인트
'''
@router.get(
    "/send",
    summary="이메일 전송",
    description="사용자에게 인증 이메일을 전송합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def verify_email(user_email: str = Query(..., description="사용자 이메일")):
    await auth_svc.send_confirmation_email(user_email)
    return ResultType(status='success', message=SU.SUCCESS[1])

'''
코드 확인 엔드포인트
'''
@router.get(
    "/code",
    summary="코드 확인",
    description="이메일 인증 코드를 확인합니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def code():
    res = await auth_svc.code()
    return ResultType(status='success', message=SU.SUCCESS[1], detail={"code": res})
