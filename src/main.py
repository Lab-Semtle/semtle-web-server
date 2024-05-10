"""
Main Server Module
"""
from fastapi import FastAPI
from src.api.v1.user import user_control
from src.schema.session import engine, Base
from src.schema import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# async def close_app():
#     await engine.dispose()
#     print("Application is shutting down.")

# # 이벤트 핸들러 등록
# app.add_event_handler("startup", create_tables)
# app.add_event_handler("shutdown", close_app)


# 라우터 포함
app.include_router(user_control.router)
