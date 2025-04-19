from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import crud
from app.db.database import get_db
from app.schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.ConversationResponse)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(get_db)):
    """創建新對話"""
    db_bot = crud.get_bot(db, bot_id=conversation.bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return crud.create_conversation(db=db, conversation=conversation)


@router.get("/{conversation_id}", response_model=schemas.ConversationResponse)
def read_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """獲取對話詳情及其訊息"""
    db_conversation = crud.get_conversation(db, conversation_id=conversation_id)
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db_conversation


@router.get("/bot/{bot_id}", response_model=List[schemas.ConversationResponse])
def read_conversations_by_bot(bot_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """獲取指定Bot的所有對話"""
    db_bot = crud.get_bot(db, bot_id=bot_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return crud.get_conversations_by_bot(db, bot_id=bot_id, skip=skip, limit=limit)


@router.delete("/{conversation_id}", response_model=dict)
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """刪除對話及其所有訊息"""
    success = crud.delete_conversation(db, conversation_id=conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "success", "message": "Conversation deleted"} 