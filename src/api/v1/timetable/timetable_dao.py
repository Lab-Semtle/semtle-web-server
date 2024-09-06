from sqlalchemy import update 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select 
from src.database.models import User
from src.database.session import rdb

@rdb.dao(transactional=True)
async def post_time_data(user_email: str, data: str, db: AsyncSession) -> bool:
    """
    시간표 데이터 저장 함수
    """
    try:
        stmt = (
                update(User)
                .where(User.user_email == user_email)
                .values(data=data)
            )
        await db.execute(stmt)
    except:
        return False
@rdb.dao()
async def get_time_data(user_email: str, db: AsyncSession):
    """
    시간표 데이터 가져오기 함수
    """
    try:
        stmt = select(User.data).where(User.user_email == user_email) 
        result = await db.execute(stmt) 
        data = result.scalar_one_or_none()  
        return data
    except:
        return False
