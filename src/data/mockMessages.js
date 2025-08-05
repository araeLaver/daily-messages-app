// 임시 메시지 데이터 (API 서버 없을 때 사용)
export const mockMessages = [
  {
    id: 1,
    text: "성공의 비결은 준비와 기회가 만나는 것이다.",
    author: "세네카",
    category: "성공"
  },
  {
    id: 2,
    text: "당신이 할 수 있다고 생각하든 할 수 없다고 생각하든, 당신이 옳다.",
    author: "헨리 포드",
    category: "동기부여"
  },
  {
    id: 3,
    text: "행복은 선택이다. 매일 아침 당신이 내리는 선택이다.",
    author: "웨인 다이어",
    category: "행복"
  },
  {
    id: 4,
    text: "가장 큰 영광은 넘어지지 않는 것이 아니라, 넘어질 때마다 일어서는 것이다.",
    author: "공자",
    category: "용기"
  },
  {
    id: 5,
    text: "변화를 두려워하지 마라. 변화 없이는 성장도 없다.",
    author: "벤자민 프랭클린",
    category: "성장"
  },
  {
    id: 6,
    text: "사랑받기를 원한다면 먼저 사랑하라.",
    author: "세네카",
    category: "사랑"
  },
  {
    id: 7,
    text: "인내는 쓰지만 그 열매는 달다.",
    author: "아리스토텔레스",
    category: "인내"
  },
  {
    id: 8,
    text: "감사하는 마음이 있는 곳에 행복이 자란다.",
    author: "달라이 라마",
    category: "감사"
  },
  {
    id: 9,
    text: "리더는 희망을 파는 상인이다.",
    author: "나폴레옹 보나파르트",
    category: "리더십"
  },
  {
    id: 10,
    text: "창의성은 지식보다 중요하다.",
    author: "알베르트 아인슈타인",
    category: "창의성"
  },
  {
    id: 11,
    text: "현재 순간에 집중하라. 그것이 유일한 실재이다.",
    author: "부처",
    category: "마음챙김"
  },
  {
    id: 12,
    text: "영감은 준비된 마음에게 찾아온다.",
    author: "루이 파스퇴르",
    category: "영감"
  },
  {
    id: 13,
    text: "지혜는 경험의 딸이다.",
    author: "레오나르도 다 빈치",
    category: "지혜"
  },
  {
    id: 14,
    text: "꿈을 포기하지 마라. 꿈이 사라지면 사는 것은 의미를 잃는다.",
    author: "마크 트웨인",
    category: "동기부여"
  },
  {
    id: 15,
    text: "실패는 성공으로 가는 계단이다.",
    author: "윈스턴 처칠",
    category: "성공"
  },
  {
    id: 16,
    text: "어제보다 나은 사람이 되기 위해 노력하라.",
    author: "공자",
    category: "성장"
  },
  {
    id: 17,
    text: "행복은 목적지가 아니라 여행하는 방식이다.",
    author: "마가렛 리 런벡",
    category: "행복"
  },
  {
    id: 18,
    text: "진정한 사랑은 서로를 바라보는 것이 아니라 같은 방향을 바라보는 것이다.",
    author: "생텍쥐페리",
    category: "사랑"
  },
  {
    id: 19,
    text: "용기란 두려움이 없는 것이 아니라 두려움에도 불구하고 행동하는 것이다.",
    author: "넬슨 만델라",
    category: "용기"
  },
  {
    id: 20,
    text: "참는 자는 이긴다.",
    author: "한국 속담",
    category: "인내"
  },
  {
    id: 21,
    text: "작은 것에도 감사할 줄 아는 사람이 큰것을 얻는다.",
    author: "탈무드",
    category: "감사"
  },
  {
    id: 22,
    text: "진정한 리더는 다른 리더를 만든다.",
    author: "톰 피터스",
    category: "리더십"
  },
  {
    id: 23,
    text: "상상력은 지식보다 중요하다. 지식은 한정되어 있지만 상상력은 세계를 포용한다.",
    author: "알베르트 아인슈타인",
    category: "창의성"
  },
  {
    id: 24,
    text: "지금 이 순간이 당신의 인생이다.",
    author: "오마르 카얌",
    category: "마음챙김"
  },
  {
    id: 25,
    text: "영감은 기다리는 것이 아니라 만들어가는 것이다.",
    author: "잭 런던",
    category: "영감"
  },
  {
    id: 26,
    text: "지혜는 많이 아는 것이 아니라 올바르게 아는 것이다.",
    author: "아이스킬로스",
    category: "지혜"
  },
  {
    id: 27,
    text: "불가능이란 단어는 내 사전에 없다.",
    author: "나폴레옹",
    category: "동기부여"
  },
  {
    id: 28,
    text: "성공하려면 먼저 실패할 용기가 있어야 한다.",
    author: "스티브 잡스",
    category: "성공"
  }
];

export const mockCategories = [
  { name: 'all', name_ko: '전체', message_count: 28 },
  { name: '동기부여', name_ko: '동기부여', message_count: 3 },
  { name: '성공', name_ko: '성공', message_count: 3 },
  { name: '성장', name_ko: '성장', message_count: 2 },
  { name: '행복', name_ko: '행복', message_count: 2 },  
  { name: '사랑', name_ko: '사랑', message_count: 2 },
  { name: '용기', name_ko: '용기', message_count: 2 },
  { name: '인내', name_ko: '인내', message_count: 2 },
  { name: '감사', name_ko: '감사', message_count: 2 },
  { name: '리더십', name_ko: '리더십', message_count: 2 },
  { name: '창의성', name_ko: '창의성', message_count: 2 },
  { name: '마음챙김', name_ko: '마음챙김', message_count: 2 },
  { name: '영감', name_ko: '영감', message_count: 2 },
  { name: '지혜', name_ko: '지혜', message_count: 2 }
];