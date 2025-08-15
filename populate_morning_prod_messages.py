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

# 주요 카테고리별 메시지 템플릿 (각 카테고리별로 150개 이상 생성)
CATEGORY_MESSAGES = {
    "동기부여": {
        "authors": ["앤서니 로빈스", "짐 론", "브라이언 트레이시", "스티븐 코비", "데일 카네기", "나폴레온 힐", "토니 로빈스"],
        "messages": [
            "오늘은 어제보다 더 나은 당신이 될 수 있는 완벽한 날입니다.",
            "성공은 준비와 기회가 만나는 지점에서 탄생합니다.",
            "당신의 꿈은 당신이 포기하지 않는 한 절대 죽지 않습니다.",
            "매일 조금씩 발전하는 것이 큰 변화를 만드는 비밀입니다.",
            "실패는 성공으로 가는 디딤돌일 뿐입니다.",
            "당신의 한계는 당신이 정하는 것입니다.",
            "오늘의 노력이 내일의 성과를 만듭니다.",
            "불가능은 단지 의견일 뿐입니다.",
            "당신이 믿는 만큼 이룰 수 있습니다.",
            "작은 발걸음도 꾸준히 하면 목적지에 도달합니다."
        ]
    },
    "긍정": {
        "authors": ["노먼 빈센트 필", "루이즈 헤이", "웨인 다이어", "오프라 윈프리", "아리아나 허핑턴"],
        "messages": [
            "긍정적인 생각은 긍정적인 결과를 만들어냅니다.",
            "매일 아침 감사할 일을 생각하며 하루를 시작하세요.",
            "당신의 마음이 평화로우면 세상도 평화롭게 보입니다.",
            "웃음은 마음의 약입니다.",
            "오늘도 아름다운 하루가 될 것입니다.",
            "행복은 선택입니다. 오늘 행복을 선택하세요.",
            "당신 안에는 무한한 가능성이 있습니다.",
            "좋은 일은 좋은 생각에서 시작됩니다.",
            "매 순간이 새로운 시작의 기회입니다.",
            "당신의 미소가 세상을 밝게 만듭니다."
        ]
    },
    "성공": {
        "authors": ["잭 웰치", "워렌 버핏", "빌 게이츠", "스티브 잡스", "일론 머스크", "제프 베조스"],
        "messages": [
            "성공하기 위해서는 먼저 성공할 준비를 해야 합니다.",
            "성공은 하루 아침에 이루어지지 않습니다.",
            "성공한 사람들은 실패를 두려워하지 않습니다.",
            "목표를 세우고 계획을 세우며 실행하세요.",
            "성공의 열쇠는 지속적인 학습입니다.",
            "성공은 준비된 자에게 온다.",
            "성공하려면 먼저 실패할 용기가 있어야 합니다.",
            "성공의 90%는 그냥 나타나는 것입니다.",
            "성공은 과정이지 목적지가 아닙니다.",
            "성공은 다른 사람을 돕는 것에서 시작됩니다."
        ]
    },
    "행복": {
        "authors": ["달라이 라마", "틱낫한", "마틴 셀리그만", "소냐 류보머스키"],
        "messages": [
            "행복은 목적지가 아니라 여행하는 방식입니다.",
            "작은 것에서 큰 기쁨을 찾으세요.",
            "행복은 다른 사람과 나누면 더 커집니다.",
            "현재 순간에 집중하면 행복이 찾아옵니다.",
            "행복은 내면에서 나옵니다.",
            "감사하는 마음이 행복의 시작입니다.",
            "행복은 선택의 문제입니다.",
            "단순함 속에서 행복을 찾으세요.",
            "행복은 완벽함이 아니라 충족감입니다.",
            "행복한 사람은 다른 사람을 행복하게 만듭니다."
        ]
    },
    "건강": {
        "authors": ["딥초프라", "앤드루 웨일", "마이클 그리거", "데이비드 펄머터"],
        "messages": [
            "건강한 몸에 건강한 정신이 깃듭니다.",
            "운동은 몸과 마음을 위한 최고의 약입니다.",
            "충분한 수면은 건강의 기본입니다.",
            "균형 잡힌 식사가 건강한 삶의 시작입니다.",
            "물을 충분히 마시는 것만으로도 건강이 좋아집니다.",
            "스트레스 관리는 건강관리의 핵심입니다.",
            "규칙적인 생활습관이 건강을 만듭니다.",
            "건강은 돈으로 살 수 없는 가장 큰 자산입니다.",
            "예방이 치료보다 중요합니다.",
            "몸의 소리에 귀 기울이세요."
        ]
    },
    "지혜": {
        "authors": ["공자", "소크라테스", "아인슈타인", "부처", "랄프 왈도 에머슨"],
        "messages": [
            "아는 것은 아는 것이고 모르는 것은 모르는 것이니, 이것이 앎이다.",
            "배움은 평생에 걸친 여행입니다.",
            "지혜는 경험에서 나옵니다.",
            "질문하는 것이 답을 찾는 시작입니다.",
            "실수로부터 배우는 것이 가장 큰 지혜입니다.",
            "겸손함이 지혜의 시작입니다.",
            "지혜로운 사람은 말보다 행동으로 보여줍니다.",
            "과거에서 배우고 현재에 집중하며 미래를 준비하세요.",
            "지혜는 나이가 아니라 경험의 깊이에서 나옵니다.",
            "진정한 지혜는 자신의 무지를 아는 것입니다."
        ]
    },
    "창의성": {
        "authors": ["파블로 피카소", "레오나르도 다 빈치", "스티브 잡스", "월트 디즈니"],
        "messages": [
            "창의성은 연결하는 것입니다.",
            "상상력은 지식보다 중요합니다.",
            "모든 창의적 행위는 파괴 행위입니다.",
            "창의성은 용기가 필요합니다.",
            "제약이 있을 때 창의성이 꽃핍니다.",
            "다르게 생각하세요.",
            "창의성은 실패를 두려워하지 않습니다.",
            "새로운 아이디어는 기존의 것들을 새롭게 조합하는 것입니다.",
            "창의성은 호기심에서 시작됩니다.",
            "완벽함을 추구하면 창의성이 죽습니다."
        ]
    },
    "도전": {
        "authors": ["테디 루즈벨트", "넬슨 만델라", "헬렌 켈러", "마하트마 간디"],
        "messages": [
            "도전하지 않으면 얻을 수 없습니다.",
            "안전지대를 벗어나야 성장할 수 있습니다.",
            "도전은 인생을 흥미롭게 만들고, 극복하는 것은 인생을 의미있게 만듭니다.",
            "가장 큰 위험은 위험을 감수하지 않는 것입니다.",
            "어려움은 기회로 가장한 축복입니다.",
            "도전 없이는 변화도 없습니다.",
            "두려움을 느낀다면 그것이 바로 해야 할 일입니다.",
            "도전은 능력을 발견하게 해줍니다.",
            "편안함은 성장의 적입니다.",
            "도전을 피하면 기회도 놓치게 됩니다."
        ]
    },
    "감사": {
        "authors": ["오푸라 윈프리", "브레네 브라운", "멜로디 비티", "로버트 에먼스"],
        "messages": [
            "감사는 풍요로움을 가져다줍니다.",
            "감사할 일을 찾으면 더 많은 감사할 일이 생깁니다.",
            "감사는 마음의 기억입니다.",
            "감사하는 마음은 행복의 열쇠입니다.",
            "작은 것에 감사하면 큰 것도 받게 됩니다.",
            "감사는 현재를 충분하게 만듭니다.",
            "감사하는 마음은 모든 것을 변화시킵니다.",
            "감사는 삶을 풍요롭게 만드는 마법입니다.",
            "감사할 줄 아는 사람은 더 많은 복을 받습니다.",
            "매일 감사 일기를 써보세요."
        ]
    },
    "평화": {
        "authors": ["달라이 라마", "틱낫한", "마더 테레사", "간디"],
        "messages": [
            "평화는 내면에서 시작됩니다.",
            "마음이 평화로우면 모든 것이 평화롭습니다.",
            "평화는 목적지가 아니라 여행하는 방식입니다.",
            "내면의 평화가 외부의 평화를 만듭니다.",
            "평화는 분노의 부재가 아니라 정의의 존재입니다.",
            "평화로운 마음은 가장 큰 축복입니다.",
            "평화는 선택입니다.",
            "평화는 힘이며, 약함이 아닙니다.",
            "평화는 조화로운 관계에서 나옵니다.",
            "평화는 용서에서 시작됩니다."
        ]
    }
}

