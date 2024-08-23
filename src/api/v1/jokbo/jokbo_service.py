from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.api.v1.jokbo import jokbo_dao
from typing import Optional

logger = logging.getLogger(__name__)

async def save_file(contents: bytes, filename: str, db: AsyncSession) -> bool:
    try:
        await jokbo_dao.insert_file(db, filename, contents)
        logger.info(f"파일 {filename} 저장 성공.")
        return True
    except Exception as e:
        logger.error(f"파일 {filename} 저장 실패. : {e}")
        return False

async def get_file(filename: str, db: AsyncSession) -> Optional[dict]:
    try:
        file_record = await jokbo_dao.get_file_by_name(db, filename)
        if file_record:
            return {"filename": file_record.filename, "content": file_record.content}
        else:
            return None
    except Exception as e:
        logger.error(f"파일 {filename} 불어오기 실패: {e}")
        return None
