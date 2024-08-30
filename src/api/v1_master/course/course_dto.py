from datetime import datetime, timezone
from typing import Optional, Annotated
from fastapi import Depends, Form, Path
from var.dto import BaseDTO
from pydantic import Field

class CourseGrade(BaseDTO):
    user_email: str = Field(description="유저 아이디")
    count_star: int = Field(description="별점")
    course_comment: str = Field(description="강의평")