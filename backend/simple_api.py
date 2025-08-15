#!/usr/bin/env python3
"""
PostgreSQL 기반 간단한 API (메시지 포함)
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import hashlib
import json
from typing import Optional, List
import uuid
from datetime import datetime
import random
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = FastAPI(title="모닝 앱 API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 모델들
class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class FavoriteCreate(BaseModel):
    message_id: str
    message_text: str
    message_author: str

# PostgreSQL 데이터베이스 연결 함수
def get_db_connection():
    """PostgreSQL 데이터베이스 연결"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            port=int(os.getenv('DATABASE_PORT', 5432)),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            sslmode='require',
            options=f'-c search_path={os.getenv("DATABASE_SCHEMA", "morning_dev")}'
        )
        return conn
    except Exception as e:
        print(f"DB 연결 오류: {e}")
        raise

# 비밀번호 해시 함수
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 기본 엔드포인트
@app.get("/")
async def root():
    return {"message": "모닝 앱 API 서버가 실행 중입니다!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM daily_messages WHERE is_active = true")
        result = cursor.fetchone()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected", 
            "schema": "postgresql",
            "message_count": result[0],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e), "timestamp": datetime.now().isoformat()}

# 사용자 관련 엔드포인트
@app.post("/auth/register")
async def register(user_data: UserCreate):
    """사용자 회원가입 (기존 users 테이블 사용)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 중복 확인
        cur.execute("SELECT COUNT(*) FROM users WHERE name = %s;", (user_data.name,))
        if cur.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자명입니다.")
        
        if user_data.email:
            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s;", (user_data.email,))
            if cur.fetchone()[0] > 0:
                raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        
        # 새 사용자 생성
        user_id = str(uuid.uuid4())
        password_hash = hash_password(user_data.password)
        
        cur.execute("""
            INSERT INTO users (user_id, name, email, password_hash, active, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (user_id, user_data.name, user_data.email, password_hash, True, datetime.now()))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "message": "회원가입이 완료되었습니다!",
            "user": {
                "user_id": user_id,
                "name": user_data.name,
                "email": user_data.email,
                "active": True,
                "created_at": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"회원가입 중 오류가 발생했습니다: {str(e)}")

@app.post("/auth/login")
async def login(user_data: UserLogin):
    """사용자 로그인"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        password_hash = hash_password(user_data.password)
        
        cur.execute("""
            SELECT user_id, name, email, active, created_at 
            FROM users 
            WHERE name = %s AND password_hash = %s AND active = true
            LIMIT 1;
        """, (user_data.name, password_hash))
        
        user = cur.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="사용자명 또는 비밀번호가 올바르지 않습니다.")
        
        cur.close()
        conn.close()
        
        return {
            "message": "로그인 성공!",
            "user": {
                "user_id": str(user[0]),
                "name": user[1],
                "email": user[2],
                "active": user[3],
                "created_at": user[4].isoformat() if user[4] else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로그인 중 오류가 발생했습니다: {str(e)}")

@app.get("/users")
async def get_users():
    """모든 사용자 조회 (테스트용)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT user_id, name, email, active, created_at 
            FROM users 
            ORDER BY created_at DESC
            LIMIT 10;
        """)
        
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        return {
            "users": [
                {
                    "user_id": str(user[0]),
                    "name": user[1],
                    "email": user[2],
                    "active": user[3],
                    "created_at": user[4].isoformat() if user[4] else None
                }
                for user in users
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 조회 중 오류가 발생했습니다: {str(e)}")

# 즐겨찾기 기능 (localStorage 시뮬레이션)
@app.post("/favorites")
async def add_favorite(favorite: FavoriteCreate):
    """즐겨찾기 추가 (단순 응답)"""
    return {
        "message": f"메시지 '{favorite.message_text[:30]}...'가 즐겨찾기에 추가되었습니다!",
        "favorite_id": str(uuid.uuid4()),
        "success": True
    }

@app.get("/favorites")
async def get_favorites():
    """즐겨찾기 조회 (임시 데이터)"""
    return {
        "favorites": [
            {
                "id": str(uuid.uuid4()),
                "message_id": "msg_1",
                "message_text": "새로운 하루가 시작됩니다. 오늘도 좋은 하루 되세요!",
                "message_author": "모닝 팀",
                "added_at": datetime.now().isoformat()
            }
        ]
    }

# 데이터베이스 정보 확인용
@app.get("/db/tables")
async def get_tables():
    """데이터베이스 테이블 정보 조회"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
            ORDER BY table_name;
        """, (os.getenv('DATABASE_SCHEMA', 'morning_dev'),))
        
        tables = [table[0] for table in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return {"tables": tables}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"테이블 조회 중 오류가 발생했습니다: {str(e)}")

# === 메시지 관련 엔드포인트 ===

@app.get("/messages/random")
async def get_random_message(
    category: Optional[str] = None,
    time_of_day: Optional[str] = None,
    season: Optional[str] = None,
    exclude_ids: Optional[str] = None
):
    """랜덤 메시지 가져오기"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 기본 쿼리
        query = "SELECT * FROM daily_messages WHERE is_active = true"
        params = []
        
        # 필터링 추가
        if category and category != "all":
            query += " AND category = %s"
            params.append(category)
        
        if time_of_day:
            query += " AND (time_of_day = %s OR time_of_day IS NULL)"
            params.append(time_of_day)
        
        if season and season != "all":
            query += " AND (season = %s OR season = 'all')"
            params.append(season)
        
        # 최근 본 메시지 제외
        if exclude_ids:
            ids_list = [int(id_str) for id_str in exclude_ids.split(',') if id_str.isdigit()]
            if ids_list:
                placeholders = ','.join(['%s'] * len(ids_list))
                query += f" AND id NOT IN ({placeholders})"
                params.extend(ids_list)
        
        # 랜덤 정렬
        query += " ORDER BY RANDOM() LIMIT 1"
        
        cursor.execute(query, params)
        message = cursor.fetchone()
        
        if not message:
            # 기본 메시지 반환
            conn.close()
            return {
                "id": "default",
                "text": "새로운 하루가 시작됩니다. 오늘도 좋은 하루 되세요! ✨",
                "author": "모닝",
                "category": "새로운 시작",
                "source": "default"
            }
        
        # 조회수 증가
        cursor.execute("UPDATE daily_messages SET view_count = COALESCE(view_count, 0) + 1 WHERE id = %s", (message[0],))
        conn.commit()
        conn.close()
        
        return {
            "id": message[0],
            "text": message[1],
            "author": message[2],
            "category": message[3],
            "time_of_day": message[4] if len(message) > 4 else None,
            "season": message[5] if len(message) > 5 else None,
            "source": "postgresql",
            "view_count": (message[6] if len(message) > 6 else 0) + 1
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메시지 조회 실패: {str(e)}")

@app.get("/messages/stats")
async def get_message_stats():
    """메시지 통계"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 전체 메시지 수
        cursor.execute("SELECT COUNT(*) FROM daily_messages WHERE is_active = true")
        total = cursor.fetchone()[0]
        
        # 카테고리별 통계
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM daily_messages 
            WHERE is_active = true 
            GROUP BY category
        """)
        categories = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 소스별 통계 (단순히 'postgresql'로 표시)
        sources = {"postgresql": total}
        
        conn.close()
        
        return {
            "total_messages": total,
            "by_category": categories,
            "by_source": sources
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@app.get("/messages/categories")
async def get_categories():
    """사용 가능한 카테고리 목록"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM daily_messages WHERE is_active = true")
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 조회 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("모닝 앱 API 서버 시작 (PostgreSQL)...")
    print("API 문서: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)