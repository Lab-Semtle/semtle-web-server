"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
from typing import Optional, Annotated, List
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.lib.dto import BaseDTO


class ReadBoard(BaseDTO):
    Board_no: Annotated[int, Field(description="자유 게시판 게시물 번호")]
    Title: Annotated[str, Form(description="자유 게시판 게시물 제목")]
    Content: Annotated[Optional[str] | None, Form(description="자유 게시판 게시물 내용")]
    Create_date: Annotated[datetime, Field(description="자유 게시판 게시물 작성 일자")] = Field(
        default_factory=lambda: datetime.now().replace(second=0, microsecond=0).replace(tzinfo=None), description="자유 게시판 게시물 작성 일자")
    Views: Annotated[int, Field(description="자유 게시판 게시물 조회수")]

class UpdateBoard(BaseDTO):
    Title: Annotated[str, Form(description="자유 게시판 게시물 제목")]
    Content: Annotated[Optional[str] | None, Form(description="자유 게시판 게시물 내용")]

class CreateBoard(UpdateBoard):
    Views: Annotated[int, Field(description="자유 게시판 게시물 조회수")]

class ReadBoardlist(BaseDTO):
    total: Annotated[int, Form(description="자유 게시판 전체 게시물 갯수")] = 0
    Board_info: Annotated[List[ReadBoard], Form(description="게시물 데이터")] = []
