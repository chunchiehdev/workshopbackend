from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.db import crud
from app.db.database import get_db
from app.schemas import schemas
from app.utils.ai import build_educational_prompt, generate_ai_response
from app.core.config import settings

router = APIRouter()

class PromptRequest(BaseModel):
    role: str = Field(..., description="The character or role the AI should play (e.g., 'Math Teacher')")
    goal: str = Field(..., description="Learning objectives for students")
    object: str = Field(..., description="Description of target students")
    activity: str = Field(..., description="How the learning activity should be conducted")
    format: str = Field(..., description="Desired output format")
    responsestyle: str = Field(..., description="Tone/style for responses")
    description: Optional[str] = Field(None, description="Bot description (optional)")
    model: str = Field("gpt-4o", description="AI model to use (e.g., 'gpt-4o' or 'gemini-2.0-flash')")
    name: str = Field(..., min_length=2, max_length=100, description="Name of the bot")
    user_id: Optional[str] = None

class PromptResponse(BaseModel):
    reply: str
    bot_id: Optional[int] = None

class ErrorResponse(BaseModel):
    error: str


@router.post("/", response_model=PromptResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_prompt(
    request: PromptRequest, 
    background_tasks: BackgroundTasks,
    save_to_db: bool = True,
    db: Session = Depends(get_db)
):
    """
    Generate educational chatbot prompts based on provided parameters.
    
    This endpoint automatically detects whether to use OpenAI or Gemini APIs
    based on the model name provided.
    """
    try:
        # Log input parameters
        print("\n===== Request Parameters =====")
        for key, value in request.dict().items():
            print(f"{key}: {value}")
        print("=============================\n")
        
        # Build educational prompt
        prompt = build_educational_prompt(request)
        
        # Determine if model is Gemini or OpenAI based on model name
        is_gemini_model = any(model_name in request.model.lower() for model_name in settings.GEMINI_MODELS)
        
        # Generate response using unified approach
        reply = generate_ai_response(prompt, request.model, is_gemini_model)
        
        # 如果需要保存到數據庫
        bot_id = None
        if save_to_db:
            # 創建Bot對象
            bot_create = schemas.BotCreate(
                name=request.name,
                role=request.role,
                goal=request.goal,
                object=request.object,
                activity=request.activity,
                format=request.format,
                responsestyle=request.responsestyle,
                model=request.model,
                description=getattr(request, 'description', None),
                user_id=request.user_id
            )
            # 保存到數據庫
            db_bot = crud.create_bot(db=db, bot=bot_create, prompt=reply)
            bot_id = db_bot.id
            
        return {"reply": reply, "bot_id": bot_id}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 