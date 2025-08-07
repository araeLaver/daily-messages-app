# 🔧 로컬 개발환경 트러블슈팅 가이드

## 📋 개발 중 발생한 주요 이슈들과 해결방법

### 1. 🚨 카테고리 "로딩중..." 무한 표시 문제

#### 🔍 **증상**
- 프론트엔드에서 카테고리 셀렉트 박스가 계속 "카테고리 로딩 중..." 상태로 고정
- 실제 카테고리 데이터가 로드되지 않음

#### 🎯 **원인**
1. **API 베이스 URL 불일치**
   - 프론트엔드: `localhost:8000`으로 요청
   - 백엔드: `localhost:3002`에서 실행
   - 환경 변수가 제대로 로드되지 않음

2. **데이터 구조 불일치**
   - API가 반환: `{categories: ["전체", "동기부여", ...]}`
   - 프론트엔드가 기대: `[{name: "all", name_ko: "전체", message_count: 0}, ...]`

3. **CORS 설정 누락**
   - 새로운 포트(`localhost:3005`)가 CORS 허용 목록에 없음

#### 💡 **해결방법**

1. **환경 변수 수정**
```env
# .env 파일
PORT=3005
REACT_APP_API_BASE_URL=http://localhost:3002

# .env.development 파일  
REACT_APP_API_BASE_URL=http://localhost:3002
REACT_APP_ENVIRONMENT=development
DB_SCHEMA=morning_dev
```

2. **데이터 구조 변환 코드 추가**
```javascript
// App.jsx에서 API 응답을 프론트엔드 형식으로 변환
const categoryArray = categoryList.categories || categoryList || [];
const formattedCategories = categoryArray.map(cat => ({
  name: cat === '전체' ? 'all' : cat,
  name_ko: cat,
  message_count: statsData?.by_category?.[cat] || 0
}));
setCategories(formattedCategories);
```

3. **CORS 설정 업데이트**
```python
# postgres_api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3005", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

4. **서버 완전 재시작**
```bash
# 기존 프로세스 종료 후 재시작
taskkill /F /IM node.exe
taskkill /F /IM python.exe
npm start
```

---

### 2. 🚨 PostgreSQL 테이블 연결 문제

#### 🔍 **증상**
- API에서 `public.messages` 테이블을 찾지 못함
- "table does not exist" 에러 발생

#### 🎯 **원인**
- 실제 데이터는 `morning_dev.daily_messages` 스키마에 있음
- API 코드가 잘못된 스키마/테이블을 참조

#### 💡 **해결방법**

1. **스키마 확인**
```sql
-- PostgreSQL에서 실제 테이블 위치 확인
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_name LIKE '%message%';
```

2. **API 코드 수정**
```python
# 환경에 따른 스키마 동적 선택
schema = os.getenv('DB_SCHEMA', 'morning_prod')
query = f"SELECT id, text, category, author FROM {schema}.daily_messages WHERE is_active = true"
```

3. **환경 변수로 스키마 관리**
```bash
# 개발 환경
set DB_SCHEMA=morning_dev

# 운영 환경  
set DB_SCHEMA=morning_prod
```

---

### 3. 🚨 포트 충돌 문제

#### 🔍 **증상**
- "Something is already running on port 3000/3001" 에러
- 서버 시작 실패

#### 🎯 **원인**
- 이전에 실행된 프로세스가 완전히 종료되지 않음
- 포트가 계속 점유된 상태

#### 💡 **해결방법**

1. **프로세스 확인 및 종료**
```bash
# 포트 사용 프로세스 확인
netstat -ano | findstr :3000
netstat -ano | findstr :3002

# 프로세스 강제 종료
taskkill /F /PID [프로세스ID]

# 또는 모든 Node.js/Python 프로세스 종료
taskkill /F /IM node.exe
taskkill /F /IM python.exe
```

2. **다른 포트 사용**
```env
# .env 파일에서 포트 변경
PORT=3005
```

---

### 4. 🚨 Mock 데이터 사용 문제

#### 🔍 **증상**
- 실제 데이터베이스 데이터가 아닌 하드코딩된 메시지만 표시
- "오늘도 새로운 기회가 당신을 기다리고 있습니다." 고정 메시지

#### 🎯 **원인**
- API 연결 실패 시 fallback으로 mock 데이터 사용
- 실제 API 서버가 실행되지 않음

#### 💡 **해결방법**

1. **API 서버 상태 확인**
```bash
# API 서버 실행 확인
python test_api.py

# 직접 API 테스트
curl http://localhost:3002/api/categories
curl http://localhost:3002/api/messages/random
```

2. **실제 데이터 연결 확인**
```javascript
// 브라우저 개발자 도구에서 실행
fetch('http://localhost:3002/api/categories')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

---

### 5. 🚨 한글 인코딩 문제

#### 🔍 **증상**
- 데이터베이스에서 한글이 깨져서 표시
- "���" 같은 문자로 보임

#### 🎯 **원인**
- Windows 콘솔 인코딩 문제
- UTF-8 설정 누락

#### 💡 **해결방법**

1. **콘솔 인코딩 설정**
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
```

2. **PostgreSQL 연결시 인코딩 명시**
```python
conn = psycopg2.connect(
    host='...',
    user='...',
    password='...',
    database='...',
    client_encoding='utf8'
)
```

---

## 🔧 일반적인 디버깅 단계

### 1. 환경 확인
```bash
# 환경 변수 확인
echo %REACT_APP_API_BASE_URL%

# 프로세스 확인
tasklist | findstr node
tasklist | findstr python

# 포트 확인
netstat -ano | findstr :3002
netstat -ano | findstr :3005
```

### 2. API 연결 테스트
```bash
# 헬스체크
curl http://localhost:3002/health

# 카테고리 확인
curl http://localhost:3002/api/categories

# 랜덤 메시지 확인
curl http://localhost:3002/api/messages/random
```

### 3. 로그 확인
- 브라우저 개발자 도구 → Console 탭
- 네트워크 탭에서 실제 API 요청/응답 확인
- 백엔드 콘솔에서 에러 로그 확인

### 4. 완전 재시작 절차
```bash
# 1. 모든 프로세스 종료
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# 2. 백엔드 시작
cd backend
set DB_SCHEMA=morning_dev
python postgres_api.py

# 3. 프론트엔드 시작 (다른 터미널에서)
set REACT_APP_API_BASE_URL=http://localhost:3002
npm start
```

---

## 🎯 체크리스트

### ✅ 서버 시작 전 확인사항
- [ ] PostgreSQL 데이터베이스 연결 가능
- [ ] 환경 변수 올바르게 설정
- [ ] 포트 충돌 없음
- [ ] 필요한 패키지 설치됨

### ✅ 프론트엔드 연결 확인
- [ ] API 베이스 URL 올바름 (`http://localhost:3002`)
- [ ] CORS 설정에 프론트엔드 포트 포함됨
- [ ] 브라우저에서 API 직접 접근 가능

### ✅ 데이터 확인
- [ ] `morning_dev.daily_messages` 테이블에 1505개 데이터 존재
- [ ] 15개 카테고리 정상 조회
- [ ] 한글 인코딩 정상

---

**💡 추가 도움이 필요한 경우**
1. 브라우저 개발자 도구(F12) → Console에서 에러 메시지 확인
2. 네트워크 탭에서 실제 API 요청 상태 확인  
3. `debug_console.html` 페이지에서 API 연결 테스트 수행