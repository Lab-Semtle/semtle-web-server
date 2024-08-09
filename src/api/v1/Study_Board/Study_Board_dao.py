"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
import os
import secrets
from fastapi import Depends, UploadFile, File
from sqlalchemy import Result, ScalarResult, select, update, insert, delete, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload, query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.api.v1.Study_Board.Study_Board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.var.models import Study_Board
from src.var.session import get_db

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')


# Read List
async def get_Study_Board_List(db: AsyncSession, skip: int = 0) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(Study_Board).order_by(Study_Board.Board_no.desc()).offset(skip*10).limit(10))
    Board_info = result.scalars().all()
    total = await db.execute(select(func.count(Study_Board.Board_no)))
    total = total.scalar()
    return total, Board_info

# Read
async def get_Study_Board(db: AsyncSession, Board_no: int) -> ReadBoard:
    result = await db.execute(select(Study_Board).filter(Study_Board.Board_no == Board_no))
    Board_info = result.scalars().first()
    return Board_info

# Create
async def create_Study_Board(Title: str, Content: str, File_name: list[UploadFile], db: AsyncSession):
    create_values = {
        "Title": Title,
        "Content": Content,
        "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
        "Views" : 0
    }
    Image_paths=[]
    for file in File_name:
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
        saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
        file_location = os.path.join(IMG_DIR, saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        Image_paths.append(saved_file_name)
    create_values["Image_paths"] = ",".join(Image_paths)
    await db.execute(insert(Study_Board).values(create_values))
    await db.commit()
    
    
# Update
async def update_Study_Board(Board_no: int, Title: str, Content: str, File_name: list[UploadFile], db: AsyncSession) -> None:
    create_values = {
        "Title": Title,
        "Content": Content,
        "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
        "Views" : 0
    }
    Image_paths=[]
    for file in File_name:
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
        saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
        file_location = os.path.join(IMG_DIR, saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        Image_paths.append(saved_file_name)
    create_values["Image_paths"] = ",".join(Image_paths)
    await db.execute(update(Study_Board).filter(Study_Board.Board_no == Board_no).values(create_values))
    await db.commit()
    

# Delete
async def delete_Study_Board(Board_no: int, db: AsyncSession) -> None:
    delete_Image_Study_Board(Board_no, db)
    await db.execute(delete(Study_Board).filter(Study_Board.Board_no == Board_no))
    await db.commit()

# Delte Image
async def delete_Image_Study_Board(Board_no: int, db: AsyncSession) -> None:
    result = await db.execute(select(Study_Board.Image_paths).filter(Study_Board.Board_no == Board_no))
    image_paths = result.scalar_one_or_none()
    image_paths = image_paths.split(',')
    for image_path in image_paths:
        full_path = os.path.join(IMG_DIR, image_path.strip())
        os.remove(full_path)

#sort
async def sort_Study_Board(db: AsyncSession, skip: int = 0, sel: int = 0) -> tuple[int, list[ReadBoardlist]]:
    if sel == 0:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Board_no.desc()).offset(skip*10).limit(10))
    elif sel == 1:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Board_no.asc()).offset(skip*10).limit(10))
    elif sel == 2:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Create_date.desc()).offset(skip*10).limit(10))
    elif sel == 3:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Create_date.asc()).offset(skip*10).limit(10))
    elif sel == 4:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Title.asc()).offset(skip*10).limit(10))
    elif sel == 5:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Title.desc()).offset(skip*10).limit(10))
    elif sel == 6:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Views.desc()).offset(skip*10).limit(10))
    elif sel == 7:
        result = await db.execute(select(Study_Board).order_by(Study_Board.Views.asc()).offset(skip*10).limit(10))
    Board_info = result.scalars().all()
    Total = await db.execute(select(func.count(Study_Board.Board_no)))
    Total = Total.scalar()
    return Total, Board_info



