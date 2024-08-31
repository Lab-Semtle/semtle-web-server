"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 호출할 모듈 추가
from src.api.v1.free_board_comment.free_board_comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.api.v1.free_board_comment import free_board_comment_dao


# Read
async def get_free_board_comment(free_board_no: int, skip: int) -> list[ReadCommentlist]:
    total, free_board_comment_info = await free_board_comment_dao.get_free_board_comment(free_board_no, skip)
    free_board_comment_info = [ReadComment.from_orm(Comment).dict() for Comment in free_board_comment_info]
    return total, free_board_comment_info


# Create
async def create_free_board_comment(free_board_no: int, free_board_comment_info: CreateComment) -> None:
    await free_board_comment_dao.create_free_board_comment(free_board_no, free_board_comment_info)
    
    
# Update
async def update_free_board_comment(free_board_no: int ,free_board_comment_no: int, free_board_comment_info: UpdateComment) -> None:
    await free_board_comment_dao.update_free_board_comment(free_board_no, free_board_comment_no, free_board_comment_info)
    

# Delete
async def delete_free_board_comment(free_board_no: int, free_board_comment_no: int) -> None:
    await free_board_comment_dao.delete_free_board_comment(free_board_no, free_board_comment_no)