"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
import os
import secrets
from datetime import datetime, timezone
from typing import Optional
from fastapi import UploadFile
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.board_exam.exam_dto import ReadBoard, ReadBoardlist, CreateBoard
from src.database.models import ExamBoard
from src.database.session import rdb


BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/exam_sharing_board/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/exam_sharing_board/')

@rdb.dao()
async def get_exam_sharing_board_list(db: AsyncSession, skip: int = 0) -> tuple[int, list[ReadBoardlist]]:
    result = await db.execute(select(ExamBoard).order_by(ExamBoard.Board_no.desc()).offset(skip*10).limit(10))
    exam_sharing_board_info = result.scalars().all()
    total = await db.execute(select(func.count(ExamBoard.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_info

@rdb.dao()
async def get_exam_sharing_board(db: AsyncSession, exam_sharing_board_no: int) -> ReadBoard:
    result = await db.execute(select(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no))
    exam_sharing_board_info = result.scalars().first()
    return exam_sharing_board_info

@rdb.dao(transactional=True)
async def create_exam_sharing_board(Eexam_sharing_board_info: Optional[CreateBoard], db: AsyncSession) -> int:
    create_values = Eexam_sharing_board_info.dict()
    create_values['Create_date'] = datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None)
    result = await db.execute(insert(ExamBoard).values(create_values).returning(ExamBoard.Board_no))
    Eexam_sharing_board_no = result.scalar_one()
    return Eexam_sharing_board_no

@rdb.dao(transactional=True)
async def upload_file_exam_sharing_board(exam_sharing_board_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
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
    
    image_paths = ",".join(image_paths)
    create_values = {"Image_paths": image_paths}
    await db.execute(update(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no).values(create_values))

@rdb.dao(transactional=True)
async def update_exam_sharing_board(exam_sharing_board_no: int, exam_sharing_board_info: Optional[CreateBoard], db: AsyncSession):
    await db.execute(update(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no).values(exam_sharing_board_info.dict()))

@rdb.dao(transactional=True)
async def upload_file_add_exam_sharing_board(exam_sharing_board_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    result = await db.execute(select(ExamBoard.Image_paths).filter(ExamBoard.Board_no == exam_sharing_board_no))
    image_paths = result.scalar_one_or_none()  

    if image_paths is None:
        image_paths = []
    else:
        image_paths = image_paths.split(",")
        
    if file_name:
        for file in file_name:
            currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
            original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
            saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
            file_location = os.path.join(STATIC_DIR, saved_file_name)
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            image_paths.append(saved_file_name)
    
    image_paths = ",".join(image_paths)
    create_values = {"Image_paths": image_paths}
    await db.execute(update(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no).values(create_values))

@rdb.dao(transactional=True)
async def delete_exam_sharing_board(exam_sharing_board_no: int, db: AsyncSession) -> None:
    await db.execute(delete(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no))

@rdb.dao(transactional=True)
async def delete_file_exam_sharing_board(exam_sharing_board_no: int, db: AsyncSession) -> None:
    result = await db.execute(select(ExamBoard.Image_paths).filter(ExamBoard.Board_no == exam_sharing_board_no))
    image_paths = result.scalar_one_or_none()
    if image_paths:
        image_paths = image_paths.split(',')
        for image_path in image_paths:
            full_path = os.path.join(STATIC_DIR, image_path.strip())
            os.remove(full_path)
    await db.execute(update(ExamBoard).filter(ExamBoard.Board_no == exam_sharing_board_no).values(Image_paths=""))

@rdb.dao()
async def sort_exam_sharing_board(db: AsyncSession, skip: int = 0, sel: int = 0) -> tuple[int, list[ReadBoardlist]]:
    if sel == 0:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Board_no.desc()).offset(skip*10).limit(10))
    elif sel == 1:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Board_no.asc()).offset(skip*10).limit(10))
    elif sel == 2:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Create_date.desc()).offset(skip*10).limit(10))
    elif sel == 3:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Create_date.asc()).offset(skip*10).limit(10))
    elif sel == 4:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Title.asc()).offset(skip*10).limit(10))
    elif sel == 5:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Title.desc()).offset(skip*10).limit(10))
    elif sel == 6:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Views.desc()).offset(skip*10).limit(10))
    elif sel == 7:
        result = await db.execute(select(ExamBoard).order_by(ExamBoard.Views.asc()).offset(skip*10).limit(10))
    exam_sharing_board_info = result.scalars().all()
    total = await db.execute(select(func.count(ExamBoard.Board_no)))
    total = total.scalar()
    return total, exam_sharing_board_info
