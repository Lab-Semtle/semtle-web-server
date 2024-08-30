"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.api.v1.comment_free.comm_free_dto import UpdateComment, CreateComment, ReadCommentlist
from src.database.models import FreeComment
from src.database.session import rdb


@rdb.dao()
async def get_free_board_comment(db: AsyncSession, free_board_no: int, skip: int = 0) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(FreeComment).filter(FreeComment.Board_no == free_board_no).order_by(FreeComment.Board_no.desc()).offset(skip*10).limit(10))
    free_board_comment_info = result.scalars().all()
    total = await db.execute(select(func.count(FreeComment.Board_no)))
    total = total.scalar()
    return total, free_board_comment_info

@rdb.dao(transactional=True)
async def create_free_board_comment(free_board_no: int, free_board_comment_info: CreateComment, db: AsyncSession):
    create_values = {
    "Board_no": free_board_no,
    "Content": free_board_comment_info.Content,
    "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "Likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    await db.execute(insert(FreeComment).values(create_values))
    
@rdb.dao(transactional=True)
async def update_free_board_comment(free_board_no: int, free_board_comment_no: int, free_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(FreeComment).filter(FreeComment.Board_no == free_board_no).filter(FreeComment.Comment_no == free_board_comment_no).values(free_board_comment_info.dict()))    

@rdb.dao(transactional=True)
async def delete_free_board_comment(free_board_no: int, free_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(FreeComment).filter(FreeComment.Board_no == free_board_no).filter(FreeComment.Comment_no == free_board_comment_no))

@rdb.dao(transactional=True)
async def all_delete_free_board_comment(free_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(FreeComment).filter(FreeComment.Board_no == free_board_no))
