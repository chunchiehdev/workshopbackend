from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Bot(Base):
    __tablename__ = "bots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    goal = Column(Text, nullable=False)
    object = Column(Text, nullable=False)
    activity = Column(Text, nullable=False)
    format = Column(Text, nullable=False)
    responsestyle = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)
    description = Column(Text, nullable=True)  # 添加描述欄位
    model = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(String(50), nullable=True)  # 可選的用戶ID，未來整合用戶系統時使用
    
    # 關聯到對話記錄
    conversations = relationship("Conversation", back_populates="bot", cascade="all, delete-orphan")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    user_identifier = Column(String(100), nullable=True)  # 可以是匿名ID或登入用戶ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    title = Column(String(200), nullable=True)
    
    # 關聯
    bot = relationship("Bot", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text, nullable=False)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 關聯
    conversation = relationship("Conversation", back_populates="messages") 