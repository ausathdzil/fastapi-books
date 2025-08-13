from fastapi import APIRouter

from app.api.routes import books, utils

api_router = APIRouter()
api_router.include_router(books.router)
api_router.include_router(utils.router)
