"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from src.api.v1.comment_free.comm_free_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.comment_free import comm_free_dao


async def get_free_board_comment(free_board_no: int, skip: int = 0) -> list[ReadCommentlist]:
    total, free_board_comment_info = await comm_free_dao.get_free_board_comment(free_board_no, skip)
    free_board_comment_info = [ReadComment.from_orm(Comment).dict() for Comment in free_board_comment_info]
    return total, free_board_comment_info

async def create_free_board_comment(free_board_no: int, free_board_comment_info: CreateComment) -> None:
    await comm_free_dao.create_free_board_comment(free_board_no, free_board_comment_info)
    
async def update_free_board_comment(free_board_no: int ,free_board_comment_no: int, free_board_comment_info: UpdateComment) -> None:
    await comm_free_dao.update_free_board_comment(free_board_no, free_board_comment_no, free_board_comment_info)
    
async def delete_free_board_comment(free_board_no: int, free_board_comment_no: int) -> None:
    await comm_free_dao.delete_free_board_comment(free_board_no, free_board_comment_no)