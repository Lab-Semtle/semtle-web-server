from typing import Optional, Annotated, List
from datetime import datetime, timezone
from fastapi import Depends, Form, Path, Query
from pydantic import Field, EmailStr
from enum import Enum
from src.lib.dto import BaseDTO


class InfoUserRole(str, Enum):
    admin = "admin"
    member = "member"

class InfoUserGrade(str, Enum):
    Aplus = "Aplus"
    A = "A"
    Bplus = "Bplus"
    B = "B"
    F = "F"
    

class UserBase(BaseDTO):
    ''' 공통 필드를 가진 기본 유저 정보 클래스 정의 '''
    
    user_email: EmailStr = Field(..., description="유저 이메일")
    user_name: Optional[str] = Field(None, description="유저 이름")
    user_nickname: Optional[str] = Field(None, description="유저 닉네임")
    user_phone: Optional[str] = Field(None, description="유저 전화번호")
    user_birth: Optional[str] = Field(None, description="유저 생년월일")
    user_profile_img_path: Optional[str] = Field(None, description="유저 프로필 이미지 경로")
    user_introduce: Optional[str] = Field(None, description="유저 소개")
    user_create_date: Optional[datetime] = Field(None, description="유저 생성 날짜")
    user_role: Optional[InfoUserRole] = Field(None, description="유저 역할")
    grade_id: Optional[int] = Field(None, description="유저 등급 ID")
    user_activate: Optional[bool] = Field(None, description="유저 활성화 상태")


class ReadUserInfo(UserBase):
    ''' 관리자 페이지에서 유저 정보를 읽기 위한 DTO '''
    pass


class ReadFilterUser(BaseDTO):
    ''' 유저 조회 필터 조건 DTO '''
    role: Optional[InfoUserRole] = Field(None, description="유저 권한")
    grade: Optional[InfoUserGrade] = Field(None, description="유저 등급")
