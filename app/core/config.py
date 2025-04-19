import os
from dotenv import load_dotenv
from typing import Set, List, Optional

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Teaching Assistant Generator"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/teachbot")
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Model settings
    GEMINI_MODELS: Set[str] = {
        "gemini-pro", 
        "gemini-1.0-pro", 
        "gemini-1.5-pro", 
        "gemini-2.0-flash"
    }
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

settings = Settings() 