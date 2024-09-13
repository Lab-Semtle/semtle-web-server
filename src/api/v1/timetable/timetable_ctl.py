from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response, HTTPException
from src.lib.type import ResultType 
from src.lib.status import Status, SU, ER 
from src.api.v1.timetable import timetable_svc 
from src.lib.security import JWTBearer

router = APIRouter(prefix="/timetable", tags=["timetable"])

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
async def post_time(user_email: Annotated[str,Depends(JWTBearer().get_user)], data: str):
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
async def get_time(user_email: Annotated[str,Depends(JWTBearer().get_user)]):
    res = await timetable_svc.get_time_data(user_email)
    if res == False:
        return ResultType(status='error', message=ER.INVALID_REQUEST[1])
    return res