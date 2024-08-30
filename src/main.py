"""
메인 서버 모듈
"""
from src.core import setup_logging
from src.core import cors, error, event
from src.core.router import SemtleAPI
import logging

setup_logging()  # 로깅 설정
logger = logging.getLogger(__name__)


app = SemtleAPI(
    title="Semtle API Server",
    description="Semtle 공식 웹페이지",
    version="0.1",
    docs_url="/docs",   # 개발 중에는 문서 활성화
    redoc_url="/redoc", # 개발 중에는 ReDoc 활성화
    # disable_api_doc=True  # 배포 시 False로 변경할 것, True로 설정하면 API 문서 비활성화
)

# 라우터 매니저를 사용하여 라우터 로드
app.use_router_manager(base_path="./src/api/v1")

# 필요한 확장 모듈 사용
app.use(cors)  # CORS 설정 모듈 사용
app.use(error) # 에러 핸들링 모듈 사용
app.use(event) # 이벤트 핸들링 모듈 사용

logger.info('=>> 서버 시작 중...')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)