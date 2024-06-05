"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from var.session import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True)
    user_password = Column(String(128), nullable=False)  # null 값 허용안함
    user_name = Column(String(30), unique=True, nullable=False)
    user_email = Column(String(30), nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_birth = Column(Integer, nullable=True)
    create_date = Column(DateTime(timezone=True))

class Star(Base):
    __tablename__ = "star"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)
    count_star = Column(Integer, nullable = False)
    course_comment = Column(String(300), nullable=False)
    count_like = Column(Integer, nullable=True, default=0)

class Professor(Base):
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    professor = Column(String, nullable=False)
    course = Column(String, nullable=False)