from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API keys from environment
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Check API keys
if not OPENAI_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables")
if not GEMINI_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables")

# Define Gemini models
GEMINI_MODELS = {
    "gemini-pro", 
    "gemini-1.0-pro", 
    "gemini-1.5-pro", 
    "gemini-2.0-flash"
}


@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the application is running."""
    return {"status": "healthy"}


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate educational chatbot prompts based on provided parameters.
    
    This endpoint expects a POST request with JSON data containing:
    - role: The character/role the AI should play (e.g., "Math Teacher")
    - goal: Learning objectives for students
    - object: Description of target students
    - activity: How the learning activity should be conducted
    - format: Desired output format
    - responsestyle: Tone/style for responses
    - model: AI model to use (e.g., "gpt-4o" or "gemini-2.0-flash")
    
    The endpoint automatically detects whether to use OpenAI or Gemini APIs
    based on the model name provided.
    """
    try:
        # Extract parameters from request
        params = extract_parameters(request.get_json())
        
        # Log input parameters
        log_parameters(params)
        
        # Build educational prompt
        prompt = build_educational_prompt(params)
        
        # Determine if model is Gemini or OpenAI based on model name
        is_gemini_model = any(model_name in params["model"].lower() for model_name in GEMINI_MODELS)
        
        # Generate response using unified approach
        reply = generate_ai_response(prompt, params["model"], is_gemini_model)
        
        return jsonify({"reply": reply})
        
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"API error: {str(e)}")
        return jsonify({"error": str(e)}), 500


def extract_parameters(data: Dict[str, Any]) -> Dict[str, str]:
    """Extract and validate parameters from the request data."""
    if not data:
        raise ValueError("Request body is empty or invalid")
    
    return {
        "role": data.get("role", ""),
        "goal": data.get("goal", ""),
        "object": data.get("object", ""),
        "activity": data.get("activity", ""),
        "format": data.get("format", ""),
        "responsestyle": data.get("responsestyle", ""),
        "model": data.get("model", "gpt-4o")
    }


def log_parameters(params: Dict[str, str]) -> None:
    """Log input parameters for debugging."""
    print("\n===== Request Parameters =====")
    for key, value in params.items():
        print(f"{key}: {value}")
    print("=============================\n")


def build_educational_prompt(params: Dict[str, str]) -> str:
    """Build prompt template for educational chatbot."""
    return f"""
        你是一個擬人化的 AI 教學機器人，角色是「{params['role']}」。
        請根據以下設定幫我設計一段 chatbot Prompt，用來建立一個能與學生進行互動的 AI 對話機器人。

        🎯 任務目標（Goal）：
        {params['goal']}

        👥 教學對象描述（Object）：
        {params['object']}

        🛠️ 教學活動進行方式（Learning Activity）：
        {params['activity']}

        🗂️ 輸出內容與格式（Output）：
        {params['format']}

        🎨 回應風格（Style）：
        {params['responsestyle']}

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)