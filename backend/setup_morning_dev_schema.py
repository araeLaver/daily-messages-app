#!/usr/bin/env python3
"""morning_dev 스키마에 messages 테이블 생성 및 데이터 추가"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def setup_morning_dev():
    print("Setting up morning_dev schema...")
    
    try:
        # DB 연결
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            port=os.getenv('DATABASE_PORT', 5432),
            sslmode='require'
        )
        
        cur = conn.cursor()
        
        # 1. morning_dev 스키마 생성
        cur.execute("CREATE SCHEMA IF NOT EXISTS morning_dev")
        print("morning_dev schema created")
        
        # 2. messages 테이블 생성
        cur.execute("""
            CREATE TABLE IF NOT EXISTS morning_dev.messages (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                author VARCHAR(100) NOT NULL DEFAULT '모닝팀',
                category VARCHAR(50) NOT NULL,
                time_of_day VARCHAR(20),
                season VARCHAR(20) DEFAULT 'all',
                source VARCHAR(50) DEFAULT 'manual',
                view_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("messages table created in morning_dev schema")
        
        # 3. users 테이블도 생성
        cur.execute("""
            CREATE TABLE IF NOT EXISTS morning_dev.users (
                user_id UUID PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("users table created in morning_dev schema")
        
        conn.commit()
        
        # 4. 기존 메시지가 있는지 확인
        cur.execute("SELECT COUNT(*) FROM morning_dev.messages WHERE is_active = true")
        existing_count = cur.fetchone()[0]
        print(f"Existing messages: {existing_count}")
        
        if existing_count == 0:
            print("Adding sample messages...")
            
            # 카테고리별 메시지 데이터
            messages_data = [
                # 동기부여 - 50개
                ("오늘이야말로 당신의 꿈에 한 걸음 더 가까워지는 날입니다.", "동기부여", "morning"),
                ("실패는 성공으로 가는 계단일 뿐입니다. 포기하지 마세요.", "동기부여", "morning"),
                ("당신이 생각하는 것보다 당신은 더 강합니다.", "동기부여", "morning"),
                ("모든 성취는 시도하려는 의지에서 시작됩니다.", "동기부여", "morning"),
                ("오늘의 노력이 내일의 기적을 만듭니다.", "동기부여", "morning"),
                ("어려운 길이지만, 그 끝에는 반드시 보상이 있습니다.", "동기부여", "evening"),
                ("당신의 한계는 당신의 상상력에 의해서만 정해집니다.", "동기부여", "morning"),
                ("매일 조금씩 발전하는 것이 큰 변화를 만듭니다.", "동기부여", "morning"),
                ("성공하는 사람은 포기하지 않는 사람입니다.", "동기부여", "evening"),
                ("오늘 할 수 있는 일을 내일로 미루지 마세요.", "동기부여", "morning"),
                ("당신의 꿈이 두려움보다 크다면 반드시 이룰 수 있습니다.", "동기부여", "morning"),
                ("도전하지 않으면 얻을 수 있는 것도 없습니다.", "동기부여", "morning"),
                ("작은 진전도 진전입니다. 자신을 격려하세요.", "동기부여", "evening"),
                ("불가능해 보이는 일도 시작하면 가능해집니다.", "동기부여", "morning"),
                ("당신의 노력은 결코 헛되지 않습니다.", "동기부여", "evening"),
                ("오늘은 어제보다 더 나은 내가 되는 날입니다.", "동기부여", "morning"),
                ("목표를 향해 한 걸음씩 나아가세요.", "동기부여", "morning"),
                ("당신에게는 무한한 가능성이 있습니다.", "동기부여", "morning"),
                ("실수를 두려워하지 말고 배움의 기회로 삼으세요.", "동기부여", "morning"),
                ("당신의 열정이 길을 만들어 갈 것입니다.", "동기부여", "morning"),
                ("포기하고 싶을 때가 바로 시작하는 때입니다.", "동기부여", "evening"),
                ("당신의 미래는 지금 이 순간의 선택에 달려 있습니다.", "동기부여", "morning"),
                ("어제의 실패가 오늘의 성공을 방해하지 않게 하세요.", "동기부여", "morning"),
                ("당신은 생각보다 많은 것을 할 수 있습니다.", "동기부여", "morning"),
                ("꿈을 꾸는 것을 멈추지 마세요.", "동기부여", "evening"),
                ("매일이 새로운 기회입니다.", "동기부여", "morning"),
                ("당신의 가능성을 믿으세요.", "동기부여", "morning"),
                ("노력하는 당신을 응원합니다.", "동기부여", "morning"),
                ("오늘도 최선을 다하는 당신이 자랑스럽습니다.", "동기부여", "evening"),
                ("당신의 꿈은 이루어질 것입니다.", "동기부여", "morning"),
                ("힘든 시간도 지나갑니다. 견뎌내세요.", "동기부여", "evening"),
                ("당신은 충분히 훌륭합니다.", "동기부여", "morning"),
                ("새로운 도전을 두려워하지 마세요.", "동기부여", "morning"),
                ("당신의 인생은 당신이 주인공입니다.", "동기부여", "morning"),
                ("오늘 하루도 의미있게 보내세요.", "동기부여", "morning"),
                ("당신의 노력이 빛을 발할 날이 올 것입니다.", "동기부여", "evening"),
                ("실패를 성공의 디딤돌로 만드세요.", "동기부여", "morning"),
                ("당신만의 속도로 나아가면 됩니다.", "동기부여", "morning"),
                ("포기하지 않는 한 실패는 없습니다.", "동기부여", "morning"),
                ("당신의 꿈을 향해 용기있게 나아가세요.", "동기부여", "morning"),
                ("오늘도 한 걸음 더 나아갔습니다.", "동기부여", "evening"),
                ("당신의 미래는 밝습니다.", "동기부여", "morning"),
                ("시작이 반입니다. 용기를 내세요.", "동기부여", "morning"),
                ("당신은 할 수 있습니다.", "동기부여", "morning"),
                ("오늘의 작은 노력이 큰 변화를 만듭니다.", "동기부여", "morning"),
                ("당신의 가능성은 무한합니다.", "동기부여", "morning"),
                ("꿈을 포기하지 마세요.", "동기부여", "evening"),
                ("당신의 열정이 길을 밝혀줄 것입니다.", "동기부여", "morning"),
                ("매일 성장하는 당신이 멋집니다.", "동기부여", "evening"),
                ("당신의 목표를 향해 꾸준히 나아가세요.", "동기부여", "morning"),
                
                # 새로운 시작 - 50개
                ("새로운 하루가 시작됩니다. 오늘도 좋은 하루 되세요!", "새로운 시작", "morning"),
                ("모든 새로운 시작에는 희망이 담겨 있습니다.", "새로운 시작", "morning"),
                ("오늘은 어제와 다른 새로운 기회의 날입니다.", "새로운 시작", "morning"),
                ("새로운 시작을 두려워하지 마세요.", "새로운 시작", "morning"),
                ("매일은 새로운 페이지를 쓸 수 있는 기회입니다.", "새로운 시작", "morning"),
                ("오늘부터 다시 시작해도 늦지 않습니다.", "새로운 시작", "morning"),
                ("새로운 도전이 새로운 나를 만듭니다.", "새로운 시작", "morning"),
                ("변화는 새로운 시작의 첫걸음입니다.", "새로운 시작", "morning"),
                ("오늘이라는 선물을 소중히 여기세요.", "새로운 시작", "morning"),
                ("새로운 하루, 새로운 희망을 품어보세요.", "새로운 시작", "morning"),
                ("시작이 있어야 끝도 있습니다.", "새로운 시작", "morning"),
                ("오늘의 시작이 내일의 성공을 만듭니다.", "새로운 시작", "morning"),
                ("새로운 경험이 당신을 성장시킵니다.", "새로운 시작", "morning"),
                ("매 순간이 새로운 출발점입니다.", "새로운 시작", "morning"),
                ("오늘부터 새로운 습관을 만들어보세요.", "새로운 시작", "morning"),
                ("새로운 시작에는 용기가 필요합니다.", "새로운 시작", "morning"),
                ("변화를 두려워하지 말고 받아들이세요.", "새로운 시작", "morning"),
                ("오늘이 인생의 전환점이 될 수 있습니다.", "새로운 시작", "morning"),
                ("새로운 목표를 세우고 시작해보세요.", "새로운 시작", "morning"),
                ("매일 아침이 새로운 기회입니다.", "새로운 시작", "morning"),
                ("과거에 얽매이지 말고 새롭게 시작하세요.", "새로운 시작", "morning"),
                ("오늘의 새로운 시작이 미래를 바꿉니다.", "새로운 시작", "morning"),
                ("새로운 환경이 새로운 가능성을 열어줍니다.", "새로운 시작", "morning"),
                ("시작하는 용기가 가장 중요합니다.", "새로운 시작", "morning"),
                ("오늘부터 더 나은 내가 되어보세요.", "새로운 시작", "morning"),
                ("새로운 시작은 언제나 설렙니다.", "새로운 시작", "morning"),
                ("변화의 바람을 타고 새롭게 출발하세요.", "새로운 시작", "morning"),
                ("오늘의 작은 시작이 큰 변화를 만듭니다.", "새로운 시작", "morning"),
                ("새로운 관점으로 세상을 바라보세요.", "새로운 시작", "morning"),
                ("매일이 새로운 학습의 기회입니다.", "새로운 시작", "morning"),
                ("오늘부터 새로운 꿈을 꾸어보세요.", "새로운 시작", "morning"),
                ("새로운 인연이 새로운 기회를 가져다줍니다.", "새로운 시작", "morning"),
                ("시작하는 마음가짐이 결과를 좌우합니다.", "새로운 시작", "morning"),
                ("오늘의 새로운 시도가 내일의 성과입니다.", "새로운 시작", "morning"),
                ("새로운 길을 걷는 것을 두려워하지 마세요.", "새로운 시작", "morning"),
                ("매 순간 새롭게 태어날 수 있습니다.", "새로운 시작", "morning"),
                ("오늘부터 새로운 버전의 나를 만나보세요.", "새로운 시작", "morning"),
                ("새로운 시작에는 무한한 가능성이 있습니다.", "새로운 시작", "morning"),
                ("변화를 통해 더 나은 내일을 만드세요.", "새로운 시작", "morning"),
                ("오늘이 새로운 인생의 첫 페이지입니다.", "새로운 시작", "morning"),
                ("새로운 하루, 새로운 에너지로 시작하세요.", "새로운 시작", "morning"),
                ("시작하는 순간부터 변화가 일어납니다.", "새로운 시작", "morning"),
                ("오늘의 새로운 도전이 성장의 발판입니다.", "새로운 시작", "morning"),
                ("새로운 시작은 희망의 메시지입니다.", "새로운 시작", "morning"),
                ("매일 새롭게 태어나는 기분으로 살아보세요.", "새로운 시작", "morning"),
                ("오늘부터 새로운 이야기를 써나가세요.", "새로운 시작", "morning"),
                ("새로운 시작이 새로운 행복을 가져다줍니다.", "새로운 시작", "morning"),
                ("변화의 첫걸음을 용기있게 내딛으세요.", "새로운 시작", "morning"),
                ("오늘의 새로운 시작이 미래의 기적입니다.", "새로운 시작", "morning"),
                ("새로운 하루가 선사하는 무한한 가능성을 믿으세요.", "새로운 시작", "morning"),
            ]
            
            # 메시지 삽입
            insert_count = 0
            for text, category, time_of_day in messages_data:
                cur.execute("""
                    INSERT INTO morning_dev.messages (text, author, category, time_of_day, season, source, is_active, view_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (text, "모닝팀", category, time_of_day, "all", "manual", True, 0))
                insert_count += 1
            
            conn.commit()
            print(f"Inserted {insert_count} messages")
        
        # 5. 최종 확인
        cur.execute("SELECT COUNT(*) FROM morning_dev.messages WHERE is_active = true")
        final_count = cur.fetchone()[0]
        
        cur.execute("""
            SELECT category, COUNT(*) 
            FROM morning_dev.messages 
            WHERE is_active = true 
            GROUP BY category 
            ORDER BY category
        """)
        category_counts = cur.fetchall()
        
        print(f"\n=== Setup Complete ===")
        print(f"Total active messages: {final_count}")
        print(f"Messages by category:")
        for cat, count in category_counts:
            print(f"  {cat}: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_morning_dev()