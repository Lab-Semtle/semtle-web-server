"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from src.api.v1.comment_exam.comm_exam_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.comment_exam import comm_exam_dao


async def get_exam_sharing_board_comment(exam_sharing_board_no: int, skip: int = 0) -> list[ReadCommentlist]:
    total, exam_sharing_board_comment_info = await comm_exam_dao.get_exam_sharing_board_comment(exam_sharing_board_no, skip)
    exam_sharing_board_comment_info = [ReadComment.from_orm(Comment).dict() for Comment in exam_sharing_board_comment_info]
    return total, exam_sharing_board_comment_info

async def create_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_info: CreateComment) -> None:
    await comm_exam_dao.create_exam_sharing_board_comment(exam_sharing_board_no, exam_sharing_board_comment_info)
        
async def update_exam_sharing_board_comment(exam_sharing_board_no: int ,exam_sharing_board_comment_no: int, exam_sharing_board_comment_info: UpdateComment) -> None:
    await comm_exam_dao.update_exam_sharing_board_comment(exam_sharing_board_no, exam_sharing_board_comment_no, exam_sharing_board_comment_info)
    
async def delete_exam_sharing_board_comment(exam_sharing_board_no: int, exam_sharing_board_comment_no: int) -> None:
    await comm_exam_dao.delete_exam_sharing_board_comment(exam_sharing_board_no, exam_sharing_board_comment_no)