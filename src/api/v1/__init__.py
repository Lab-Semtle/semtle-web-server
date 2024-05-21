from fastapi import APIRouter
from .user.user_control import router as user_router
from .example.example_control import router as example_router

router = APIRouter()
router.include_router(user_router)
router.include_router(example_router)