def generate_message_variants(base_messages, target_count=150):
    """기본 메시지들을 변형하여 목표 개수만큼 생성"""
    variants = []
    
    # 메시지 변형 패턴들
    prefixes = [
        "오늘은", "지금 이 순간", "새로운 하루에", "이 아침에", "매일", "항상",
        "지금부터", "오늘부터", "새롭게", "다시 한번", "언제나", "늘"
    ]
    
    suffixes = [
        "기억하세요", "명심하세요", "생각해보세요", "시작하세요", "도전하세요",
        "믿으세요", "실천하세요", "꿈꾸세요", "노력하세요", "집중하세요"
    ]
    
    connectors = [
        "그리고", "또한", "특히", "무엇보다", "더욱이", "게다가"
    ]
    
    # 기본 메시지들을 그대로 추가
    variants.extend(base_messages)
    
    # 변형 메시지 생성
    while len(variants) < target_count:
        base_msg = random.choice(base_messages)
        
        # 여러 변형 방법 적용
        variation_type = random.choice(['prefix', 'suffix', 'both', 'connector'])
        
        if variation_type == 'prefix':
            new_msg = f"{random.choice(prefixes)} {base_msg.lower()}"
        elif variation_type == 'suffix':
            new_msg = f"{base_msg} {random.choice(suffixes)}."
        elif variation_type == 'both':
            new_msg = f"{random.choice(prefixes)} {base_msg.lower()} {random.choice(suffixes)}."
        elif variation_type == 'connector':
            connector = random.choice(connectors)
            additional = random.choice(base_messages)
            new_msg = f"{base_msg} {connector} {additional.lower()}"
        
        # 중복 방지
        if new_msg not in variants and len(new_msg) < 500:
            variants.append(new_msg)
    
    return variants[:target_count]

