from fastapi import APIRouter
from .user.user_control import router as user_router
from .login.login_control import router as login_router
from .course.course_control import router as course_router

router = APIRouter()
router.include_router(user_router)
router.include_router(login_router)
router.include_router(course_router)