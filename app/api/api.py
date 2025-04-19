from fastapi import APIRouter
from app.api.endpoints import bots, conversations, chat, generate, admin

api_router = APIRouter()

# 註冊所有API路由
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"]) 