"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.Free_Board_Comment.Free_Board_Comment_dto import UpdateComment, ReadComment, CreateComment
from src.api.v1.Free_Board_Comment import Free_Board_Comment_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_Free_Board_Comment(Free_Board_no: int, db: AsyncSession) -> list[ReadComment]:
    Comment_info = await Free_Board_Comment_dao.get_Free_Board_Comment(Free_Board_no, db)
    return Comment_info

# Create
async def create_Free_Board_Comment(Comment_info: CreateComment, db: AsyncSession) -> None:
    await Free_Board_Comment_dao.create_Free_Board_Comment(Comment_info, db)
    
    
# Update
async def update_Free_Board_Comment(Free_Board_no: int ,Comment_no: int, example_info: UpdateComment, db: AsyncSession) -> None:
    await Free_Board_Comment_dao.update_Free_Board_Comment(Free_Board_no, Comment_no, example_info, db)
    

# Delete
async def delete_Free_Board_Comment(Free_Board_no: int, Comment_no: int, db: AsyncSession) -> None:
    await Free_Board_Comment_dao.delete_Free_Board_Comment(Free_Board_no, Comment_no, db)