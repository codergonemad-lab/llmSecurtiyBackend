from fastapi import APIRouter
from .endpoints import auth, users, challenges

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])