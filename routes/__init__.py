from fastapi import APIRouter

from .response import router as response_router

main_router = APIRouter()

main_router.include_router(response_router, tags=["response"])

@main_router.get("/")
async def index():
    return 0