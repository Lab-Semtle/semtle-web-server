"""
API 개발 시 참고 : API 호출 시 데이터 전달 양식 정의
"""
# 기본적으로 추가
from typing import Optional, Annotated
from datetime import datetime, timezone
from fastapi import Depends, Form, Path
from pydantic import Field
from src.var.dto import BaseDTO


# - 개발하려는 API의 목적에 맞게 클래스 작성
# - 중복되는 부분은 상속받아서 중복 코드 최소화하기
# - src/var/model.py에 데이터베이스에 생성하고자하는 테이블 먼저 선언 후, 해당 클래스 참고하여 dto를 작성하면 편함
# - 데이터 전달 객체를 사용하는 API의 목적에 따라서 클래스명 작성
#   1) Read, Create, Update, Delete 중 1택
#   2) 목적에 따라 클래스명 원하는 대로 선언(컨벤션에 맞춰 작성할 것, 대소문자 유의)

class keyExample(BaseDTO):
    example_id: Annotated[str | None, Form(description="예제 id")]


class UpdateExample(BaseDTO):
    example_name: Annotated[str | None, Form(description="예제 이름")] = 'test1'
    example_comm1: Annotated[str | None, Form(description="예제 내용1_Form")] = 'sample1'
    example_comm2: Annotated[str | None, Field(description="예제 내용2_Field")] = 'sample2'


class CreateExample(keyExample, UpdateExample):
    ...

class ReadExampleInfo(CreateExample):
    ...