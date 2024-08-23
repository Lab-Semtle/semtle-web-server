"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
import os
import secrets
from fastapi import UploadFile
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import Optional

from src.api.v1.exam_sharing_board_comment import exam_sharing_board_comment_dao
from src.api.v1.exam_sharing_board.exam_sharing_board_dto import ReadBoard, ReadBoardlist
from src.var.models import Exam_Sharing_Board

BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/exam_sharing_board/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/exam_sharing_board/')


# Read list
async def get_exam_sharing_board_list(db: AsyncSession, skip: int = 0) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Board_no.desc()).offset(skip*10).limit(10))
    exam_sharing_board_info = result.scalars().all()
    total = await db.execute(select(func.count(Exam_Sharing_Board.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_info


# Read
async def get_exam_sharing_board(db: AsyncSession, exam_sharing_board_no: int) -> ReadBoard:
    result = await db.execute(select(Exam_Sharing_Board).filter(Exam_Sharing_Board.Board_no == exam_sharing_board_no))
    exam_sharing_board_info = result.scalars().first()
    return exam_sharing_board_info


# Create
async def create_exam_sharing_board(title: str, content: str, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    create_values = {
        "Title": title,
        "Content": content,
        "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
        "Views" : 0
    }
    image_paths=[]
    if file_name:
        for file in file_name:
            currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
            original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
            saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
            file_location = os.path.join(STATIC_DIR, saved_file_name)
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            image_paths.append(saved_file_name)
    if image_paths:
        create_values["Image_paths"] = ",".join(image_paths)
    await db.execute(insert(Exam_Sharing_Board).values(create_values))
    await db.commit()
    
    
# Update
async def update_exam_sharing_board(exam_sharing_board_no: int, title: str, content: str, file_name: list[UploadFile], db: AsyncSession) -> None:
    create_values = {
        "Title": title,
        "Content": content,
        "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
        "Views" : 0
    }
    image_paths=[]
    for file in file_name:
        currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
        original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
        saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
        file_location = os.path.join(STATIC_DIR, saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        image_paths.append(saved_file_name)
    create_values["Image_paths"] = ",".join(image_paths)
    await db.execute(update(Exam_Sharing_Board).filter(Exam_Sharing_Board.Board_no == exam_sharing_board_no).values(create_values))
    await db.commit()
    

# Delete
async def delete_exam_sharing_board(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await delete_image_exam_sharing_board(exam_sharing_board_no, db)
    await exam_sharing_board_comment_dao.all_delete_exam_sharing_board_comment(exam_sharing_board_no, db)
    await db.execute(delete(Exam_Sharing_Board).filter(Exam_Sharing_Board.Board_no == exam_sharing_board_no))
    await db.commit()


# Delte Image
async def delete_image_exam_sharing_board(exam_sharing_board_no: int, db: AsyncSession) -> None:
    result = await db.execute(select(Exam_Sharing_Board.Image_paths).filter(Exam_Sharing_Board.Board_no == exam_sharing_board_no))
    image_paths = result.scalar_one_or_none()
    if image_paths:
        image_paths = image_paths.split(',')
        for image_path in image_paths:
            full_path = os.path.join(STATIC_DIR, image_path.strip())
            os.remove(full_path)


#sort
async def sort_exam_sharing_board(db: AsyncSession, skip: int = 0, sel: int = 0) -> tuple[int, list[ReadBoardlist]]:
    if sel == 0:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Board_no.desc()).offset(skip*10).limit(10))
    elif sel == 1:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Board_no.asc()).offset(skip*10).limit(10))
    elif sel == 2:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Create_date.desc()).offset(skip*10).limit(10))
    elif sel == 3:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Create_date.asc()).offset(skip*10).limit(10))
    elif sel == 4:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Title.asc()).offset(skip*10).limit(10))
    elif sel == 5:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Title.desc()).offset(skip*10).limit(10))
    elif sel == 6:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Views.desc()).offset(skip*10).limit(10))
    elif sel == 7:
        result = await db.execute(select(Exam_Sharing_Board).order_by(Exam_Sharing_Board.Views.asc()).offset(skip*10).limit(10))
    exam_sharing_board_info = result.scalars().all()
    total = await db.execute(select(func.count(Exam_Sharing_Board.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_info



