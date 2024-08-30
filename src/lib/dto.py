""" 
애플리케이션의 모든 DTO(데이터 전송 객체)에 대한 기본 설정을 정의
"""
from pydantic import BaseModel


class BaseDTO(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True
