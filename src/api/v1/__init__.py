from fastapi import APIRouter
from src.api.v1.admin_user.admin_user_control import router as admin_user_router
from src.api.v1.admin_board.admin_board_control import router as admin_board_router
from src.api.v1.user.user_control import router as user_router
from src.api.v1.Free_Board.Free_Board_ctl import router as Free_Board_router
from src.api.v1.Free_Board_Comment.Free_Board_Comment_ctl import router as Free_Board_Comment_router
from .login.login_control import router as login_router
from .course.course_control import router as course_router
from .jokbo.jokbo_control import router as jokbo_router


router = APIRouter()
router.include_router(user_router)
router.include_router(admin_user_router)
router.include_router(admin_board_router)

router.include_router(login_router)
router.include_router(course_router)
router.include_router(jokbo_router)

router.include_router(Free_Board_router)
router.include_router(Free_Board_Comment_router)