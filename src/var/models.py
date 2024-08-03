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
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String(128), primary_key=True, index=True)
    user_password = Column(String(128), nullable=False)
    user_name = Column(String(30), unique=True, nullable=False)
    user_email = Column(String(30), nullable=False)
    user_phone = Column(String(11), nullable=False)
    user_birth = Column(String(6), nullable=True)
    create_date = Column(DateTime(timezone=False), default=datetime.now)
    
    user_nickname = Column(String(30), unique=True, nullable=False)
    user_profile_img_path = Column(Text, nullable=True)
    user_introduce = Column(Text, nullable=True)
    user_role = Column(String(30), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    user_activate = Column(Boolean, default=False, nullable=False)    
    
    grade = relationship("Grade", back_populates="user")

# class User(Base):
#     __tablename__ = "user"

#     user_id = Column(String, primary_key=True)
#     user_password = Column(String(128), nullable=False)  # null 값 허용안함
#     user_name = Column(String(30), unique=True, nullable=False)
#     user_email = Column(String(30), nullable=False)
#     user_phone = Column(String(15), nullable=False)
#     user_birth = Column(Integer, nullable=True)
#     create_date = Column(DateTime(timezone=True))


class Grade(Base):
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, index=True)
    grade_grade = Column(String(5), unique=True, nullable=False)
    grade_desc = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="grade")
    

'''
게시판 관련
'''
class Free_Board(Base):
    __tablename__ = "Free_Board"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Views = Column(Integer, nullable=False)

    Comment = relationship("Free_Board_Comment", back_populates="Board")


class Free_Board_Comment(Base):
    __tablename__ = "Free_Board_Comment"

    Comment_no = Column(Integer, primary_key=True, autoincrement=True)
    Board_no = Column(Integer, ForeignKey("Free_Board.Board_no"))
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0), nullable=False)
    Views = Column(Integer, nullable=False)

    Board = relationship("Free_Board", back_populates="Comment")


#################################
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


class FileRecord(Base):
    __tablename__ = 'file_records'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(LargeBinary)