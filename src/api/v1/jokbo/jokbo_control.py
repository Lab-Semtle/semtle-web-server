from typing import Annotated, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, Response
from core.status import Status, SU, ER
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from var.session import get_db
from api.v1.jokbo import jokbo_service
from src.lib.security import JWTBearer
from fastapi.responses import StreamingResponse
from urllib.parse import quote, unquote
from io import BytesIO

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jokbo", tags=["jokbo"])

@router.post(
    "/",
    summary="파일 저장",
    description="- 형식 상관 X",
    responses=Status.docs(SU.CREATED, ER.UNAUTHORIZED,ER.INTERNAL_ERROR,ER.NOT_FOUND)
)
async def upload_file(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    user: Annotated[Optional[dict], Depends(JWTBearer())] = None
):
    if not user:
        return ER.UNAUTHORIZED

    try:
        contents = await file.read()  # 바이너리로 파일 읽기
        logger.info(f"파일 업로드 성공: {file.filename}")

        result = await jokbo_service.save_file(contents, file.filename, db)

        if result:
            return SU.CREATED
        else:
            return ER.INTERNAL_ERROR
    except Exception as e:
        logger.error(f"파일 업로드 중에 문제가 발생 : {e}")
        return {"status": ER.NOT_FOUND, "message": "업로드 중에 문제가 발생하였습니다."}

@router.get(
    "/",
    summary="파일 불러오기",
    description="- 파일 이름으로 파일을 불러옵니다",
    responses=Status.docs(SU.SUCCESS, ER.UNAUTHORIZED,ER.NOT_FOUND)
)
async def get_file(
    filename: str = Query(..., description="불러올 파일의 이름"),
    db: AsyncSession = Depends(get_db),
    user: Annotated[Optional[dict], Depends(JWTBearer())] = None
):
    if not user:
        raise ER.UNAUTHORIZED

    decoded_filename = unquote(filename)  # URL 디코딩
    file_data = await jokbo_service.get_file(decoded_filename, db)
    if file_data:
        file_stream = BytesIO(file_data["content"])
        return StreamingResponse(
            file_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(file_data['filename'])}"}
        )
    else:
        raise ER.NOT_FOUND
