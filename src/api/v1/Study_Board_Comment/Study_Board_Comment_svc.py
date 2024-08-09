"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""

from fastapi import UploadFile, File
# 호출할 모듈 추가
from src.api.v1.Study_Board_Comment.Study_Board_Comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.Study_Board_Comment import Study_Board_Comment_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_Study_Board_Comment(db: AsyncSession, Study_Board_no: int, skip: int = 0) -> list[ReadCommentlist]:
    total, Comment_info = await Study_Board_Comment_dao.get_Study_Board_Comment(db, Study_Board_no, skip)
    Comment_info = [ReadComment.from_orm(Comment).dict() for Comment in Comment_info]
    return total, Comment_info


# Create
async def create_Study_Board_Comment(Study_Board_no: int, Content: str, File_name: list[UploadFile], db: AsyncSession) -> None:
    await Study_Board_Comment_dao.create_Study_Board_Comment(Study_Board_no, Content, File_name, db)
    
    
# Update
async def update_Study_Board_Comment(Study_Board_no: int ,Comment_no: int, Content: str, File_name: list[UploadFile], db: AsyncSession) -> None:
    await Study_Board_Comment_dao.delete_Image_Study_Board_Comment(Study_Board_no, Comment_no)
    await Study_Board_Comment_dao.update_Study_Board_Comment(Study_Board_no, Comment_no, Content, File_name, db)
    

# Delete
async def delete_Study_Board_Comment(Study_Board_no: int, Comment_no: int, db: AsyncSession) -> None:
    await Study_Board_Comment_dao.delete_Study_Board_Comment(Study_Board_no, Comment_no, db)