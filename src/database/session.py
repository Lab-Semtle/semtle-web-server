"""
RDB 세션 모듈 : 데이터베이스 연결 및 세션 설정
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.lib.tools import RDBTools
from src.core import settings


DATABASE_URL = settings.rdb.DATABASE_URL

# 비동기 데이터베이스 엔진 생성, 커넥션 풀 생성
AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,    # SQL 문장 로그로 출력
    future=True,  # SQLAlchemy 2.0 스타일 활성화
)

# 데이터베이스 세션 생성
AsyncSessionLocal = sessionmaker(
    autocommit=False,  # 자동 커밋
    autoflush=False,   # 세션 변동사항 데이터베이스 자동 반영
    bind=AsyncEngine,      # 세션을 통해 실행되는 SQL 명령에 사용될 엔진 지정
    class_=AsyncSession,
    expire_on_commit=False
)

rdb = RDBTools(DATABASE_URL)

# 데이터베이스 세션 생성
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session