"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated, List
from datetime import datetime
from fastapi import Form
from pydantic import Field, validator
from src.var.dto import BaseDTO



# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)

class ReadBoard(BaseDTO):
    Board_no: Annotated[int, Field(description="스터디 게시판 게시물 번호")]
    Title: Annotated[str, Form(description="스터디 게시판 게시물 제목")]
    Content: Annotated[Optional[str] | None, Form(description="스터디 게시판 게시물 내용")]
    Create_date: Annotated[datetime, Field(description="스터디 게시판 게시물 작성 일자")] = Field(
        default_factory=lambda: datetime.now().replace(second=0, microsecond=0).replace(tzinfo=None), description="스터디 게시판 게시물 작성 일자")
    Image_paths : Annotated[Optional[list[str]], Form(description="스터디 게시판 게시물 이미지 파일 다중 경로")]
    Views: Annotated[int, Field(description="스터디 게시판 게시물 조회수")]

    @validator('Image_paths', pre=True)
    def split_image_paths(cls, v):
        if isinstance(v, str):
            # 콤마로 구분된 문자열을 리스트로 변환
            return v.split(',')
        return v
    
    class Config:
        from_attributes = True

class UpdateBoard(BaseDTO):
    Title: Annotated[str, Form(description="스터디 게시판 게시물 제목")]
    Content: Annotated[Optional[str] | None, Form(description="스터디 게시판 게시물 내용")]

class CreateBoard(UpdateBoard):
    Views: Annotated[int, Field(description="스터디 게시판 게시물 조회수")]

class ReadBoardlist(BaseDTO):
    total: Annotated[int, Form(description="스터디 게시판 전체 게시물 갯수")] = 0
    Board_info: Annotated[List[ReadBoard], Form(description="게시물 데이터")] = []

    class Config:
        from_attributes = True