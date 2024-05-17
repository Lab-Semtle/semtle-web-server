"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from fastapi import Depends
from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.example.example_dto import ReadExampleInfo, CreateExample, UpdateExample, keyExample
from src.var.models import Example
from src.var.session import get_db


# Read
async def get_examples(db: AsyncSession) -> list[ReadExampleInfo]:  # = Depends(get_db)
    result = await db.execute(select(Example))
    examples_info = result.scalars().all()
    return examples_info


# Create
async def create_example(example: CreateExample, db: AsyncSession) -> None:
    await db.execute(insert(Example).values(example.dict()))
    await db.commit() # 자동으로 commit되게 설정 변경 필요
    
    
# Update
async def update_example(example_id: str, example_info: UpdateExample, db: AsyncSession) -> None:
    await db.execute(update(Example).filter(Example.example_id==example_id).values(example_info.dict()))
    await db.commit()
    

# Delete
async def delete_example(example_id: str, db: AsyncSession) -> None:
    await db.execute(delete(Example).where(Example.example_id == example_id))
    await db.commit()