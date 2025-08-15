#!/usr/bin/env python3
"""잘못 만든 messages 테이블 삭제"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def cleanup():
    print("Cleaning up wrong tables...")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            port=os.getenv('DATABASE_PORT', 5432),
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # 잘못 만든 messages 테이블 삭제
        print("Dropping morning_dev.messages table...")
        cur.execute("DROP TABLE IF EXISTS morning_dev.messages")
        
        # 잘못 만든 users 테이블도 삭제 (기존에 있을 수 있음)
        print("Dropping morning_dev.users table (if created by mistake)...")
        cur.execute("DROP TABLE IF EXISTS morning_dev.users CASCADE")
        
        conn.commit()
        
        # 확인
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'morning_dev' AND table_name IN ('messages', 'users')
        """)
        remaining = cur.fetchall()
        
        if remaining:
            print(f"WARNING: Still found these tables: {remaining}")
        else:
            print("SUCCESS: Wrong tables removed")
        
        # daily_messages 테이블 확인
        cur.execute("SELECT COUNT(*) FROM morning_dev.daily_messages WHERE is_active = true")
        count = cur.fetchone()[0]
        print(f"daily_messages table has {count} active messages")
        
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    cleanup()