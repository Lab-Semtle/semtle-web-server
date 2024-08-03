"""
메인 서버 모듈
"""
from fastapi import FastAPI
from src.core.cors import setup_cors
from src.core.event import app_lifespan
from src.core.error import setup_error_handling
from src.api.v1 import router as v1_router
from src.core.config import setup_logging


setup_logging()  # 로깅 설정


app = FastAPI(
    title="Semtle-Web-Server",
    version="0.1",
    description="API 서버",
    lifespan=app_lifespan  # 생명주기 이벤트 설정
)


setup_cors(app)  # CORS 설정
setup_error_handling(app)  # 에러 핸들링 설정
app.include_router(v1_router, prefix="/api/v1")  # API v1 라우터 추가