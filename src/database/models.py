"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, LargeBinary, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_email = Column(String(30), primary_key=True, index=True)
    user_password = Column(String(128), nullable=False)
    user_name = Column(String(15), unique=False, nullable=False)
    user_nickname = Column(String(15), nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_birth = Column(Date, nullable=True)
    create_date = Column(DateTime(timezone=True), default=datetime.now)
    user_profile_img_path = Column(Text, nullable=True)
    user_introduce = Column(Text, nullable=True)
    user_role = Column(String(30), default="학생", nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    user_activate = Column(Boolean, default=False, nullable=False)    
    data = Column(String, nullable=True)
    grade = relationship("Grade", back_populates="user")

class Grade(Base):
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, index=True)
    grade_grade = Column(String(5), unique=True, nullable=False)
    grade_desc = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="grade")