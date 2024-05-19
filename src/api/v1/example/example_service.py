"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.example.example_dto import ReadExampleInfo, CreateExample, UpdateExample, keyExample
from src.api.v1.example import example_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_examples(db: AsyncSession) -> list[ReadExampleInfo]:
    examples_info = await example_dao.get_examples(db)
    return examples_info

# Create
async def create_example(example: CreateExample, db: AsyncSession) -> None:
    await example_dao.create_example(example, db)
    
    
# Update
async def update_example(example_id: str, example_info: UpdateExample, db: AsyncSession) -> None:
    await example_dao.update_example(example_id, example_info, db)
    

# Delete
async def delete_example(example_id: str, db: AsyncSession) -> None:
    await example_dao.delete_example(example_id, db)