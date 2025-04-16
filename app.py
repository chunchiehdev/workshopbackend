from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # 讀取 .env

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables. Please check your .env file.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    role = data.get("role", "")
    goal = data.get("goal", "")
    object = data.get("object", "")
    activity = data.get("activity", "")
    format = data.get("format", "")
    responsestyle = data.get("responsestyle", "")
    model = data.get("model", "gpt-4o")

    # ✅ 印出前端傳入資料
    print("\n===== 前端傳入內容 =====")
    print(f"角色：{role}")
    print(f"任務目標：{goal}")
    print(f"教學對象描述：{object}")
    print(f"教學活動方式：{activity}")
    print(f"輸出格式：{format}")
    print(f"回應風格：{responsestyle}")
    print(f"使用模型：{model}")
    print("=======================\n")

    # ✅ 新版 Prompt 內容設計
    prompt = f"""
                你是一個擬人化的 AI 教學機器人，角色是「{role}」。
                請根據以下設定幫我設計一段 chatbot Prompt，用來建立一個能與學生進行互動的 AI 對話機器人。

                🎯 任務目標（Goal）：
                {goal}

                👥 教學對象描述（Object）：
                {object}

                🛠️ 教學活動進行方式（Learning Activity）：
                {activity}

                🗂️ 輸出內容與格式（Output）：
                {format}

                🎨 回應風格（Style）：
                {responsestyle}

                請用這些條件撰寫一段 Prompt，讓這個機器人能用來幫助學生進行有意義的學習對話。Prompt 中請包括：
                - 機器人角色與個性
                - 回應語氣
                - 該如何進行提問或引導
                - 要提供什麼樣的學習幫助與回饋
            """

    try:
        # Alternative API key setup approach
        api_key = os.getenv("OPENAI_API_KEY")
        print("api_key", api_key)
        if not api_key:
            return jsonify({"error": "OPENAI_API_KEY not found in environment variables"}), 500
            
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        print(reply,"reply")
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
