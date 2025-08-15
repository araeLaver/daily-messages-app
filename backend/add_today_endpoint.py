#!/usr/bin/env python3
"""
PostgreSQL API 서버에 /api/messages/today 엔드포인트를 추가하는 임시 서버
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from datetime import datetime
import random

load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME'),
        port=os.getenv('DATABASE_PORT', 5432)
    )

@app.get("/")
async def root():
    return {"message": "PostgreSQL API 서버", "version": "2.0.0"}

@app.get("/api/messages/random")
async def get_random_message():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        schema = os.getenv('DATABASE_SCHEMA', 'public')
        cur.execute(f"SELECT * FROM {schema}.messages WHERE is_active = true ORDER BY RANDOM() LIMIT 1")
        message = cur.fetchone()
        
        if not message:
            return {"id": "default", "text": "새로운 하루가 시작됩니다.", "category": "기본"}
        
        # 조회수 증가
        cur.execute(f"UPDATE {schema}.messages SET view_count = view_count + 1 WHERE id = %s", (message['id'],))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return dict(message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages/today")
async def get_today_message():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        schema = os.getenv('DATABASE_SCHEMA', 'public')
        
        # 오늘 날짜 기반으로 고정된 메시지 선택
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday
        
        cur.execute(f"SELECT COUNT(*) FROM {schema}.messages WHERE is_active = true")
        total_count = cur.fetchone()[0]
        
        if total_count == 0:
            return {"id": "today_default", "text": "오늘도 좋은 하루 되세요!", "category": "기본", "isToday": True}
        
        offset = day_of_year % total_count
        
        cur.execute(f"SELECT * FROM {schema}.messages WHERE is_active = true ORDER BY id LIMIT 1 OFFSET %s", (offset,))
        message = cur.fetchone()
        
        if message:
            cur.execute(f"UPDATE {schema}.messages SET view_count = view_count + 1 WHERE id = %s", (message['id'],))
            conn.commit()
        
        cur.close()
        conn.close()
        
        result = dict(message)
        result['isToday'] = True
        result['date'] = today.strftime("%Y-%m-%d")
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        schema = os.getenv('DATABASE_SCHEMA', 'public')
        cur.execute(f"SELECT DISTINCT category FROM {schema}.messages WHERE is_active = true ORDER BY category")
        
        categories = []
        total_count = 0
        
        for row in cur.fetchall():
            category = row[0]
            # 각 카테고리별 메시지 수 계산
            cur.execute(f"SELECT COUNT(*) FROM {schema}.messages WHERE category = %s AND is_active = true", (category,))
            count = cur.fetchone()[0]
            total_count += count
            
            categories.append({
                "name": category,
                "name_ko": category,
                "message_count": count
            })
        
        # '전체' 카테고리 추가
        categories.insert(0, {
            "name": "all",
            "name_ko": "전체", 
            "message_count": total_count
        })
        
        cur.close()
        conn.close()
        
        return categories
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        schema = os.getenv('DATABASE_SCHEMA', 'public')
        
        # 전체 메시지 수
        cur.execute(f"SELECT COUNT(*) FROM {schema}.messages WHERE is_active = true")
        total = cur.fetchone()[0]
        
        # 카테고리별 통계
        cur.execute(f"SELECT category, COUNT(*) FROM {schema}.messages WHERE is_active = true GROUP BY category")
        by_category = dict(cur.fetchall())
        
        cur.close()
        conn.close()
        
        return {
            "total_messages": total,
            "by_category": by_category,
            "schema": "postgresql"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("새로운 PostgreSQL API 서버 시작 (포트 3004)...")
    uvicorn.run(app, host="127.0.0.1", port=3004)