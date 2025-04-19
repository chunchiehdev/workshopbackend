import psycopg2
import time
from app.db.database import engine, Base
from app.core.config import settings

def init_db():
    """初始化數據庫，等待數據庫準備好後再創建表"""
    max_retries = 10
    retry_interval = 3

    for i in range(max_retries):
        try:
            print(f"嘗試連接數據庫... (嘗試 {i+1}/{max_retries})")
            # 測試連接
            conn = psycopg2.connect(
                dbname="teachbot",
                user="postgres", 
                password="postgres",
                host="db", 
                port="5432"
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