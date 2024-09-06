"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True)
    user_password = Column(String(128), nullable=False)  # null 값 허용안함
    user_name = Column(String(30), unique=True, nullable=False)
    user_email = Column(String(30), nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_birth = Column(Integer, nullable=True)
    create_date = Column(DateTime(timezone=True))

class FreeBoard(Base):
    """ 자유 게시판 콘텐츠 """
    __tablename__ = "free_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    views = Column(Integer, nullable=False)

    free_comment = relationship("FreeComment", back_populates="free_board", cascade="all, delete-orphan")

class FreeComment(Base):
    """ 자유 게시판 댓글 """
    __tablename__ = "free_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("free_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    likes = Column(Integer, nullable=False)

    free_board = relationship("FreeBoard", back_populates="free_comment")

class StudyBoard(Base):
    """ 스터디 모집 게시판 콘텐츠 """
    __tablename__ = "study_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    views = Column(Integer, nullable=False)

    study_comment = relationship("StudyComment", back_populates="study_board", cascade="all, delete-orphan")

class StudyComment(Base):
    """ 스터디 모집 게시판 댓글 """
    __tablename__ = "study_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("study_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    likes = Column(Integer, nullable=False)

    study_board = relationship("StudyBoard", back_populates="study_comment")

class ExamBoard(Base):
    """ 족보 공유 게시판 콘텐츠 """
    __tablename__ = "exam_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    views = Column(Integer, nullable=False)

    exam_comment = relationship("ExamComment", back_populates="exam_board", cascade="all, delete-orphan")

class ExamComment(Base):
    """ 족보 공유 게시판 댓글 """
    __tablename__ = "exam_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("exam_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    likes = Column(Integer, nullable=False)

    exam_board = relationship("ExamBoard", back_populates="exam_comment")

