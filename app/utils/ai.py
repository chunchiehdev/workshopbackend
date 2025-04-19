import openai
from app.core.config import settings

def build_educational_prompt(params) -> str:
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
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        client = openai.OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        
        # Add system message for Gemini
        messages = [
            {"role": "system", "content": "你是一個有幫助的教育助手。"},
            {"role": "user", "content": prompt}
        ]
    else:
        # Use standard OpenAI API
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Simple message for OpenAI
        messages = [{"role": "user", "content": prompt}]
    
    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    return response.choices[0].message.content


def generate_chat_response(bot_prompt: str, chat_history: str, message: str, model: str, is_gemini: bool) -> str:
    """Generate a chat response based on bot prompt and chat history."""
    system_prompt = f"""你是一個遵循以下角色定義的AI教學助手：

    {bot_prompt}

    請按照上述設定的角色與指導方針回覆用戶的問題。
    """
    
    user_prompt = f"聊天歷史：\n{chat_history}\n\n請根據上述聊天歷史回應用戶最後一個問題。"
    
    # 調用AI生成回覆
    if is_gemini:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found")
        # 使用Gemini的OpenAI兼容API
        client = openai.OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    else:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found")
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    messages_for_api = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # 生成回覆
    response = client.chat.completions.create(
        model=model,
        messages=messages_for_api
    )
    
    return response.choices[0].message.content 