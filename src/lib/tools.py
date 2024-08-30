"""
데이터베이스 세션 관리 도구 모음
"""
from typing import AsyncIterable, Callable, Any
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps
from src.database.models import Base
import logging
_logger = logging.getLogger(__name__)


class RDBTools:
    ''' 데이터베이스 세션 도구 모음 '''
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.session_factory = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_tables(self):
        ''' 모델에 기반해 테이블 생성 '''
        _logger.info('모델 메타 데이터에 기반하여 테이블 유무 확인 후, 생성')
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose_engine(self):
        ''' 데이터베이스 엔진 종료 '''
        _logger.info('DB 연결 해제')
        await self.engine.dispose()
    
    @asynccontextmanager
    async def get_session(self) -> AsyncIterable[AsyncSession]:
        ''' 
        데이터베이스 세션 가져오기 
        - 세션에서 작업이 명시적으로 commit 되지 않으면 데이터베이스에 적용 X, 세션 종료 시 롤백
        - 단순 데이터 조회/ 트랜잭션 직접 관리 X 일 때 사용
        - 트랜잭션 오버헤드 피할 수 있음.
        '''
        async with self.session_factory() as session:
            yield session

    @asynccontextmanager
    async def get_transaction_session(self) -> AsyncIterable[AsyncSession]:
        ''' 
        트랜잭션 세션 가져오기 
        - 세션이 종료될 때 자동으로 커밋 또는 롤백
        - 데이터베이스 변경 작업(삽입, 업데이트, 삭제 등) 수행 시 사용
        '''
        async with self.session_factory.begin() as session:
            yield session

    def dao(self, transactional: bool = False, session_var_name: str = "db"):
        '''
        DAO 데코레이터 팩토리
        :transactional: 트랜잭션 사용 여부
        :session_var_name: 세션을 주입할 변수 이름
        '''
        def dao_decorator(original_function: Callable[..., Any]):
            ''' DAO 데코레이터 '''
            @wraps(original_function)
            async def wrapper(*args, **kwargs):
                get_session = self.get_transaction_session if transactional else self.get_session
                async with get_session() as session:
                    kwargs[session_var_name] = session
                    result = await original_function(*args, **kwargs)
                return result
            return wrapper
        return dao_decorator
