#!/usr/bin/env python3
import psycopg2
import uuid
from datetime import datetime

DATABASE_CONFIG = {
    'host': 'ep-blue-unit-a2ev3s9x.eu-central-1.pg.koyeb.app',
    'database': 'untab',
    'user': 'untab', 
    'password': '0AbVNOIsl2dn',
    'port': 5432
}

def add_five_messages():
    messages = [
        ("성공은 준비와 기회가 만나는 순간에 탄생합니다.", "세네카", "성공"),
        ("긍정적인 마음이 긍정적인 현실을 만들어냅니다.", "노먼 빈센트 필", "긍정"),
        ("행복은 여행의 방식이지 목적지가 아닙니다.", "로이 굿먼", "행복"),
        ("건강한 몸에 건강한 정신이 깃듭니다.", "유베날리스", "건강"),
        ("상상력은 지식보다 더 중요합니다.", "아인슈타인", "창의성")
    ]
    
    conn = None
    try:
        print("연결 중...")
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        for text, author, category in messages:
            message_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO morning_prod.daily_messages 
                (id, text, author, category, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (message_id, text, author, category, True, datetime.now(), datetime.now()))
            print(f"추가: {text[:30]}... - {author} ({category})")
        
        conn.commit()
        print("5개 메시지 추가 완료!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"오류: {e}")
        if conn:
            conn.close()

if __name__ == "__main__":
    add_five_messages()