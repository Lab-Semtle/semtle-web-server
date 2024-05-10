"""
RDB Session Module
"""
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings


DATABASE_URL = settings.DATABASE_URL

# 비동기 데이터베이스 엔진 생성, 커넥션 풀 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,    # SQL 문장 로그로 출력
    future=True,  # SQLAlchemy 2.0 스타일 활성화
)

# 데이터베이스 세션 생성
SessionLocal = sessionmaker(
    autocommit=False,  # 자동 커밋
    autoflush=False,   # 세션 변동사항 데이터베이스 자동 반영
    bind=engine,      # 세션을 통해 실행되는 SQL 명령에 사용될 엔진 지정
    # class_=AsyncSessionLocal
)
# AsyncSessionLocal

Base = declarative_base()


# 데이터베이스 세션 생성 및 사용 후 종료
def get_db():
    db = SessionLocal()
    try:
        yield db  # db 연결 성공한 경우, DB 세션 시작
    finally:
        db.close()  # API 호출 끝나면, DB세션 닫기
