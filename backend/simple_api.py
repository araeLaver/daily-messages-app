#!/usr/bin/env python3
"""
SQLite 기반 간단한 API (메시지 포함)
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import hashlib
import json
from typing import Optional, List
import uuid
from datetime import datetime
import random

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

# SQLite 데이터베이스 연결 함수
def get_db_connection():
    """SQLite 데이터베이스 연결"""
    conn = sqlite3.connect('messages.db')
    conn.row_factory = sqlite3.Row
    return conn

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
        cursor.execute("SELECT COUNT(*) as count FROM messages")
        result = cursor.fetchone()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected", 
            "schema": "sqlite",
            "message_count": result['count'],
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
        cur.execute("SELECT user_id FROM users WHERE name = %s;", (user_data.name,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자명입니다.")
        
        if user_data.email:
            cur.execute("SELECT user_id FROM users WHERE email = %s;", (user_data.email,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")
        
        # 새 사용자 생성
        user_id = str(uuid.uuid4())
        password_hash = hash_password(user_data.password)
        
        cur.execute("""
            INSERT INTO users (user_id, name, email, password_hash, active, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING user_id, name, email, active, created_at;
        """, (user_id, user_data.name, user_data.email, password_hash, True, datetime.now()))
        
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "message": "회원가입이 완료되었습니다!",
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
            WHERE name = %s AND password_hash = %s AND active = true;
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
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
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
    season: Optional[str] = None
):
    """랜덤 메시지 가져오기"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 기본 쿼리
        query = "SELECT * FROM messages WHERE is_active = 1"
        params = []
        
        # 필터링 추가
        if category and category != "all":
            query += " AND category = ?"
            params.append(category)
        
        if time_of_day:
            query += " AND (time_of_day = ? OR time_of_day IS NULL)"
            params.append(time_of_day)
        
        if season and season != "all":
            query += " AND (season = ? OR season = 'all')"
            params.append(season)
        
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
        cursor.execute("UPDATE messages SET view_count = view_count + 1 WHERE id = ?", (message['id'],))
        conn.commit()
        conn.close()
        
        return {
            "id": message['id'],
            "text": message['text'],
            "author": message['author'],
            "category": message['category'],
            "time_of_day": message['time_of_day'],
            "season": message['season'],
            "source": message['source'],
            "view_count": message['view_count'] + 1
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
        cursor.execute("SELECT COUNT(*) as count FROM messages WHERE is_active = 1")
        total = cursor.fetchone()['count']
        
        # 카테고리별 통계
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM messages 
            WHERE is_active = 1 
            GROUP BY category
        """)
        categories = {row['category']: row['count'] for row in cursor.fetchall()}
        
        # 소스별 통계
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM messages 
            WHERE is_active = 1 
            GROUP BY source
        """)
        sources = {row['source']: row['count'] for row in cursor.fetchall()}
        
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
        
        cursor.execute("SELECT DISTINCT category FROM messages WHERE is_active = 1")
        categories = [row['category'] for row in cursor.fetchall()]
        
        conn.close()
        
        return {"categories": categories}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 조회 실패: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("모닝 앱 API 서버 시작...")
    print("API 문서: http://localhost:8005/docs")
    uvicorn.run(app, host="0.0.0.0", port=8005)