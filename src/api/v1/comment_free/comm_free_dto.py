"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated, List
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.lib.dto import BaseDTO


# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)


class ReadComment(BaseDTO):
    board_no: Annotated[int, Field(description="자유 게시판 게시물 번호")]
    comment_no: Annotated[int, Field(description="자유 게시판 게시물 댓글 번호")]
    content: Annotated[Optional[str] | None, Form(description="자유 게시판 게시물 댓글 내용")]
    create_date: Annotated[datetime, Field(description="댓글 작성 일자")] = Field(
        default_factory=lambda: datetime.now().replace(second=0, microsecond=0).replace(tzinfo=None), description="댓글 작성 일자")
    likes: Annotated[int, Field(description="자유 게시판 게시물 댓글 공감수")]

    class Config:
        from_attributes = True

class UpdateComment(BaseDTO):
    content: Annotated[Optional[str] | None, Form(description="자유 게시판 게시물 댓글 내용")]

class CreateComment(UpdateComment):
    ...

class ReadCommentlist(BaseDTO):
    total: Annotated[int, Form(description="자유 게시판 게시물 댓글 전체 갯수")] = 0
    Board_info: Annotated[List[ReadComment], Form(description="게시물 댓글 데이터")] = []

    class Config:
        from_attributes = True

