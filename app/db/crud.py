from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import models
from app.schemas import schemas
from typing import List, Optional

# Bot CRUD 操作
def create_bot(db: Session, bot: schemas.BotCreate, prompt: str):
    db_bot = models.Bot(
        name=bot.name,
        role=bot.role,
        goal=bot.goal,
        object=bot.object,
        activity=bot.activity,
        format=bot.format,
        responsestyle=bot.responsestyle,
        model=bot.model,
        prompt=prompt,
        description=bot.description,
        user_id=bot.user_id
    )
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def get_bot(db: Session, bot_id: int):
    return db.query(models.Bot).filter(models.Bot.id == bot_id).first()

def get_bots(db: Session, skip: int = 0, limit: int = 100, user_id: Optional[str] = None):
    query = db.query(models.Bot)
    if user_id:
        query = query.filter(models.Bot.user_id == user_id)
    return query.order_by(desc(models.Bot.created_at)).offset(skip).limit(limit).all()

def update_bot(db: Session, bot_id: int, bot_data: schemas.BotCreate, prompt: str):
    db_bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if db_bot:
        update_data = bot_data.dict(exclude_unset=True)
        update_data["prompt"] = prompt
        for key, value in update_data.items():
            setattr(db_bot, key, value)
        db.commit()
        db.refresh(db_bot)
    return db_bot

def delete_bot(db: Session, bot_id: int):
    db_bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if db_bot:
        db.delete(db_bot)
        db.commit()
        return True
    return False

# 對話 CRUD 操作
def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    db_conversation = models.Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_conversations_by_bot(db: Session, bot_id: int, skip: int = 0, limit: int = 20):
    return db.query(models.Conversation).filter(
        models.Conversation.bot_id == bot_id
    ).order_by(desc(models.Conversation.created_at)).offset(skip).limit(limit).all()

def delete_conversation(db: Session, conversation_id: int):
    db_conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if db_conversation:
        db.delete(db_conversation)
        db.commit()
        return True
    return False

# 聊天訊息 CRUD 操作
def create_message(db: Session, message: schemas.MessageCreate, conversation_id: int):
    db_message = models.Message(**message.dict(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, conversation_id: int, skip: int = 0, limit: int = 50):
    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.created_at).offset(skip).limit(limit).all() 