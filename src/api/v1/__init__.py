from fastapi import APIRouter
from src.api.v1.admin_user.admin_user_control import router as admin_user_router
from src.api.v1.admin_board.admin_board_control import router as admin_board_router
from src.api.v1.user.user_control import router as user_router


router = APIRouter()
router.include_router(user_router)
router.include_router(admin_user_router)
router.include_router(admin_board_router)