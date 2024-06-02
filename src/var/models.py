"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


'''
회원 관련
'''
class User(Base):
    __tablename__ = "users"
    
    user_email = Column(String(128), primary_key=True, index=True)
    user_password = Column(String(128), nullable=False)
    user_name = Column(String(30), unique=True, nullable=False)
    user_nickname = Column(String(30), unique=True, nullable=False)
    user_phone = Column(String(11), nullable=False)
    user_birth = Column(String(6), nullable=True)
    user_profile_img_path = Column(Text, nullable=True)
    user_introduce = Column(Text, nullable=True)
    user_create_date = Column(DateTime(timezone=False), default=datetime.now)
    user_role = Column(String(30), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.grade_id"))
    user_activate = Column(Boolean, default=False, nullable=False)    
    
    grade = relationship("Grade", back_populates="user")


class Grade(Base):
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, index=True)
    grade_grade = Column(String(5), unique=True, nullable=False)
    grade_desc = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="grade")
    

'''
게시판 관련
'''
class BoardFree(Base):
    __tablename__ = "board_free"
    
    Board_no = Column(Integer, primary_key=True, autoincrement=True)
    Title = Column(String, nullable=False)
    Content = Column(String, nullable=False)
    Create_date = Column(DateTime(timezone=True))
    Views = Column(Integer, nullable=False)

# class Board(Base):
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True, index=True)
#     board_type = Column(String, nullable=False)  # 게시판 유형
#     title = Column(String, nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(TIMESTAMP, nullable=False)
#     updated_at = Column(TIMESTAMP, nullable=True)
#     author_id = Column(Integer, ForeignKey("users.id"))
#     likes = Column(Integer, default=0)
#     views = Column(Integer, default=0)

#     author = relationship("User")


# class Comment(Base):
#     __tablename__ = "comments"
#     id = Column(Integer, primary_key=True, index=True)
#     post_id = Column(Integer, ForeignKey("posts.id"))
#     author_id = Column(Integer, ForeignKey("users.id"))
#     content = Column(Text, nullable=False)
#     created_at = Column(TIMESTAMP, nullable=False)

#     post = relationship("Post")
#     author = relationship("User")


# class Tag(Base):
#     __tablename__ = "tags"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, nullable=False)


# class BoardTag(Base):
#     __tablename__ = "post_tags"
#     post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
#     tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


# class LectureRating(Base):
#     __tablename__ = "lecture_ratings"
#     id = Column(Integer, primary_key=True, index=True)
#     post_id = Column(Integer, ForeignKey("posts.id"))
#     rating = Column(Integer, nullable=False)
#     author_id = Column(Integer, ForeignKey("users.id"))

#     post = relationship("Post")
#     author = relationship("User")


'''
활동 관리
'''
# class Event(Base):
#     __tablename__ = "events"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     start_date = Column(TIMESTAMP, nullable=False)
#     end_date = Column(TIMESTAMP, nullable=True)
#     created_at = Column(TIMESTAMP, nullable=False)

# class EventParticipant(Base):
#     __tablename__ = "event_participants"
#     id = Column(Integer, primary_key=True, index=True)
#     event_id = Column(Integer, ForeignKey("events.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     status = Column(String, nullable=True)

#     event = relationship("Event")
#     user = relationship("User")


'''
설문 조사, 투표 기능
'''
# class Poll(Base):
#     __tablename__ = "polls"
#     id = Column(Integer, primary_key=True, index=True)
#     question = Column(Text, nullable=False)
#     created_at = Column(TIMESTAMP, nullable=False)

# class PollOption(Base):
#     __tablename__ = "poll_options"
#     id = Column(Integer, primary_key=True, index=True)
#     poll_id = Column(Integer, ForeignKey("polls.id"))
#     option_text = Column(Text, nullable=False)

#     poll = relationship("Poll")

# class PollVote(Base):
#     __tablename__ = "poll_votes"
#     id = Column(Integer, primary_key=True, index=True)
#     poll_id = Column(Integer, ForeignKey("polls.id"))
#     option_id = Column(Integer, ForeignKey("poll_options.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))

#     poll = relationship("Poll")
#     option = relationship("PollOption")
#     user = relationship("User")
