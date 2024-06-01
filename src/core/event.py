"""
FastAPI 웹 애플리케이션 생명주기 이벤트 처리
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.var.session import AsyncEngine
from src.var.models import Base
from sqlalchemy import text, inspect
import logging

logger = logging.getLogger(__name__)


async def table_has_changes(conn, table):
    def get_db_columns(sync_conn, table_name):
        inspector = inspect(sync_conn)
        return {col['name']: col for col in inspector.get_columns(table_name)}

    db_columns = await conn.run_sync(get_db_columns, table.name)
    model_columns = {col.name: col for col in table.columns}

    if db_columns.keys() != model_columns.keys():
        return True

    for col_name, model_col in model_columns.items():
        db_col = db_columns.get(col_name)
        if not db_col:
            continue

        if str(db_col['type']) != str(model_col.type):
            return True
        if db_col['nullable'] != model_col.nullable:
            return True
        if 'default' in db_col and db_col['default'] != model_col.default:
            return True

    return False


async def recreate_table(conn, table):
    quoted_table_name = f'"{table.name}"'
    # Drop the existing table if it exists
    drop_command = f"DROP TABLE IF EXISTS {quoted_table_name} CASCADE"
    await conn.execute(text(drop_command))
    logger.info(f"테이블 {table.name} 삭제됨")
    # Create the new table
    await conn.run_sync(Base.metadata.create_all)
    logger.info(f"테이블 {table.name} 생성됨")


async def check_and_update_tables():
    async with AsyncEngine.begin() as conn:
        def get_inspector(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        db_tables = await conn.run_sync(get_inspector)

        for table in Base.metadata.sorted_tables:
            if table.name in db_tables:
                logger.info(f"테이블 {table.name} 존재, 변동사항 검사 중...")
                if await table_has_changes(conn, table):
                    logger.info(f"테이블 {table.name}에 변동사항이 있음, 재생성 중...")
                    await recreate_table(conn, table)
                else:
                    logger.info(f"테이블 {table.name}에 변동사항이 없음")
            else:
                logger.info(f"테이블 {table.name} 생성 중...")
                await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    애플리케이션 주요 생명주기 이벤트를 관리하는 함수
    - FastAPI 애플리케이션 인스턴스에 대한 이벤트 핸들러 등록
    - 특정 이벤트 발생 시 해당 함수 호출
    """
    # 시작 이벤트 처리
    logger.info("애플리케이션 서버를 시작합니다...")
    await check_and_update_tables()

    yield  # 여기에서 FastAPI가 요청 처리를 시작

    # 종료 이벤트 처리
    logger.info("애플리케이션 서버를 종료합니다...")
    await AsyncEngine.dispose()  # 리소스 정리: 데이터베이스 연결 해제
