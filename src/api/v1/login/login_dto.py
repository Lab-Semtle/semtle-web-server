from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import Field, EmailStr, validator
from var.dto import BaseDTO

from fastapi import HTTPException

class CreateUserInfo(BaseDTO):
    user_id: Annotated[str, Field(description="유저 아이디")]
    user_password: Annotated[str, Field(description="유저 비밀번호")]
    user_name: Annotated[str, Field(description="유저 이름")]
    user_email: Annotated[EmailStr, Field(description="유저 이메일")]
    user_phone: Annotated[str, Field(description="유저 전화번호")]
    user_birth: Annotated[int, Field(description="유저 생년월일")]
    create_date: Annotated[datetime, Depends(lambda: datetime.now(timezone.utc))] = Field(default_factory=lambda: datetime.now(timezone.utc), description="가입 일자")
    
    @validator('user_email', 'user_name', 'user_phone', 'user_password')
    def check_empty(cls, v):
        if not v or v. isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return v
    @validator ('user_phone')
    def check_phone(cls, v):
        phone = v
        if '-' not in v or len (phone) != 13:
            raise HTTPException(status_code=422, detail="올바른 형식의 번호를 입력해주세요. ")
        return phone
    @validator ('user_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요. ")
        if not any(char.isdigit() for char in v):
            raise HTTPException(status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요. ")
        if not any(char.isalpha() for char in v): 
            raise HTTPException (status_code=422, detail="비밀번호는 8자리 이상 영문과 숫자를 포함하여 작성해 주세요. ")
        return v