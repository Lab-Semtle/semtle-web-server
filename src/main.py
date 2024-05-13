"""
메인 서버 모듈
"""
from fastapi import FastAPI
from core.cors import setup_cors
from core.event import app_lifespan
from core.error import setup_error_handling
from api.v1 import router as v1_router

from var.session import engine, Base


app = FastAPI(
    title="Semtle-Web-Server",
    version="0.1",
    description="API 서버",
    lifespan=app_lifespan  # 생명주기 이벤트 설정
)

# CORS 설정
setup_cors(app)

# 에러 핸들링 설정 (미작성)
setup_error_handling(app)

# API v1 라우터 추가
app.include_router(v1_router, prefix="/api/v1")
