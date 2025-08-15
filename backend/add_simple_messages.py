#!/usr/bin/env python3
"""
PostgreSQL에 간단한 메시지 100개씩 추가
"""

import psycopg2
import uuid
import random
import os
from dotenv import load_dotenv

load_dotenv()

# 카테고리와 간단한 메시지들
categories_messages = {
    "동기부여": [
        "오늘도 최선을 다하는 당신이 멋집니다.",
        "작은 발걸음이 큰 변화를 만듭니다.",
        "포기하지 않는 당신이 승리자입니다.",
        "오늘의 노력이 내일의 성공을 만듭니다.",
        "당신은 이미 충분히 잘하고 있습니다.",
    ],
    "지혜": [
        "경험은 최고의 스승입니다.",
        "실수에서 배우는 것이 진정한 지혜입니다.",
        "들을 줄 아는 사람이 현명한 사람입니다.",
        "겸손함이 지혜의 시작입니다.",
        "질문하는 용기가 지혜를 키웁니다.",
    ],
    "행복": [
        "작은 것에서 큰 기쁨을 찾으세요.",
        "오늘 하루를 감사한 마음으로 보내세요.",
        "웃음이 최고의 약입니다.",
        "행복은 마음의 선택입니다.",
        "소중한 사람들과 시간을 나누세요.",
    ],
    "성공": [
        "꾸준함이 성공의 열쇠입니다.",
        "목표를 향한 매일의 노력이 성공을 만듭니다.",
        "실패를 두려워하지 않는 자가 성공합니다.",
        "준비된 자에게 기회가 찾아옵니다.",
        "작은 성취가 큰 성공의 시작입니다.",
    ],
    "사랑": [
        "사랑은 가장 강력한 힘입니다.",
        "진정한 사랑은 서로를 이해하는 것입니다.",
        "사랑하는 마음이 세상을 아름답게 만듭니다.",
        "사랑을 표현하는 것을 두려워하지 마세요.",
        "사랑받기 위해서는 먼저 사랑해야 합니다.",
    ]
}

time_of_day_options = ["morning", "afternoon", "evening", "night", "any"]
season_options = ["spring", "summer", "fall", "winter", "all"]
source_options = ["daily_inspiration", "life_wisdom", "motivational_quotes"]

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME'),
        port=os.getenv('DATABASE_PORT', 5432)
    )

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    schema = os.getenv('DATABASE_SCHEMA', 'public')
    
    # 스키마 생성
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    
    # 테이블 생성
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.messages (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            author TEXT DEFAULT '모닝팀',
            category TEXT NOT NULL,
            time_of_day TEXT,
            season TEXT DEFAULT 'all',
            source TEXT DEFAULT 'daily_inspiration',
            view_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"테이블 {schema}.messages 준비 완료")

def add_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    schema = os.getenv('DATABASE_SCHEMA', 'public')
    total_added = 0
    
    for category, base_messages in categories_messages.items():
        print(f"{category} 카테고리 처리 중...")
        
        # 100개 메시지 생성 (기본 5개를 반복하여 확장)
        messages = []
        for i in range(100):
            base_msg = base_messages[i % len(base_messages)]
            if i >= len(base_messages):
                # 번호를 붙여서 다양화
                messages.append(f"{base_msg} (변형 {i // len(base_messages) + 1})")
            else:
                messages.append(base_msg)
        
        # 데이터베이스에 삽입
        for i, message_text in enumerate(messages):
            message_id = f"{category}_{i+1:03d}"
            time_of_day = random.choice(time_of_day_options)
            season = random.choice(season_options)
            source = random.choice(source_options)
            
            try:
                cursor.execute(f'''
                    INSERT INTO {schema}.messages (
                        id, text, author, category, time_of_day, season, source, view_count, is_active
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                ''', (
                    message_id,
                    message_text,
                    "모닝팀",
                    category,
                    time_of_day,
                    season,
                    source,
                    random.randint(0, 50),
                    True
                ))
                total_added += 1
            except Exception as e:
                print(f"메시지 {message_id} 삽입 실패: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"총 {total_added}개 메시지 추가 완료")
    return total_added

def verify_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    schema = os.getenv('DATABASE_SCHEMA', 'public')
    
    cursor.execute(f"SELECT COUNT(*) FROM {schema}.messages")
    total = cursor.fetchone()[0]
    print(f"총 메시지 수: {total}개")
    
    cursor.execute(f"""
        SELECT category, COUNT(*) 
        FROM {schema}.messages 
        GROUP BY category 
        ORDER BY category
    """)
    
    for category, count in cursor.fetchall():
        print(f"  - {category}: {count}개")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("PostgreSQL에 메시지 추가 시작...")
    print(f"스키마: {os.getenv('DATABASE_SCHEMA', 'public')}")
    
    create_table_if_not_exists()
    add_messages()
    verify_data()
    
    print("완료!")