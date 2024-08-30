"""
유저 API
"""
from typing import Annotated
from fastapi import APIRouter, Depends
from src.lib.type import ResultType
from src.lib.status import Status, SU, ER
from src.lib.security import JWTBearer
from src.api.v1.user.user_dto import ReadUserInfo, UpdateUserInfo
from src.api.v1.user import user_svc


router = APIRouter(prefix="/user", tags=["user"])

'''
전체 유저 정보 목록 조회 엔드포인트
'''
@router.get(
    "/view_all",
    summary="전체 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 등록된 유저가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_users():
    users_info = await user_svc.get_users()
    return ResultType(status='success', message=SU.SUCCESS[1], detail=users_info)

'''
특정 유저 정보 조회 엔드포인트
'''
@router.get(
    "/view_one",
    summary="특정 유저 정보 목록 조회",
    description="- 유저 정보 리스트 반환, 유저 정보가 없는 경우 `[]` 반환",
    response_model=list[ReadUserInfo],
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def get_user(user_id: Annotated[str,Depends(JWTBearer().get_user)]):
    user_info = await user_svc.get_user(user_id)
    return ResultType(status='success', message=SU.SUCCESS[1], detail=user_info)

'''
유저 정보 수정 엔드포인트
'''
@router.patch(
    "/user_info_modify",
    summary="유저 정보 수정",
    description="- ",
    responses=Status.docs(SU.ACCEPTED, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def update_user(user_id: Annotated[str,Depends(JWTBearer().get_user)], user_info: UpdateUserInfo):
    res = await user_svc.update_user(user_id, user_info)
    if res:
        return ResultType(status='success', message=SU.ACCEPTED[1])
    else:
        return ResultType(status='error', message=ER.NOT_FOUND[1])

'''
유저 삭제 엔드포인트
'''
@router.delete(
    "/user_delete",
    summary="유저 삭제",
    description="- 유저 삭제",
    responses=Status.docs(SU.SUCCESS, ER.NOT_FOUND),
    dependencies=[Depends(JWTBearer())],
)
async def delete_user(user_id: Annotated[str,Depends(JWTBearer().get_user)]):
    await user_svc.delete_user(user_id)
    return ResultType(status='success', message=SU.SUCCESS[1])