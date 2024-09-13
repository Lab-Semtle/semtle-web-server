"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
from typing import Optional, Annotated, List
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field, validator, field_validator
from src.lib.dto import BaseDTO


class ReadComment(BaseDTO):
    board_no: Annotated[int, Field(description="스터디 게시판 게시물 번호")]
    comment_no: Annotated[int, Field(description="스터디 게시판 게시물 댓글 번호")]
    content: Annotated[Optional[str] | None, Form(description="스터디 게시판 게시물 댓글 내용")]
    create_date: Annotated[datetime, Field(description="스터디 게시판 게시물 댓글 작성 일자")] = Field(
        default_factory=lambda: datetime.now().replace(second=0, microsecond=0).replace(tzinfo=None), description="댓글 작성 일자")
    image_paths : Annotated[Optional[list[str]], Form(description="스터디 게시판 댓글 이미지 파일 다중 경로")]
    likes: Annotated[int, Field(description="스터디 게시판 게시물 댓글 공감수")]

    @field_validator('image_paths', mode='before')
    def split_image_paths(cls, v):
        if isinstance(v, str):
            # 콤마로 구분된 문자열을 리스트로 변환
            return v.split(',')
        return v

class UpdateComment(BaseDTO):
    content: Annotated[Optional[str] | None, Form(description="스터디 게시판 게시물 댓글 내용")]

class CreateComment(UpdateComment):
    ...

class ReadCommentlist(BaseDTO):
    total: Annotated[int, Form(description="스터디 게시판 게시물 댓글 전체 갯수")] = 0
    Board_info: Annotated[List[ReadComment], Form(description="게시물 댓글 데이터")] = []