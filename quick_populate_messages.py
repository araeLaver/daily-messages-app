#!/usr/bin/env python3
import psycopg2
import uuid
from datetime import datetime
import random

# 데이터베이스 연결 정보
DATABASE_CONFIG = {
    'host': 'ep-blue-unit-a2ev3s9x.eu-central-1.pg.koyeb.app',
    'database': 'untab',
    'user': 'untab', 
    'password': '0AbVNOIsl2dn',
    'port': 5432
}

def quick_populate():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        print("[시작] 주요 카테고리에 메시지 빠르게 추가...")
        
        # 주요 카테고리들과 간단한 메시지 템플릿
        categories = {
            "동기부여": ["나폴레온 힐", "데일 카네기", "짐 론"],
            "긍정": ["노먼 빈센트 필", "루이즈 헤이", "웨인 다이어"], 
            "성공": ["잭 웰치", "워렌 버핏", "스티브 잡스"],
            "행복": ["달라이 라마", "틱낫한", "오푸라 윈프리"],
            "건강": ["딥초프라", "앤드루 웨일", "마이클 그리거"],
            "지혜": ["공자", "소크라테스", "아인슈타인"],
            "창의성": ["스티브 잡스", "파블로 피카소", "레오나르도 다 빈치"],
            "도전": ["넬슨 만델라", "테디 루즈벨트", "헬렌 켈러"],
            "감사": ["오푸라 윈프리", "브레네 브라운", "로버트 에먼스"],
            "평화": ["달라이 라마", "틱낫한", "마더 테레사"]
        }
        
        base_messages = [
            "오늘은 새로운 기회의 날입니다.",
            "당신의 꿈을 믿고 나아가세요.",
            "작은 발걸음도 큰 변화의 시작입니다.",
            "긍정적인 마음으로 하루를 시작하세요.",
            "성공은 준비된 자에게 찾아옵니다.",
            "행복은 마음의 선택입니다.",
            "건강한 몸과 마음을 위해 노력하세요.",
            "지혜는 경험에서 나옵니다.",
            "창의적인 사고로 문제를 해결하세요.",
            "도전을 두려워하지 마세요.",
            "감사하는 마음이 풍요를 가져다줍니다.",
            "내면의 평화를 찾으세요.",
            "매일 조금씩 발전하는 것이 중요합니다.",
            "자신을 믿고 전진하세요.",
            "실패는 성공의 어머니입니다."
        ]
        
        total_added = 0
        batch_size = 50
        
        for category, authors in categories.items():
            print(f"\n'{category}' 카테고리 처리중...")
            
            # 현재 개수 확인
            cursor.execute("""
                SELECT COUNT(*) FROM morning_prod.daily_messages 
                WHERE category = %s AND is_active = true
            """, (category,))
            current_count = cursor.fetchone()[0]
            
            need_count = max(0, 150 - current_count)
            print(f"  현재: {current_count}개, 추가 필요: {need_count}개")
            
            if need_count <= 0:
                continue
                
            # 배치로 데이터 생성
            messages_to_insert = []
            for i in range(need_count):
                message_id = str(uuid.uuid4())
                text = f"{category} - {random.choice(base_messages)} {i+1}번째 메시지입니다."
                author = random.choice(authors)
                
                messages_to_insert.append((
                    message_id, text, author, category, True,
                    random.randint(0, 30), random.randint(0, 100),
                    datetime.now(), datetime.now()
                ))
                
                # 배치 사이즈마다 실행
                if len(messages_to_insert) >= batch_size:
                    cursor.executemany("""
                        INSERT INTO morning_prod.daily_messages 
                        (id, text, author, category, is_active, reaction_count, view_count, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, messages_to_insert)
                    
                    total_added += len(messages_to_insert)
                    messages_to_insert = []
                    print(f"  {total_added}개 추가됨...")
            
            # 남은 메시지 처리
            if messages_to_insert:
                cursor.executemany("""
                    INSERT INTO morning_prod.daily_messages 
                    (id, text, author, category, is_active, reaction_count, view_count, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, messages_to_insert)
                total_added += len(messages_to_insert)
        
        # 커밋
        conn.commit()
        print(f"\n[완료] 총 {total_added}개의 메시지가 추가되었습니다!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] {e}")
        if conn:
            conn.rollback()

if __name__ == "__main__":
    quick_populate()