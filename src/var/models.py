"""
데이터베이스 테이블에 매핑될 모델 정의(ORM Model)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Example(Base):
    __tablename__ = "example"

    example_id = Column(String, primary_key=True)
    example_name = Column(Text, nullable=True)
    example_comm1 = Column(Text, nullable=True)
    example_comm2 = Column(Text, nullable=True)

class User(Base):
    __tablename__ = "users"
    
    user_email = Column(String(128), primary_key=True)
    user_password = Column(String(128), nullable=False)  # null 값 허용안함
    user_name = Column(String(30), unique=True, nullable=False)
    user_nickname = Column(String(30), unique=True, nullable=False)
    user_phone = Column(String(15), nullable=False)
    user_birth = Column(Integer, nullable=True)
    create_date = Column(DateTime(timezone=True))
    # is_active = Column(Boolean, default=False)



# Role

# User-Role