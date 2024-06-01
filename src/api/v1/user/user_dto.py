from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import Field, EmailStr, validator
from src.var.dto import BaseDTO

# 유저 정보를 읽기 위한 DTO
class ReadUserInfo(BaseDTO):
    user_id: Annotated[str, Form(description="유저 아이디")]
    user_name: Annotated[Optional[str], Form(description="유저 이름")]
    user_email: Annotated[Optional[str], Form(description="유저 이메일")]
    user_phone: Annotated[Optional[str], Form(description="유저 전화번호")]
    user_birth: Annotated[Optional[int], Form(description="유저 생년월일")]

# 유저 정보를 업데이트하기 위한 DTO
class UpdateUserInfo(BaseDTO):
    user_id: Annotated[str, Form(description="유저 아이디")]
    user_password: Annotated[str, Form(description="유저 비밀번호")]
    user_password: Annotated[Optional[str], Form(description="유저 신규 비밀번호")]
    # user_confirm_password: Annotated[str | None, Form(description="유저 신규 비밀번호 확인")]         
    # ^^^ 위 필드는 '알 수 없는 열'이라는 오류를 발생시키므로 주석 처리되었습니다.
    user_name: Annotated[str, Form(description="유저 이름")]
    user_email: Annotated[str, Form(description="유저 이메일")]
    user_phone: Annotated[str, Form(description="유저 전화번호")]
    user_birth: Annotated[int, Form(description="유저 생년월일")]