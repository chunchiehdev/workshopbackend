from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud
from app.db.database import get_db
from app.schemas import schemas
from app.utils.ai import build_educational_prompt, generate_ai_response
from app.core.config import settings

router = APIRouter()

# @router.post("/", response_model=schemas.BotResponse)
# def create_bot(bot: schemas.BotCreate, db: Session = Depends(get_db)):
#     """創建新的Bot（不生成提示詞，使用已有的提示詞）"""
#     prompt = build_educational_prompt(bot)  # 使用相同的提示詞生成函數
#     return crud.create_bot(db=db, bot=bot, prompt=prompt)


@router.get("/", response_model=List[schemas.BotResponse])
def read_bots(skip: int = 0, limit: int = 100, user_id: Optional[str] = None, db: Session = Depends(get_db)):
    """獲取Bot列表，可以按用戶ID篩選"""
    bots = crud.get_bots(db, skip=skip, limit=limit, user_id=user_id)
    return bots


@router.get("/{bot_id}", response_model=schemas.BotResponse)
def read_bot(bot_id: int, db: Session = Depends(get_db)):
    """獲取指定Bot的詳細信息"""
    db_bot = crud.get_bot(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return db_bot


@router.put("/{bot_id}", response_model=schemas.BotResponse)
def update_bot(bot_id: int, bot: schemas.BotCreate, db: Session = Depends(get_db)):
    """更新Bot信息"""
    prompt = build_educational_prompt(bot) 
    is_gemini_model = any(model_name in bot.model.lower() for model_name in settings.GEMINI_MODELS)
    generated_prompt = generate_ai_response(prompt, bot.model, is_gemini_model)
    db_bot = crud.update_bot(db, bot_id=bot_id, bot_data=bot, prompt=generated_prompt)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return db_bot


@router.delete("/{bot_id}", response_model=dict)
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    """刪除Bot"""
    success = crud.delete_bot(db, bot_id=bot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"status": "success", "message": "Bot deleted"} 