import psycopg2
import time
from app.db.database import engine, Base
from app.core.config import settings
import os

def init_db():
    """初始化數據庫，等待數據庫準備好後再創建表"""
    max_retries = 10
    retry_interval = 3

    for i in range(max_retries):
        try:
            print(f"嘗試連接數據庫... (嘗試 {i+1}/{max_retries})")
            
            # 從 settings 獲取資料庫連接信息
            db_url = settings.DATABASE_URL
            # 解析資料庫 URL 以獲取連接參數
            db_parts = db_url.replace("postgresql://", "").split("@")
            user_pass = db_parts[0].split(":")
            host_port_db = db_parts[1].split("/")
            host_port = host_port_db[0].split(":")
            
            # 測試連接
            conn = psycopg2.connect(
                dbname=host_port_db[1],
                user=user_pass[0],
                password=user_pass[1],
                host=host_port[0],
                port=host_port[1]
            )
            conn.close()
            print("數據庫連接成功，創建表...")
            Base.metadata.create_all(bind=engine)
            print("表創建完成")
            return
        except Exception as e:
            print(f"數據庫連接失敗: {e}")
            if i < max_retries - 1:
                print(f"等待 {retry_interval} 秒後重試...")
                time.sleep(retry_interval)
            else:
                print("達到最大重試次數，放棄嘗試")
                raise 