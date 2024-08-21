"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.api.v1.exam_sharing_board_comment.exam_sharing_board_comment_dto import UpdateComment, CreateComment, ReadCommentlist
from src.var.models import Exam_Sharing_Board_Comment


# Read
async def get_exam_sharing_board_comment(db: AsyncSession, exam_sharing_board_no: int, skip: int = 0) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(Exam_Sharing_Board_Comment).filter(Exam_Sharing_Board_Comment.Board_no == exam_sharing_board_no).order_by(Exam_Sharing_Board_Comment.Board_no.desc()).offset(skip*10).limit(10))
    exam_sharing_board_comment_info = result.scalars().all()
    total = await db.execute(select(func.count(Exam_Sharing_Board_Comment.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_comment_info


# Create
async def create_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_info: CreateComment, db: AsyncSession):
    create_values = {
    "Board_no": exam_sharing_board_no,
    "Content": exam_sharing_board_comment_info.Content,
    "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "Likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    await db.execute(insert(Exam_Sharing_Board_Comment).values(create_values))
    await db.commit()
    
    
# Update
async def update_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int, exam_sharing_board_comment_info: UpdateComment, db: AsyncSession) -> None:
    await db.execute(update(Exam_Sharing_Board_Comment).filter(Exam_Sharing_Board_Comment.Board_no == exam_sharing_board_no).filter(Exam_Sharing_Board_Comment.Comment_no == exam_sharing_board_comment_no).values(exam_sharing_board_comment_info.dict()))
    await db.commit()
    

# Delete
async def delete_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Exam_Sharing_Board_Comment).filter(Exam_Sharing_Board_Comment.Board_no == exam_sharing_board_no).filter(Exam_Sharing_Board_Comment.Comment_no == exam_sharing_board_comment_no))
    await db.commit()


# Delete
async def all_delete_exam_sharing_board_comment(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Exam_Sharing_Board_Comment).filter(Exam_Sharing_Board_Comment.Board_no == exam_sharing_board_no))
    await db.commit()