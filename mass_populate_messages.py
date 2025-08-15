#!/usr/bin/env python3
import psycopg2
import uuid
from datetime import datetime
import random

DATABASE_CONFIG = {
    'host': 'ep-blue-unit-a2ev3s9x.eu-central-1.pg.koyeb.app',
    'database': 'untab',
    'user': 'untab', 
    'password': '0AbVNOIsl2dn',
    'port': 5432
}

def mass_populate():
    # 각 카테고리별 기본 템플릿과 저자들
    templates = {
        "동기부여": {
            "authors": ["나폴레온 힐", "데일 카네기", "짐 론", "브라이언 트레이시", "앤서니 로빈스"],
            "bases": [
                "당신의 꿈은 포기하지 않는 한 살아있습니다",
                "성공은 준비된 자에게 찾아오는 기회입니다", 
                "오늘의 노력이 내일의 성과를 만듭니다",
                "실패는 성공으로 가는 단계입니다",
                "당신은 생각보다 더 강한 사람입니다"
            ]
        },
        "긍정": {
            "authors": ["노먼 빈센트 필", "루이즈 헤이", "오푸라 윈프리", "웨인 다이어"],
            "bases": [
                "긍정적인 생각이 긍정적인 현실을 만듭니다",
                "매일 아침 감사할 일을 하나씩 생각해보세요",
                "당신의 미소가 세상을 밝게 만듭니다",
                "좋은 일은 좋은 마음에서 시작됩니다",
                "행복은 선택이며 당신이 그 선택의 주인입니다"
            ]
        },
        "성공": {
            "authors": ["스티브 잡스", "빌 게이츠", "워렌 버핏", "잭 웰치", "일론 머스크"],
            "bases": [
                "성공의 비밀은 꾸준한 노력과 인내입니다",
                "성공한 사람들은 실패를 두려워하지 않습니다", 
                "목표를 세우고 계획을 실행하는 것이 성공의 열쇠입니다",
                "성공은 다른 사람을 돕는 것에서 시작됩니다",
                "성공은 과정이며 목적지가 아닙니다"
            ]
        },
        "행복": {
            "authors": ["달라이 라마", "틱낫한", "마틴 셀리그만", "브레네 브라운"],
            "bases": [
                "행복은 여행의 방식이지 목적지가 아닙니다",
                "작은 것에서 큰 기쁨을 찾는 것이 행복의 비밀입니다",
                "현재 순간에 집중하면 행복이 찾아옵니다",
                "행복은 다른 사람과 나눌 때 더욱 커집니다",
                "감사하는 마음이 행복의 문을 엽니다"
            ]
        },
        "건강": {
            "authors": ["히포크라테스", "딥초프라", "앤드루 웨일", "마이클 그리거"],
            "bases": [
                "건강한 몸에 건강한 정신이 깃듭니다",
                "운동은 몸과 마음을 위한 최고의 명상입니다",
                "균형 잡힌 식사가 건강한 삶의 기초입니다",
                "충분한 수면은 건강의 첫 번째 조건입니다",
                "예방이 치료보다 중요합니다"
            ]
        }
    }
    
    # 문장 변형용 접두사/접미사
    prefixes = ["오늘", "지금", "매일", "항상", "새롭게", "다시", "언제나"]
    suffixes = ["하세요", "해보세요", "시작하세요", "기억하세요", "실천하세요", "믿으세요"]
    
    conn = None
    try:
        print("데이터베이스 연결 중...")
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        total_added = 0
        
        for category, data in templates.items():
            print(f"\n'{category}' 카테고리 처리 중...")
            
            # 현재 개수 확인  
            cursor.execute("""
                SELECT COUNT(*) FROM morning_prod.daily_messages 
                WHERE category = %s AND is_active = true
            """, (category,))
            current_count = cursor.fetchone()[0]
            
            need_count = max(0, 150 - current_count)
            print(f"  현재: {current_count}개, 필요: {need_count}개")
            
            if need_count <= 0:
                continue
                
            # 메시지 생성 및 추가
            added_count = 0
            for i in range(need_count):
                base_msg = random.choice(data['bases'])
                author = random.choice(data['authors'])
                
                # 문장 변형
                if random.choice([True, False]):
                    text = f"{random.choice(prefixes)} {base_msg.lower()}"
                else:
                    text = f"{base_msg}. {random.choice(suffixes)}."
                
                # 번호 추가로 유니크하게
                text = f"{text} ({i+1})"
                
                message_id = str(uuid.uuid4())
                
                try:
                    cursor.execute("""
                        INSERT INTO morning_prod.daily_messages 
                        (id, text, author, category, is_active, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (message_id, text, author, category, True, datetime.now(), datetime.now()))
                    
                    added_count += 1
                    if added_count % 20 == 0:
                        print(f"  {added_count}개 추가됨...")
                        
                except Exception as e:
                    print(f"  오류 (건너뛰기): {e}")
                    continue
            
            total_added += added_count
            print(f"  '{category}' 완료: {added_count}개 추가")
        
        conn.commit()
        print(f"\n[완료] 총 {total_added}개 메시지 추가!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"전체 오류: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    mass_populate()