def populate_messages():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        print("[시작] morning_prod 스키마에 메시지 추가 작업 시작...")
        
        total_added = 0
        
        for category, data in CATEGORY_MESSAGES.items():
            print(f"\n[작업중] '{category}' 카테고리 처리중...")
            
            # 현재 카테고리의 메시지 수 확인
            cursor.execute("""
                SELECT COUNT(*) FROM morning_prod.daily_messages 
                WHERE category = %s AND is_active = true
            """, (category,))
            current_count = cursor.fetchone()[0]
            
            target_count = 150
            need_count = max(0, target_count - current_count)
            
            print(f"  - 현재: {current_count}개, 목표: {target_count}개, 추가 필요: {need_count}개")
            
            if need_count <= 0:
                print(f"  - '{category}' 카테고리는 이미 충분한 메시지가 있습니다.")
                continue
            
            # 메시지 생성
            messages = generate_message_variants(data['messages'], need_count)
            authors = data['authors']
            
            # 데이터베이스에 추가
            added_count = 0
            for i in range(need_count):
                message_id = str(uuid.uuid4())
                text = messages[i % len(messages)]
                author = random.choice(authors)
                
                # 중복 체크 (동일한 텍스트가 이미 있는지 확인)
                cursor.execute("""
                    SELECT id FROM morning_prod.daily_messages 
                    WHERE text = %s AND category = %s
                """, (text, category))
                
                if cursor.fetchone():
                    continue  # 중복이면 건너뛰기
                
                # 메시지 추가
                cursor.execute("""
                    INSERT INTO morning_prod.daily_messages 
                    (id, text, author, category, is_active, reaction_count, view_count, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    message_id,
                    text,
                    author,
                    category,
                    True,
                    random.randint(0, 50),
                    random.randint(0, 200),
                    datetime.now(),
                    datetime.now()
                ))
                
                added_count += 1
                
                if added_count >= need_count:
                    break
            
            print(f"  - '{category}' 카테고리에 {added_count}개 메시지 추가됨")
            total_added += added_count
        
        # 변경사항 커밋
        conn.commit()
        print(f"\n[완료] 총 {total_added}개의 메시지가 추가되었습니다.")
        
        # 최종 상태 확인
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM morning_prod.daily_messages 
            WHERE is_active = true
            GROUP BY category 
            ORDER BY count DESC;
        """)
        
        final_counts = cursor.fetchall()
        print(f"\n[결과] 카테고리별 최종 메시지 개수:")
        for category, count in final_counts:
            print(f"  - {category}: {count}개")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] 작업 중 오류 발생: {e}")
        if conn:
            conn.rollback()

if __name__ == "__main__":
    populate_messages()