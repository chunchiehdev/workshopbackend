from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import uvicorn

from app.api.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for generating educational chatbot prompts using OpenAI or Google Gemini models",
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊API路由
app.include_router(api_router)

# 靜態文件和模板
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
except:
    print("⚠️ WARNING: 'static' or 'templates' directory not found. Static files and templates will not be served.")
    templates = None


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


if __name__ == "__main__":
    # 初始化資料庫
    init_db()
    
    # Run the server using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 