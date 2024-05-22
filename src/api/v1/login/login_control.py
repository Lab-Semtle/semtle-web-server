# 기본적으로 추가
from typing import Annotated
from typing import Optional
from fastapi import APIRouter, Depends
from core.type import ResultType
from core.status import Status, SU, ER
from fastapi.security import OAuth2PasswordRequestForm
import logging

# (db 세션 관련)이후 삭제 예정
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db

# 호출할 모듈 추가
from api.v1.login import login_service
from api.v1.login.login_dto import CreateUserInfo

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/login", tags=["login"])


@router.post(
    "/",
    summary="로그인",
    description="- 로그인 기능만 구현, 비밀번호 추후 암호화 해야함, JWT도 해야함",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED)
)
async def post_login(login_form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    logger.info("----------로그인----------")
    verify  = await login_service.verify(login_form.username, login_form.password, db)
    if not verify:
        return ER.UNAUTHORIZED
    return SU.SUCCESS

@router.post(
    "/{signup}",
    summary="회원가입",
    description="- 회원가입 기능만 구현, 비밀번호 추후 암호화 해야함, JWT도 해야함",
    responses=Status.docs(SU.CREATED, ER.DUPLICATE_RECORD),
)
async def post_signup(login_info: Optional[CreateUserInfo], db: AsyncSession = Depends(get_db)):
    logger.info("----------회원가입----------")
    
    if login_info and await login_service.is_user(login_info.user_id, login_info.user_name, login_info.user_email, login_info.user_phone, db):
        logger.warning("이미 존재하는 유저입니다.")
        return ER.DUPLICATE_RECORD

    await login_service.post_signup(login_info, db)
    return SU.CREATED