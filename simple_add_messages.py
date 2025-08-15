#!/usr/bin/env python3
import psycopg2
import uuid
from datetime import datetime

# 데이터베이스 연결 정보
DATABASE_CONFIG = {
    'host': 'ep-blue-unit-a2ev3s9x.eu-central-1.pg.koyeb.app',
    'database': 'untab',
    'user': 'untab', 
    'password': '0AbVNOIsl2dn',
    'port': 5432
}

def add_messages():
    conn = None
    try:
        print("데이터베이스 연결 중...")
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        # 간단한 메시지 추가 (동기부여 카테고리만)
        messages = [
            ("당신은 생각보다 강합니다.", "나폴레온 힐"),
            ("오늘도 최선을 다하세요.", "데일 카네기"),
            ("꿈을 포기하지 마세요.", "짐 론"),
            ("성공은 노력의 결과입니다.", "브라이언 트레이시"),
            ("매일이 새로운 시작입니다.", "스티븐 코비")
        ]
        
        added_count = 0
        for text, author in messages:
            message_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO morning_prod.daily_messages 
                (id, text, author, category, is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (message_id, text, author, "동기부여", True, datetime.now(), datetime.now()))
            added_count += 1
            print(f"메시지 추가됨: {text}")
        
        conn.commit()
        print(f"총 {added_count}개 메시지 추가 완료")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"오류: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_messages()