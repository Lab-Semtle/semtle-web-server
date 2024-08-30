"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.api.v1_ewha.free_board_comment.free_board_comment_dto import UpdateComment, CreateComment, ReadCommentlist
from src.database.models import Free_Board_Comment


# Read
async def get_free_board_comment(db: AsyncSession, free_board_no: int, skip: int = 0) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(Free_Board_Comment).filter(Free_Board_Comment.Board_no == free_board_no).order_by(Free_Board_Comment.Board_no.desc()).offset(skip*10).limit(10))
    free_board_comment_info = result.scalars().all()
    total = await db.execute(select(func.count(Free_Board_Comment.Board_no)))
    total = total.scalar()
    return total, free_board_comment_info


# Create
async def create_free_board_comment(free_board_no: int, free_board_comment_info: CreateComment, db: AsyncSession):
    create_values = {
    "Board_no": free_board_no,
    "Content": free_board_comment_info.Content,
    "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "Likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    await db.execute(insert(Free_Board_Comment).values(create_values))
    await db.commit()
    
    
# Update
async def update_free_board_comment(free_board_no: int, free_board_comment_no: int, free_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(Free_Board_Comment).filter(Free_Board_Comment.Board_no == free_board_no).filter(Free_Board_Comment.Comment_no == free_board_comment_no).values(free_board_comment_info.dict()))
    await db.commit()
    

# Delete
async def delete_free_board_comment(free_board_no: int, free_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Free_Board_Comment).filter(Free_Board_Comment.Board_no == free_board_no).filter(Free_Board_Comment.Comment_no == free_board_comment_no))
    await db.commit()


# Delete
async def all_delete_free_board_comment(free_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Free_Board_Comment).filter(Free_Board_Comment.Board_no == free_board_no))
    await db.commit()