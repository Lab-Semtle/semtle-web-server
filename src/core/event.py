"""
FastAPI 웹 애플리케이션 생명주기 이벤트 처리
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.session import AsyncEngine, rdb
from src.database.models import Base
from sqlalchemy import text, inspect
import logging

logger = logging.getLogger(__name__)


def use(app: FastAPI):
    """ 이벤트 확장 모듈 """
    
    @app.on_event("startup")
    async def startup_event():
        '''
        서버 시작 이벤트 처리 함수
        '''
        logger.info('=>> 서버 시작 이벤트 호출')
        await rdb.create_tables()
        
    
    @app.on_event("shutdown")
    async def shutdown_event():
        '''
        서버 종료 이벤트 처리 함수
        '''
        logger.info('=>> 서버 종료 이벤트 실행')
        await rdb.dispose_engine()