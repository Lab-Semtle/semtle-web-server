"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from src.var.session import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True)
    user_password = Column(String(128), nullable=False)  # null 값 허용안함
    user_name = Column(String(30), unique=True, nullable=False)
    user_email = Column(String(30), nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_birth = Column(Integer, nullable=True)
    create_date = Column(DateTime(timezone=True))

class Free_Board(Base):
    __tablename__ = "Free_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Views = Column(Integer, nullable=False)

    Free_Board_Comment = relationship("Free_Board_Comment", back_populates="Free_Board", cascade="all, delete-orphan")

class Free_Board_Comment(Base):
    __tablename__ = "Free_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Free_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Likes = Column(Integer, nullable=False)

    Free_Board = relationship("Free_Board", back_populates="Free_Board_Comment")

class Study_Board(Base):
    __tablename__ = "Study_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Views = Column(Integer, nullable=False)

    Study_Board_Comment = relationship("Study_Board_Comment", back_populates="Study_Board", cascade="all, delete-orphan")

class Study_Board_Comment(Base):
    __tablename__ = "Study_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Study_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Likes = Column(Integer, nullable=False)

    Study_Board = relationship("Study_Board", back_populates="Study_Board_Comment")

class Exam_Sharing_Board(Base):
    __tablename__ = "Exam_Sharing_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Views = Column(Integer, nullable=False)

    Exam_Sharing_Board_Comment = relationship("Exam_Sharing_Board_Comment", back_populates="Exam_Sharing_Board", cascade="all, delete-orphan")

class Exam_Sharing_Board_Comment(Base):
    __tablename__ = "Exam_Sharing_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Exam_Sharing_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Likes = Column(Integer, nullable=False)

    Exam_Sharing_Board = relationship("Exam_Sharing_Board", back_populates="Exam_Sharing_Board_Comment")

