from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import datetime

from app.db.database import get_db

router = APIRouter()

@router.get("/tables", response_model=dict)
async def list_tables(db: Session = Depends(get_db)):
    """列出數據庫中的所有表"""
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """
    result = db.execute(query).fetchall()
    tables = [row[0] for row in result]
    return {"tables": tables}

@router.get("/tables/{table_name}", response_model=dict)
async def view_table_data(table_name: str, limit: int = 100, db: Session = Depends(get_db)):
    """檢視指定表的數據"""
    if table_name not in ["bots", "conversations", "messages"]:
        raise HTTPException(status_code=400, detail="Invalid table name")
    
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    result = db.execute(query).fetchall()
    
    # 將結果轉換為字典列表
    column_names = db.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'").fetchall()
    column_names = [col[0] for col in column_names]
    
    data = []
    for row in result:
        item = {}
        for i, column in enumerate(column_names):
            # 處理日期時間格式
            if isinstance(row[i], (datetime.datetime, datetime.date)):
                item[column] = str(row[i])
            else:
                item[column] = row[i]
        data.append(item)
    
    return {"table": table_name, "columns": column_names, "data": data, "count": len(data)} 