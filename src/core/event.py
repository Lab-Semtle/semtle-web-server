"""
FastAPI 웹 애플리케이션 생명주기 이벤트 처리
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from var.session import engine, Base


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    애플리케이션 주요 생명주기 이벤트를 관리하는 함수
    - FastAPI 애플리케이션 인스턴스에 대한 이벤트 핸들러 등록
    - 특정 이벤트 발생 시 해당 함수 호출
    """
    # 시작 이벤트 처리
    print("애플리케이션 서버를 시작합니다...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 데이터베이스 스키마 생성

    yield  # 여기에서 FastAPI가 요청 처리를 시작

    # 종료 이벤트 처리
    print("애플리케이션 서버를 종료합니다...")
