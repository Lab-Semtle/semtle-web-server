"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.var.dto import BaseDTO
from src.var.models import Free_Board


# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)

class UpdateBoard(BaseDTO):
    Title: Annotated[str, Form(description="자유 게시판 게시물 제목")]
    Content: Annotated[str | None, Form(description="자유 게시판 게시물 내용")]
    Create_date: Annotated[datetime, Depends(lambda: datetime.now(timezone.utc))] = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="가입 일자")


class ReadBoard(BaseDTO):
    total: int = 0
    question_list: list[Free_Board] = []

class CreateBoard(UpdateBoard):
    Board_no: Annotated[int, Field(description="자유 게시판 게시물 번호")]
    Views: Annotated[int, Field(description="자유 게시판 게시물 조회수")]
