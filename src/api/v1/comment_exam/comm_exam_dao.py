"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.database.session import rdb
from src.api.v1.comment_exam.comm_exam_dto import UpdateComment, CreateComment, ReadCommentlist
from src.database.models import ExamComment


# Read
@rdb.dao()
async def get_exam_sharing_board_comment(exam_sharing_board_no: int, skip: int, db: AsyncSession) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(ExamComment).filter(ExamComment.board_no == exam_sharing_board_no).order_by(ExamComment.board_no.desc()).offset(skip*10).limit(10))
    exam_sharing_board_comment_info = result.scalars().all()
    total = await db.execute(select(func.count(ExamComment.board_no)))
    total = total.scalar()
    return total, exam_sharing_board_comment_info


# Create
@rdb.dao(transactional=True)
async def create_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_info: CreateComment, db: AsyncSession):
    create_values = {
    "board_no": exam_sharing_board_no,
    "content": exam_sharing_board_comment_info.content,
    "create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    await db.execute(insert(ExamComment).values(create_values))

    
    
# Update
@rdb.dao(transactional=True)
async def update_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int, exam_sharing_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(ExamComment).filter(ExamComment.board_no == exam_sharing_board_no).filter(ExamComment.comment_no == exam_sharing_board_comment_no).values(exam_sharing_board_comment_info.dict()))

    

# Delete
@rdb.dao(transactional=True)
async def delete_exam_sharing_board_comment(exam_sharing_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(ExamComment).filter(ExamComment.comment_no == exam_sharing_board_comment_no))



# Delete
@rdb.dao(transactional=True)
async def all_delete_exam_sharing_board_comment(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(ExamComment).filter(ExamComment.board_no == exam_sharing_board_no))
