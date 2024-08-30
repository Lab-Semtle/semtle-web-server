"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.api.v1.comment_exam.comm_exam_dto import UpdateComment, CreateComment, ReadCommentlist
from src.database.models import ExamComment
from src.database.session import rdb


@rdb.dao()
async def get_exam_sharing_board_comment(db: AsyncSession, exam_sharing_board_no: int, skip: int = 0) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(ExamComment).filter(ExamComment.Board_no == exam_sharing_board_no).order_by(ExamComment.Board_no.desc()).offset(skip*10).limit(10))
    exam_sharing_board_comment_info = result.scalars().all()
    total = await db.execute(select(func.count(ExamComment.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_comment_info

@rdb.dao(transactional=True)
async def create_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_info: CreateComment, db: AsyncSession):
    create_values = {
    "Board_no": exam_sharing_board_no,
    "Content": exam_sharing_board_comment_info.Content,
    "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "Likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    await db.execute(insert(ExamComment).values(create_values))
    
@rdb.dao(transactional=True)
async def update_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int, exam_sharing_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(ExamComment).filter(ExamComment.Board_no == exam_sharing_board_no).filter(ExamComment.Comment_no == exam_sharing_board_comment_no).values(exam_sharing_board_comment_info.dict()))
    
@rdb.dao(transactional=True)
async def delete_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(ExamComment).filter(ExamComment.Board_no == exam_sharing_board_no).filter(ExamComment.Comment_no == exam_sharing_board_comment_no))

@rdb.dao(transactional=True)
async def all_delete_exam_sharing_board_comment(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(ExamComment).filter(ExamComment.Board_no == exam_sharing_board_no))
    