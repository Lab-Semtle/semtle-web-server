from sqlalchemy import Result, ScalarResult, select, update, insert, delete
from sqlalchemy.orm import joinedload, query
from src.schema.models import User
from src.api.v1.user.user_dto import CreateUserInfo, UpdateUserInfo, ReadUserInfo
from src.schema.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


async def get_users_info(db: Session = Depends(get_db)):
    users_info: ScalarResult = await db.scalar(select(User))
    return users_info.unique().all()
