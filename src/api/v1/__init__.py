from fastapi import APIRouter
from src.api.v1.user.user_control import router as user_router
from src.api.v1.example.example_control import router as example_router
from src.api.v1.Free_Board.Free_Board_ctl import router as Free_Board_router
from src.api.v1.Free_Board_Comment.Free_Board_Comment_ctl import router as Free_Board_Comment_router
from src.api.v1.Study_Board.Study_Board_ctl import router as Study_Board_router
from src.api.v1.Study_Board_Comment.Study_Board_Comment_ctl import router as Study_Board_Comment_router

router = APIRouter()
router.include_router(user_router)
router.include_router(example_router)
router.include_router(Free_Board_router)
router.include_router(Free_Board_Comment_router)
router.include_router(Study_Board_router)
router.include_router(Study_Board_Comment_router)