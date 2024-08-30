# '''
# admin/board api : 관리자 페이지-게시판 관리 탭에서 사용되는 라우터
# '''
# from typing import Optional, List
# from pydantic import EmailStr
# from fastapi import APIRouter, Depends, Query
# from src.lib.status import Status, SU, ER
# # from src.api.v1.admin_board.admin_board_dto import (
    
# # ) 
# from src.api.v1.admin_board import admin_board_svc
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.database.session import get_db
# import logging

# logger = logging.getLogger(__name__)
# router = APIRouter(prefix="/admin/user", tags=["admin_user"])

# '''
# - 관리자 게시판,게시물 선택 -> 삭제


# '''
