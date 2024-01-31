from fastapi import APIRouter

from . import chat, project

api_router = APIRouter()
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(project.router, tags=["project"])
