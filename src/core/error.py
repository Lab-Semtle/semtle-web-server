"""
전역 에러 처리 설정
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.status import ER


def setup_error_handling(app: FastAPI):

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=ER.INTERNAL_ERROR[0],
            content={"message": ER.INTERNAL_ERROR[1]}
        )
