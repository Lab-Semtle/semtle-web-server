"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
# 기본적으로 추가
from typing import Optional
from fastapi import UploadFile
from sqlalchemy import select, update, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import os
import secrets

from src.api.v1_ewha.study_board_comment.study_board_comment_dto import UpdateComment, ReadComment, CreateComment, ReadCommentlist
from src.database.models import Study_Board_Comment
from src.database.session import get_db

BASE_DIR = os.path.dirname('C:/Users/user/Documents/GitHub/Semtle-Web-Server/src/')
STATIC_DIR = os.path.join(BASE_DIR, 'images/study_board_comment/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/', 'images/study_board_comment/')

# Read
async def get_study_board_comment(db: AsyncSession, study_board_no: int, skip: int = 0) -> tuple[int, list[ReadCommentlist]]:
    result = await db.execute(select(Study_Board_Comment).filter(Study_Board_Comment.Board_no == study_board_no).order_by(Study_Board_Comment.Board_no.desc()).offset(skip*10).limit(10))
    comment_info = result.scalars().all()
    total = await db.execute(select(func.count(Study_Board_Comment.Board_no)))
    total = total.scalar()
    return total, comment_info


# Create
async def create_study_board_comment(study_board_no: int, study_board_comment_info: Optional[CreateComment], db: AsyncSession):
    create_values = {
    "Board_no": study_board_no,
    "Content": study_board_comment_info.Content,
    "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
    "Likes": 0  # 예시로 Likes 컬럼이 있다면
    }
    result = await db.execute(insert(Study_Board_Comment).values(create_values).returning(Study_Board_Comment.Board_no))
    await db.commit()
    study_board_comment_no = result.scalar_one()
    return study_board_comment_no


# # Create
# async def upload_create_study_board_comment(study_board_no: int, content: str, file_name: list[UploadFile], db: AsyncSession):
#     create_values = {
#     "Board_no": study_board_no,
#     "Content": content,
#     "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
#     "Likes": 0  # 예시로 Likes 컬럼이 있다면
#     }
#     image_paths=[]
#     for file in file_name:
#         currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
#         original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
#         saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
#         file_location = os.path.join(STATIC_DIR, saved_file_name)
#         with open(file_location, "wb+") as file_object:
#             file_object.write(file.file.read())
#         image_paths.append(saved_file_name)
#     create_values["Image_paths"] = ",".join(image_paths)
#     await db.execute(insert(Study_Board_Comment).values(create_values))
#     await db.commit()


# Create
async def upload_file_study_board_comment(study_board_comment_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
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
    await db.execute(update(Study_Board_Comment).filter(Study_Board_Comment.Comment_no == study_board_comment_no).values(create_values))
    await db.commit()
    

# Update
async def update_study_board_comment(study_board_comment_no: int, study_board_comment_info: Optional[CreateComment], db: AsyncSession):
    await db.execute(update(Study_Board_Comment).filter(Study_Board_Comment.Comment_no == study_board_comment_no).values(study_board_comment_info.dict()))
    await db.commit()


# # Update
# async def upload_update_study_board_comment(study_board_comment_no: int, content: str, file_name: list[UploadFile], db: AsyncSession) -> None:
#     create_values = {
#     "Content": content,
#     "Create_date": datetime.now(timezone.utc).replace(second=0, microsecond=0).replace(tzinfo=None),
#     "Likes": 0  # 예시로 Likes 컬럼이 있다면
#     }
#     image_paths=[]
#     for file in file_name:
#         currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
#         original_extension = os.path.splitext(file.filename)[1]  # 원래 파일의 확장자 추출
#         saved_file_name = f"{currentTime}{secrets.token_hex(16)}{original_extension}"  # 확장자 포함
#         file_location = os.path.join(STATIC_DIR, saved_file_name)
#         with open(file_location, "wb+") as file_object:
#             file_object.write(file.file.read())
#         image_paths.append(saved_file_name)
#     create_values["Image_paths"] = ",".join(image_paths)
#     await db.execute(update(Study_Board_Comment).filter(Study_Board_Comment.Board_no == study_board_no).filter(Study_Board_Comment.Comment_no == study_board_comment_no).values(create_values))
#     await db.commit()


# Update
async def upload_file_add_study_board_comment(study_board_comment_no: int, file_name: Optional[list[UploadFile]], db: AsyncSession) -> None:
    result = await db.execute(select(Study_Board_Comment.Image_paths).filter(Study_Board_Comment.Comment_no == study_board_comment_no))
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
    await db.execute(update(Study_Board_Comment).filter(Study_Board_Comment.Comment_no == study_board_comment_no).values(create_values))
    await db.commit()

# Delete
async def delete_study_board_comment(study_board_comment_no: int, db: AsyncSession) -> None:
    await db.execute(delete(Study_Board_Comment).filter(Study_Board_Comment.Comment_no == study_board_comment_no))
    await db.commit()


# Delete all
async def all_delete_study_board_comment(study_board_no: int, db: AsyncSession) -> None:
    result = await db.execute(select(Study_Board_Comment.Image_paths).filter(Study_Board_Comment.Board_no == study_board_no))
    comment_image_path_list = result.scalars().all()
    all_image_paths = []
    for image_paths in comment_image_path_list:
        if image_paths: 
            all_image_paths.extend([path.strip() for path in image_paths.split(',')])
    if all_image_paths:
        for image_path in all_image_paths:
            full_path = os.path.join(STATIC_DIR, image_path.strip())
            os.remove(full_path)
    await db.execute(delete(Study_Board_Comment).filter(Study_Board_Comment.Board_no == study_board_no))
    await db.commit()


# Delte Image
async def delete_image_study_board_comment(study_board_comment_no: int, db: AsyncSession) -> None:
    result = await db.execute(select(Study_Board_Comment.Image_paths).filter(Study_Board_Comment.Comment_no == study_board_comment_no))
    image_paths = result.scalar_one_or_none()
    if image_paths:
        image_paths = image_paths.split(',')
        for image_path in image_paths:
            full_path = os.path.join(STATIC_DIR, image_path.strip())
            os.remove(full_path)
    await db.execute(update(Study_Board_Comment).filter(Study_Board_Comment.Comment_no == study_board_comment_no).values(Image_paths=""))
    await db.commit()