from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response, HTTPException  #
from src.lib.type import ResultType 
from src.lib.status import Status, SU, ER  #
from src.api.v1.timetable import timetable_svc 
from src.lib.security import JWTBearer

router = APIRouter(prefix="/time", tags=["time"])

"""
시간표 데이터 저장 엔드포인트
"""
@router.post(
    "/",
    summary="시간표 데이터 저장", 
    description="- 강의명, 요일, 시작시간, 마치는 시간, 메모", 
    responses=Status.docs(SU.CREATED, ER.INVALID_REQUEST),
    # dependencies=[Depends(JWTBearer())],
)
async def post_time(user_email: str, data: str):
    res = await timetable_svc.post_time_data(user_email, data)
    if res == False:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])
    return ResultType(status='success', message=SU.CREATED[1])

"""
시간표 데이터 가져오기 엔드포인트
"""
@router.get(
    "/",
    summary="시간표 데이터 가져오기", 
    description="- 유저 id", 
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    # dependencies=[Depends(JWTBearer())],
)
async def get_time(user_email: str):
    res = await timetable_svc.get_time_data(user_email)
    if res == False:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])
    return res

@router.post(
    "/cookie",
    summary="쿠키", 
    description="- 쿠키", 
    responses=Status.docs(SU.SUCCESS, ER.INVALID_REQUEST),
    # dependencies=[Depends(JWTBearer())],
)
async def cookie():
    access_token_expires = timedelta(minutes=60)
    refresh_token_expires = timedelta(minutes=21600)
    response.set_cookie(key="access_token", value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYWtqeTAzMTJAZ21haWwuY29tIiwiZXhwIjoxNzI1NDcwODY5fQ.9hMxs0Sro2fGrw5H3YfkIywsRQmWyvZwg4U2KayXzsg", expires=access_token_expires, httponly=True)
    response.set_cookie(key="refresh_token", value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYWtqeTAzMTJAZ21haWwuY29tIiwiZXhwIjoxNzI2NzYzMjY5fQ.U1xMmJ8yLDLOgtjdu3SVz154lZQ9EWLyPlZp7y78IVc", expires=refresh_token_expires, httponly=True)

