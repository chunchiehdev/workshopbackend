from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Bot模型
class BotBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(..., min_length=2, max_length=100)
    goal: str = Field(...)
    object: str = Field(...)
    activity: str = Field(...)
    format: str = Field(...)
    responsestyle: str = Field(...)
    description: Optional[str] = None
    model: str = Field("gpt-4o", description="AI model to use")
    user_id: Optional[str] = None

class BotCreate(BotBase):
    pass

class BotResponse(BotBase):
    id: int
    prompt: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 對話相關模型
class MessageBase(BaseModel):
    content: str
    is_bot: bool = False

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    user_identifier: Optional[str] = None
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    bot_id: int

class ConversationResponse(ConversationBase):
    id: int
    bot_id: int
    created_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

# 聊天相關模型
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    bot_id: int
    user_identifier: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    conversation_id: int 