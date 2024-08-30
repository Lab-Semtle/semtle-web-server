"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
from typing import Optional, Annotated, List
from datetime import datetime
from fastapi import Form
from pydantic import Field
from src.lib.dto import BaseDTO


class ReadComment(BaseDTO):
    Board_no: Annotated[int, Field(description="족보 게시판 게시물 번호")]
    Comment_no: Annotated[int, Field(description="족보 게시판 게시물 댓글 번호")]
    Content: Annotated[Optional[str] | None, Form(description="족보 게시판 게시물 댓글 내용")]
    Create_date: Annotated[datetime, Field(description="댓글 작성 일자")] = Field(
        default_factory=lambda: datetime.now().replace(second=0, microsecond=0).replace(tzinfo=None), description="댓글 작성 일자")
    Likes: Annotated[int, Field(description="족보 게시판 게시물 댓글 공감수")]

class UpdateComment(BaseDTO):
    Content: Annotated[Optional[str] | None, Form(description="족보 게시판 게시물 댓글 내용")]

class CreateComment(UpdateComment):
    ...

class ReadCommentlist(BaseDTO):
    total: Annotated[int, Form(description="족보 게시판 게시물 댓글 전체 갯수")] = 0
    Board_info: Annotated[List[ReadComment], Form(description="게시물 댓글 데이터")] = []

