from typing import Optional
from fastapi import APIRouter, Depends, Response, Request, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta
from decouple import config
from src.lib.type import ResultType
from src.lib.status import Status, SU, ER
from src.api.v1.login import login_svc
from src.lib.security import JWTBearer, create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from src.api.v1.login.login_dto import CreateUserInfo

# 환경 변수에서 토큰 만료 시간 설정
ACCESS_TOKEN_EXPIRE_MINUTES = float(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = float(config("REFRESH_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(prefix="/login", tags=["login"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''
로그인 엔드포인트
'''
@router.post(
    "/login",
    summary="로그인",
    description="사용자 인증 후 JWT 토큰을 발급합니다.",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED, ER.INVALID_REQUEST)
)
async def post_login(
    response: Response,
    login_form: OAuth2PasswordRequestForm = Depends()
):
    # 사용자 인증 확인
    verify = await login_svc.verify(login_form.username, login_form.password)
    if not verify:
        return ResultType(status='error', message=ER.UNAUTHORIZED[1])
    try:
        #토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(data={"sub": login_form.username}, expires_delta=access_token_expires)
        refresh_token = await create_refresh_token(data={"sub": login_form.username}, expires_delta=refresh_token_expires)

        # 쿠키에 저장
        response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, expires=refresh_token_expires, httponly=True)
        
        return ResultType(status='success', message=SU.SUCCESS[1])
    except:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

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
    if login_info and await login_svc.is_user(login_info.user_nickname, login_info.user_name, login_info.user_email, login_info.user_phone):
        return ResultType(status='error', message=ER.DUPLICATE_RECORD[1])
    if not await login_svc.verify_email(code):
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

    # 회원가입 처리
    res = await login_svc.post_signup(login_info)
    if res:
        return ResultType(status='success', message=SU.CREATED[1])
    return ResultType(status='error', message=ER.INVALID_REQUEST[1])


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
    try:
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return ResultType(status='success', message=SU.SUCCESS[1])
    except:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

'''
리프레시 토큰을 이용해 새로운 접근 토큰을 발급하는 엔드포인트
'''
@router.get(
    "/refresh",
    summary="Access 토큰 재발급",
    description="Refresh 토큰을 사용하여 새로운 Access 토큰을 발급합니다.",
    responses=Status.docs(SU.CREATED, ER.INVALID_TOKEN, ER.INVALID_REQUEST),
)
async def refresh_token(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return ResultType(status='error', message=ER.INVALID_TOKEN[1])
        
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
    "/access_token",
    summary="토큰 가져오기",
    description="Access 토큰을 가져옵니다.",
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
)
async def get_access_token(request: Request):
    try:
        access_token = request.cookies.get("access_token")
        return {"access_token": ac}
    except:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])

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
    res = await login_svc.send_confirmation_email(user_email)
    if res:
        return ResultType(status='success', message=SU.SUCCESS[1])
    return ResultType(status='error', message=ER.INVALID_REQUEST[1])

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
    res,check = await login_svc.code()
    if check:
        return ResultType(status='success', message=SU.SUCCESS[1], detail={"code": res})
    return ResultType(status='error', message=ER.INVALID_REQUEST[1])
