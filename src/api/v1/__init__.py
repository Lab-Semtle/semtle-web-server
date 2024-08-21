from fastapi import APIRouter
from src.api.v1.free_board.free_board_ctl import router as Free_Board_router
from src.api.v1.free_board_comment.free_board_comment_ctl import router as Free_Board_Comment_router
from src.api.v1.study_board.study_board_ctl import router as Study_Board_router
from src.api.v1.study_board_comment.study_board_comment_ctl import router as Study_Board_Comment_router
from src.api.v1.exam_sharing_board.exam_sharing_board_ctl import router as Exam_Sharing_Board_router
from src.api.v1.exam_sharing_board_comment.exam_sharing_board_comment_ctl import router as Exam_Sharing_Board_Comment_router

router = APIRouter()
router.include_router(Free_Board_router)
router.include_router(Free_Board_Comment_router)
router.include_router(Study_Board_router)
router.include_router(Study_Board_Comment_router)
router.include_router(Exam_Sharing_Board_router)
router.include_router(Exam_Sharing_Board_Comment_router)