"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


'''
회원 관련
'''
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
    # user_nickname = Column(String(30), unique=True, nullable=False) # 유저 활동 닉네임
    user_phone = Column(String(11), nullable=False)                   # 유저 전화번호
    user_birth = Column(String(6), nullable=True)                     # 유저 생년월일
    # user_profile_img_path = Column(Text, nullable=True)             # 프로필 이미지 경로
    create_date = Column(DateTime(timezone=False), default=datetime.now) # 학회 가입 일자
    user_role = Column(String(30), nullable=False)                       # 매니저-일반 구분
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))            # 등급 식별자
    user_activate = Column(Boolean, default=False, nullable=False)       # 아치셈틀 인증 여부
    
    grade = relationship("Grade", back_populates="user")


'''
게시판 관련
'''
class Free_Board(Base):
    ''' 자유 게시판 게시물 테이블 '''
    __tablename__ = "Free_Board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True) 
    title = Column(String, nullable=False)                           
    content = Column(String, nullable=False)                         
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False) 
    views = Column(Integer, nullable=False)                          

    free_board_comment = relationship("Free_Board_Comment", back_populates="Free_Board", cascade="all, delete-orphan")

class Free_Board_Comment(Base):
    ''' 자유 게시판 댓글 테이블 '''
    __tablename__ = "Free_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True) 
    Board_no = Column(Integer, ForeignKey("Free_Board.Board_no"))      
    Content = Column(String, nullable=False)                           
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False) 
    Likes = Column(Integer, nullable=False)

    Free_Board = relationship("Free_Board", back_populates="Free_Board_Comment")

class Study_Board(Base):
    ''' 스터디 게시판 게시물 테이블 '''
    __tablename__ = "Study_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Views = Column(Integer, nullable=False)

    Study_Board_Comment = relationship("Study_Board_Comment", back_populates="Study_Board", cascade="all, delete-orphan")

class Study_Board_Comment(Base):
    ''' 스터디 게시판 댓글 테이블 '''
    __tablename__ = "Study_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Study_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Likes = Column(Integer, nullable=False)

    Study_Board = relationship("Study_Board", back_populates="Study_Board_Comment")

class Exam_Sharing_Board(Base):
    ''' 족보 게시판 게시물 테이블 '''
    __tablename__ = "Exam_Sharing_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Views = Column(Integer, nullable=False)

    Exam_Sharing_Board_Comment = relationship("Exam_Sharing_Board_Comment", back_populates="Exam_Sharing_Board", cascade="all, delete-orphan")

class Exam_Sharing_Board_Comment(Base):
    ''' 족보 게시판 댓글 테이블 '''
    __tablename__ = "Exam_Sharing_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Exam_Sharing_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Image_paths = Column(String, nullable=True)
    Likes = Column(Integer, nullable=False)

    Exam_Sharing_Board = relationship("Exam_Sharing_Board", back_populates="Exam_Sharing_Board_Comment")

class Star(Base):
    '''  '''
    __tablename__ = "star"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)
    count_star = Column(Integer, nullable = False)
    course_comment = Column(String(300), nullable=False)
    count_like = Column(Integer, nullable=True, default=0)
    
class Professor(Base):
    ''' 교수님 정보 테이블 '''
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    professor = Column(String, nullable=False)
    course = Column(String, nullable=False)

class FileRecord(Base):
    '''  '''
    __tablename__ = 'file_records'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(LargeBinary)