from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from var.models import FileRecord

async def insert_file(db: AsyncSession, filename: str, contents: bytes) -> None:
    file_record = FileRecord(filename=filename, content=contents)
    db.add(file_record)
    await db.commit()

async def get_file_by_name(db: AsyncSession, filename: str) -> Optional[FileRecord]:
    result = await db.execute(select(FileRecord).where(FileRecord.filename == filename))
    return result.scalars().first()
