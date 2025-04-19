from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import crud
from app.db.database import get_db
from app.schemas import schemas
from app.utils.ai import generate_chat_response
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=schemas.ChatResponse)
async def chat_with_bot(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    """與Bot聊天的API端點"""
    # 獲取Bot
    db_bot = crud.get_bot(db, bot_id=request.bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # 獲取或創建對話
    conversation_id = request.conversation_id
    if conversation_id is None:
        # 創建新對話
        conversation = schemas.ConversationCreate(
            bot_id=request.bot_id, 
            user_identifier=request.user_identifier,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message
        )
        db_conversation = crud.create_conversation(db=db, conversation=conversation)
        conversation_id = db_conversation.id
    else:
        # 驗證對話存在
        db_conversation = crud.get_conversation(db, conversation_id=conversation_id)
        if db_conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        if db_conversation.bot_id != request.bot_id:
            raise HTTPException(status_code=400, detail="Conversation does not belong to this bot")
    
    # 保存用戶訊息
    user_message = schemas.MessageCreate(content=request.message, is_bot=False)
    crud.create_message(db=db, message=user_message, conversation_id=conversation_id)
    
    # 獲取對話歷史
    messages = crud.get_messages(db, conversation_id=conversation_id)
    
    # 構建對話歷史
    chat_history = "\n".join([f"{'Bot' if msg.is_bot else 'User'}: {msg.content}" for msg in messages])
    
    # 確定模型是Gemini還是OpenAI
    is_gemini_model = any(model_name in db_bot.model.lower() for model_name in settings.GEMINI_MODELS)
    
    # 生成回覆
    try:
        bot_reply = generate_chat_response(
            bot_prompt=db_bot.prompt, 
            chat_history=chat_history, 
            message=request.message, 
            model=db_bot.model, 
            is_gemini=is_gemini_model
        )
        
        # 保存機器人回覆
        bot_message = schemas.MessageCreate(content=bot_reply, is_bot=True)
        crud.create_message(db=db, message=bot_message, conversation_id=conversation_id)
        
        return {"reply": bot_reply, "conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}") 