"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, LargeBinary, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

'''
회원
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
    __tablename__ = "user"
    
    user_id = Column(String(128), primary_key=True)                   # 유저 아이디(이메일)
    user_password = Column(String(128), nullable=False)               # 유저 비밀번호
    user_name = Column(String(30), unique=True, nullable=False)       # 유저 이름
    user_email = Column(String(30), nullable=False)                   #유저 이메일
    user_phone = Column(String(30), nullable=False)                   # 유저 전화번호
    user_birth = Column(Date, nullable=True)                     # 유저 생년월일
    create_date = Column(DateTime(timezone=True), default=datetime.now) # 학회 가입 일자
    
    # user_profile_img_path = Column(Text, nullable=True)             # 프로필 이미지 경로
    # user_nickname = Column(String(30), unique=True, nullable=False) # 유저 활동 닉네임
    # user_role = Column(String(30), nullable=False)                       # 매니저-일반 구분
    # grade_id = Column(Integer, ForeignKey("grades.grade_id"))            # 등급 식별자
    # user_activate = Column(Boolean, default=False, nullable=False)       # 아치셈틀 인증 여부
    
    # grade = relationship("Grade", back_populates="user")
 
'''
게시판
'''
class Star(Base):
    """ 별점 """
    __tablename__ = "star"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    course_id = Column(Integer, nullable=False)
    count_star = Column(Integer, nullable = False)
    course_comment = Column(String(300), nullable=False)
    count_like = Column(Integer, nullable=True, default=0)
    
class FreeBoard(Base):
    """ 자유 게시판 콘텐츠 """
    __tablename__ = "free_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    views = Column(Integer, nullable=False)

    free_comment = relationship("free_comment", back_populates="free_board", cascade="all, delete-orphan")

class FreeComment(Base):
    """ 자유 게시판 댓글 """
    __tablename__ = "free_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("free_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    likes = Column(Integer, nullable=False)

    free_board = relationship("free_board", back_populates="free_comment")

class StudyBoard(Base):
    """ 스터디 모집 게시판 콘텐츠 """
    __tablename__ = "study_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    views = Column(Integer, nullable=False)

    study_comment = relationship("study_comment", back_populates="study_board", cascade="all, delete-orphan")

class StudyComment(Base):
    """ 스터디 모집 게시판 댓글 """
    __tablename__ = "study_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("study_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    likes = Column(Integer, nullable=False)

    study_board = relationship("study_board", back_populates="study_comment")

class ExamBoard(Base):
    """ 족보 공유 게시판 콘텐츠 """
    __tablename__ = "exam_board"
    
    board_no = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    views = Column(Integer, nullable=False)

    exam_comment = relationship("exam_comment", back_populates="exam_board", cascade="all, delete-orphan")

class ExamComment(Base):
    """ 족보 공유 게시판 댓글 """
    __tablename__ = "exam_comment"

    comment_no = Column(Integer, primary_key=True, autoincrement=True)
    board_no = Column(Integer, ForeignKey("exam_board.board_no"))
    content = Column(String, nullable=False)
    create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    image_paths = Column(String, nullable=True)
    likes = Column(Integer, nullable=False)

    exam_board = relationship("exam_board", back_populates="exam_comment")

class Professor(Base):
    """ 교수님 정보 """
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    professor = Column(String, nullable=False)
    course = Column(String, nullable=False)

class File(Base):
    """ 파일 """
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(LargeBinary)