"""
전역 에러 처리 설정
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.core.status import ER
import logging

logger = logging.getLogger(__name__)



def setup_error_handling(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):    
        logger.error(f"전역 에러 실행 - 필드 유효성 검증에 실패하였습니다. 즉, 올바르지 않은 값을 입력하였습니다. : {exc}")
        return JSONResponse(
            status_code=ER.FIELD_VALIDATION_ERROR[0],
            content={"message": ER.FIELD_VALIDATION_ERROR[1]}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"전역 에러 실행 - 서버 내부(벡엔드)에 에러가 발생하였습니다. : {exc}")
        return JSONResponse(
            status_code=ER.INTERNAL_ERROR[0],
            content={"message": ER.INTERNAL_ERROR[1]}
        )
