import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Daily Messages API", description="PostgreSQL backed API for daily messages")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3005", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL 연결 설정
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host='ep-blue-unit-a2ev3s9x.eu-central-1.pg.koyeb.app',
            user='untab',
            password='0AbVNOIsl2dn',
            database='untab',
            port=5432,
            sslmode='require',
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# 테이블 초기화
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 환경에 따른 스키마 선택 (기본값: morning_prod)
        schema = os.getenv('DB_SCHEMA', 'morning_prod')
        table_name = 'daily_messages' if schema == 'morning_prod' else 'daily_messages'
        
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = %s
            )
        """, (schema, table_name))
        table_exists = cursor.fetchone()['exists']
        
        if table_exists:
            print(f"{schema}.{table_name} table found successfully")
        else:
            print(f"Warning: {schema}.{table_name} table not found")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/health")
async def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/api/messages/random")
async def get_random_message(
    category: Optional[str] = None,
    exclude_ids: Optional[str] = None
):
    try:
        logger.info(f"Getting random message with category: {category}")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 환경에 따른 스키마 선택
        schema = os.getenv('DB_SCHEMA', 'morning_prod')
        query = f"SELECT id, text, category, author FROM {schema}.daily_messages WHERE is_active = true"
        params = []
        conditions = []
        
        # 카테고리 필터
        if category and category != "전체":
            conditions.append("category = %s")
            params.append(category)
            logger.info(f"Adding category filter: {category}")
        
        # 제외할 ID들
        if exclude_ids:
            exclude_list = [id.strip() for id in exclude_ids.split(',') if id.strip()]
            if exclude_list:
                placeholders = ','.join(['%s'] * len(exclude_list))
                conditions.append(f"id NOT IN ({placeholders})")
                params.extend(exclude_list)
        
        # 조건 추가
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        # 랜덤 정렬 및 1개 선택
        query += " ORDER BY RANDOM() LIMIT 1"
        
        logger.info(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            message = dict(result)
            logger.info(f"Found message: {message['id']}")
            return message
        else:
            logger.warning("No message found, returning fallback")
            return {
                "id": "fallback",
                "text": "오늘도 새로운 기회가 당신을 기다리고 있습니다.",
                "category": "새로운 시작",
                "author": "작자미상"
            }
    except Exception as e:
        logger.error(f"Error getting random message: {e}")
        return {
            "id": "error",
            "text": "오늘도 새로운 기회가 당신을 기다리고 있습니다.",
            "category": "새로운 시작",
            "author": "작자미상"
        }

@app.get("/api/categories")
async def get_categories():
    try:
        logger.info("Getting categories")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        schema = os.getenv('DB_SCHEMA', 'morning_prod')
        cursor.execute(f"SELECT DISTINCT category FROM {schema}.daily_messages WHERE is_active = true ORDER BY category")
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        categories = [row['category'] for row in results]
        logger.info(f"Found categories: {categories}")
        return {"categories": ["전체"] + categories}
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return {"categories": ["전체", "동기부여", "성장", "자신감", "감사", "희망", "도전", "성취", "행복", "인내", "꿈", "사랑", "평화", "지혜", "용기"]}

@app.get("/api/stats")
async def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 환경에 따른 스키마 선택
        schema = os.getenv('DB_SCHEMA', 'morning_prod')
        
        # 전체 메시지 수
        cursor.execute(f"SELECT COUNT(*) as total FROM {schema}.daily_messages WHERE is_active = true")
        total = cursor.fetchone()['total']
        
        # 카테고리별 메시지 수
        cursor.execute(f"SELECT category, COUNT(*) as count FROM {schema}.daily_messages WHERE is_active = true GROUP BY category ORDER BY category")
        category_results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        by_category = {row['category']: row['count'] for row in category_results}
        
        return {
            "total_messages": total,
            "by_category": by_category
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {"total_messages": 0, "by_category": {}}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3002))
    uvicorn.run(app, host="0.0.0.0", port=port)