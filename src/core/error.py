"""
전역 예외 처리 및 로깅 설정 모듈
"""
import traceback
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.lib.status import ER
import logging

logger = logging.getLogger(__name__)


def log_error(err: Exception):
    """ 예외 정보를 로깅 """
    logger.error(f"Error: {traceback.format_exc()}")


def use(app: FastAPI):
    """ 전역 예외 핸들러 설정 """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """ 
        필드 유효성 검증 오류가 발생했을 때 호출
        """
        log_error(exc)
        return JSONResponse(status_code=ER.FIELD_VALIDATION_ERROR[0], content={"message": ER.FIELD_VALIDATION_ERROR[1]})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        HTTP 관련 예외가 발생했을 때 호출
        """
        log_error(exc)
        return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        위에서 처리되지 않은 모든 예외에 대해 호출
        """
        log_error(exc)
        return JSONResponse(status_code=ER.INTERNAL_ERROR[0], content={"message": ER.INTERNAL_ERROR[1]})
