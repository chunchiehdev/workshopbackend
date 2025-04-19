from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import openai
import os
from dotenv import load_dotenv
from typing import Optional, List, Set
import uvicorn

# Load environment variables
load_dotenv()

# Get API keys from environment
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Check API keys
if not OPENAI_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables")
if not GEMINI_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables")

# Define Gemini models
GEMINI_MODELS: Set[str] = {
    "gemini-pro", 
    "gemini-1.0-pro", 
    "gemini-1.5-pro", 
    "gemini-2.0-flash"
}

# Initialize FastAPI app
app = FastAPI(
    title="AI Teaching Assistant Generator",
    description="API for generating educational chatbot prompts using OpenAI or Google Gemini models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# For serving static files and templates (if needed)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
except:
    print("⚠️ WARNING: 'static' or 'templates' directory not found. Static files and templates will not be served.")

# Define request model with Pydantic for validation
class PromptRequest(BaseModel):
    role: str = Field(..., description="The character or role the AI should play (e.g., 'Math Teacher')")
    goal: str = Field(..., description="Learning objectives for students")
    object: str = Field(..., description="Description of target students")
    activity: str = Field(..., description="How the learning activity should be conducted")
    format: str = Field(..., description="Desired output format")
    responsestyle: str = Field(..., description="Tone/style for responses")
    model: str = Field("gpt-4o", description="AI model to use (e.g., 'gpt-4o' or 'gemini-2.0-flash')")

# Define response model
class PromptResponse(BaseModel):
    reply: str

# Define error response model
class ErrorResponse(BaseModel):
    error: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page of the application."""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except:
        return HTMLResponse(content="<html><body><h1>AI Teaching Assistant Generator</h1><p>Visit /docs for API documentation</p></body></html>")


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint to verify the application is running."""
    return {"status": "healthy"}


@app.post("/generate", response_model=PromptResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate(request: PromptRequest):
    """
    Generate educational chatbot prompts based on provided parameters.
    
    This endpoint automatically detects whether to use OpenAI or Gemini APIs
    based on the model name provided.
    """
    try:
        # Log input parameters
        log_parameters(request.dict())
        
        # Build educational prompt
        prompt = build_educational_prompt(request)
        
        # Determine if model is Gemini or OpenAI based on model name
        is_gemini_model = any(model_name in request.model.lower() for model_name in GEMINI_MODELS)
        
        # Generate response using unified approach
        reply = generate_ai_response(prompt, request.model, is_gemini_model)
        
        return {"reply": reply}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def log_parameters(params: dict) -> None:
    """Log input parameters for debugging."""
    print("\n===== Request Parameters =====")
    for key, value in params.items():
        print(f"{key}: {value}")
    print("=============================\n")


def build_educational_prompt(params: PromptRequest) -> str:
    """Build prompt template for educational chatbot."""
    return f"""
        你是一個擬人化的 AI 教學機器人，角色是「{params.role}」。
        請根據以下設定幫我設計一段 chatbot Prompt，用來建立一個能與學生進行互動的 AI 對話機器人。

        🎯 任務目標（Goal）：
        {params.goal}

        👥 教學對象描述（Object）：
        {params.object}

        🛠️ 教學活動進行方式（Learning Activity）：
        {params.activity}

        🗂️ 輸出內容與格式（Output）：
        {params.format}

        🎨 回應風格（Style）：
        {params.responsestyle}

        請用這些條件撰寫一段 Prompt，讓這個機器人能用來幫助學生進行有意義的學習對話。Prompt 中請包括：
        - 機器人角色與個性
        - 回應語氣
        - 該如何進行提問或引導
        - 要提供什麼樣的學習幫助與回饋
    """


def generate_ai_response(prompt: str, model: str, is_gemini: bool) -> str:
    """Generate AI response using either OpenAI or Gemini API through OpenAI client."""
    if is_gemini:
        # Use Gemini API through OpenAI compatibility
        if not GEMINI_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        client = openai.OpenAI(
            api_key=GEMINI_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        # Add system message for Gemini
        messages = [
            {"role": "system", "content": "你是一個有幫助的教育助手。"},
            {"role": "user", "content": prompt}
        ]
    else:
        # Use standard OpenAI API
        if not OPENAI_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        client = openai.OpenAI(api_key=OPENAI_KEY)
        
        # Simple message for OpenAI
        messages = [{"role": "user", "content": prompt}]
    
    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    # Run the server using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)