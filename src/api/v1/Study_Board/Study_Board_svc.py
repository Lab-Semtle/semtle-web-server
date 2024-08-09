"""
API 개발 시 참고 : 비즈니스 로직 작성, control에서 호출
"""
from pydantic import parse_obj_as
from fastapi import APIRouter, Depends, UploadFile, File

# 호출할 모듈 추가
from src.api.v1.Study_Board.Study_Board_dto import UpdateBoard, ReadBoard, CreateBoard, ReadBoardlist
from src.api.v1.Study_Board import Study_Board_dao

# 이후 삭제 예정, 일단 기본 추가
from sqlalchemy.ext.asyncio import AsyncSession


# Read List
async def get_Study_Board_List(db: AsyncSession, skip: int = 0) -> list[ReadBoardlist]:
    total, Board_info = await Study_Board_dao.get_Study_Board_List(db, skip)
    Board_info = [ReadBoard.from_orm(board).dict() for board in Board_info]
    return total, Board_info

# Read
async def get_Study_Board(db: AsyncSession, Board_no: int) -> ReadBoard:
    Board_info = await Study_Board_dao.get_Study_Board(db, Board_no)
    return Board_info

# Create
async def create_Study_Board(Title: str, Content: str, File_name: list[UploadFile], db: AsyncSession) -> None:
    await Study_Board_dao.create_Study_Board(Title, Content, File_name, db)
   
# Update
async def update_Study_Board(Board_no: int, Title: str, Content: str, File_name: list[UploadFile], db: AsyncSession) -> None:
    await Study_Board_dao.delete_Image_Study_Board(Board_no, db) # 기존에 저장된 이미지 삭제
    await Study_Board_dao.update_Study_Board(Board_no, Title, Content, File_name, db)
    
# Delete
async def delete_Study_Board(Board_no: int, db: AsyncSession) -> None:
    await Study_Board_dao.delete_Study_Board(Board_no, db)

# sort_Title
async def sort_Study_Board(db: AsyncSession, skip: int = 0, select: int = 0) -> list[ReadBoardlist]:
    Total, Board_info = await Study_Board_dao.sort_Study_Board(db, skip, select)
    Board_info = [ReadBoard.from_orm(board).dict() for board in Board_info] 
    return Total, Board_info