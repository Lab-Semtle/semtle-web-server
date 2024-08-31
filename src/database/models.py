"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class Grade(Base):
    ''' 유저 등급 정보 테이블 '''
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, index=True)     # 등급 식별자
    grade_grade = Column(String(5), unique=True, nullable=False) # 등급 이름
    grade_desc = Column(Text, nullable=True)                     # 등급 권한 설명
    
    user = relationship("User", back_populates="grade")

class User(Base):
    ''' 유저 테이블 (매니저,일반회원 포함) '''
    __tablename__ = "users"
    
    user_id = Column(String(128), primary_key=True, index=True)       # 유저 아이디(이메일)
    user_password = Column(String(128), nullable=False)               # 유저 비밀번호
    user_name = Column(String(30), unique=True, nullable=False)       # 유저 이름
    user_email = Column(String(30), nullable=False)                   #유저 이메일
    user_phone = Column(String(11), nullable=False)                   # 유저 전화번호
    user_birth = Column(String(6), nullable=True)                     # 유저 생년월일
    create_date = Column(DateTime(timezone=False), default=datetime.now) # 학회 가입 일자
