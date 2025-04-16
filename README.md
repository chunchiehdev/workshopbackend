# 教育機器人平台

這是一個專為老師與學生設計的教育機器人平台，讓老師能夠設計 AI 教學機器人、編輯學習任務、觀看學生互動紀錄，以及進行班級管理。

## 主要功能

- **機器人管理**：設計、新增、編輯和管理教學機器人，包括設定 prompt 模板和上傳學習資源
- **學習任務**：建立和編輯學習任務，分配給班級和學生
- **互動紀錄**：查看學生與機器人的互動情況和學習成果
- **班級管理**：管理學生班級和成員

## 技術棧

### 前端
- React
- TypeScript
- Tailwind CSS
- ShadcnUI (風格系統)
- React Router

### 後端
- Flask
- OpenAI API
- Docker

## Docker 設置

### 前提條件
- Docker 和 Docker Compose

### 開始使用

1. 複製環境變數範例檔案並設定 OpenAI API 金鑰：
   ```
   cp .env.example .env
   ```
   然後編輯 .env 檔案，添加您的 OpenAI API 金鑰。

2. 構建並啟動容器：
   ```
   docker-compose up --build
   ```

3. 訪問應用程式：
   - 前端：http://localhost:3000
   - 後端 API：http://localhost:5000

4. 開發中的熱加載功能：
   - 後端使用自訂 Python 熱加載腳本，當 Python 檔案變更時自動重啟 Flask 伺服器
   - 前端使用 React 內建的熱加載功能

5. 停止容器：
   ```
   docker-compose down
   ```

## 專案結構

- `app.py`：Flask 後端伺服器
- `templates/`：Flask 應用程式的 HTML 模板
- `frontend/`：React 前端應用程式
  - `src/`：React 原始碼
    - `components/`：React 組件
      - `ui/`：基礎 UI 組件
      - `bots/`：機器人相關組件
      - `dashboard/`：儀表板相關組件
      - `tasks/`：任務相關組件
      - `records/`：記錄相關組件
      - `class-management/`：班級管理相關組件
    - `layouts/`：頁面布局
    - `pages/`：應用程式頁面
    - `lib/`：工具函數
    - `hooks/`：自訂 React hooks
    - `styles/`：全局樣式
    - `App.tsx`：主 React 組件

## 授權

本專案採用 MIT 授權。請參閱 LICENSE 檔案了解更多資訊。

