from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from pydantic import Field
from src.var.dto import BaseDTO


class ReadUserInfo(BaseDTO):
    user_name: Annotated[str | None, Form(description="유저 이름")]
    user_email: Annotated[str | None, Form(description="유저 이메일")]
    user_phone: Annotated[str | None, Form(description="유저 전화번호")]
    user_birth: Annotated[int | None, Form(description="유저 생년월일")]


class UpdateUserInfo(BaseDTO):
    user_id: Annotated[str, Form(description="유저 아이디")]
    user_password: Annotated[str, Form(description="유저 비밀번호")]
    user_password: Annotated[str | None, Form(description="유저 신규 비밀번호")]
    user_confirm_password: Annotated[
        str | None, Form(description="유저 신규 비밀번호 확인")
    ]
    user_name: Annotated[str, Form(description="유저 이름")]
    user_email: Annotated[str, Form(description="유저 이메일")]
    user_phone: Annotated[str, Form(description="유저 전화번호")]
    user_birth: Annotated[int, Form(description="유저 생년월일")]


class CreateUserInfo(BaseDTO):
    user_id: Annotated[str, Form(description="유저 아이디")]
    user_password: Annotated[str, Form(description="유저 비밀번호")]
    user_confirm_password: Annotated[str, Form(description="유저 비밀번호 확인")]
    user_name: Annotated[str, Form(description="유저 이름")]
    user_email: Annotated[str, Form(description="유저 이메일")]
    user_phone: Annotated[str, Form(description="유저 전화번호")]
    user_birth: Annotated[int, Form(description="유저 생년월일")]
    create_date: Annotated[datetime, Depends(lambda: datetime.now(timezone.utc))] = Field(
        default_factory=lambda: datetime.now(timezone.utc), description="가입 일자"
    )
