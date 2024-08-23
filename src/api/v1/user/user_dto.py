from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path, HTTPException
from pydantic import EmailStr, validator
from src.lib.dto import BaseDTO

# 유저 정보를 읽기 위한 DTO
class ReadUserInfo(BaseDTO):
    user_id: Annotated[str, Form(description="유저 아이디")]
    user_name: Annotated[Optional[str], Form(description="유저 이름")]
    user_email: Annotated[Optional[str], Form(description="유저 이메일")]
    user_phone: Annotated[Optional[str], Form(description="유저 전화번호")]
    user_birth: Annotated[Optional[int], Form(description="유저 생년월일")]

# 유저 정보를 업데이트하기 위한 DTO
class UpdateUserInfo(BaseDTO):
    present_user_password: Annotated[str, Form(description="유저 현재 비밀번호")]
    future_user_password: Annotated[str, Form(description="유저 신규 비밀번호")]
    user_name: Annotated[str, Form(description="유저 이름")]
    user_email: Annotated[str, Form(description="유저 이메일")]
    user_phone: Annotated[str, Form(description="유저 전화번호")]
    user_birth: Annotated[int, Form(description="유저 생년월일")]

    # 필수 필드가 빈 문자열이나 공백이 아닌지 확인하는 유효성 검사기
    @validator('user_email', 'user_name', 'user_phone', 'present_user_password','future_user_password')
    def check_empty(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return v
    
    # 전화번호 형식을 확인하는 유효성 검사기
    @validator('user_phone')
    def check_phone(cls, v):
        phone = v
        if '-' not in v or len(phone) != 13:
            raise HTTPException(status_code=422, detail="올바른 형식의 번호를 입력해주세요.")
        return phone
    
    # 비밀번호 유효성을 검사하는 함수
    @validator('present_user_password', 'future_user_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        if not any(char.isdigit() for char in v):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        if not any(char.isalpha() for char in v):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요.")
        return v
