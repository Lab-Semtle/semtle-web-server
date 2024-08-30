"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.free_board_comment.free_board_comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.free_board_comment import free_board_comment_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read
async def get_free_board_comment(db: AsyncSession, free_board_no: int, skip: int = 0) -> list[ReadCommentlist]:
    total, free_board_comment_info = await free_board_comment_dao.get_free_board_comment(db, free_board_no, skip)
    free_board_comment_info = [ReadComment.from_orm(Comment).dict() for Comment in free_board_comment_info]
    return total, free_board_comment_info


# Create
async def create_free_board_comment(free_board_no: int, free_board_comment_info: CreateComment, db: AsyncSession) -> None:
    await free_board_comment_dao.create_free_board_comment(free_board_no, free_board_comment_info, db)
    
    
# Update
async def update_free_board_comment(free_board_no: int ,free_board_comment_no: int, free_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await free_board_comment_dao.update_free_board_comment(free_board_no, free_board_comment_no, free_board_comment_info, db)
    

# Delete
async def delete_free_board_comment(free_board_no: int, free_board_comment_no: int, db: AsyncSession) -> None:
    await free_board_comment_dao.delete_free_board_comment(free_board_no, free_board_comment_no, db)