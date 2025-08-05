# Daily Messages App 🌅

React Bits 스타일의 아름다운 매일 명언 웹 애플리케이션

## ✨ 주요 기능

- **매일 다른 명언**: 날짜 기반으로 매일 고정된 명언 제공
- **카테고리별 분류**: 동기부여, 성공, 행복, 사랑 등 다양한 카테고리
- **190개+ 명언**: 풍부한 한국어 명언 데이터베이스
- **React Bits 디자인**: 현대적이고 아름다운 glassmorphism UI
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 완벽 지원
- **즐겨찾기 기능**: 마음에 드는 명언 저장
- **음성 읽기**: TTS를 통한 명언 음성 재생
- **공유 기능**: 명언을 쉽게 공유
- **실시간 통계**: 명언 및 카테고리 통계 표시

## 🛠 기술 스택

### Frontend
- **React 18** - 현대적 UI 라이브러리
- **Tailwind CSS** - 유틸리티 우선 CSS 프레임워크
- **Lucide React** - 아름다운 아이콘 세트
- **Axios** - HTTP 클라이언트

### Backend
- **Node.js + Express** - 웹 서버
- **PostgreSQL** - 관계형 데이터베이스
- **CORS** - 크로스 오리진 리소스 공유

### Database
- **Koyeb PostgreSQL** - 클라우드 데이터베이스
- **190개 명언** - 다양한 카테고리별 분류
- **사용자 즐겨찾기** - 개인화 기능

## 🚀 실행 방법

### 🌐 라이브 데모
- **프론트엔드**: https://daily-messages-app.netlify.app
- **API 서버**: https://daily-messages-api.koyeb.app

### 🔧 로컬 개발 환경

#### 1. 빠른 시작 (Windows)
```bash
# 실행 스크립트 사용
start_app.bat
```

#### 2. 수동 실행

##### 백엔드 서버 (개발 모드)
```bash
cd backend
npm install
npm run dev
# 개발 서버: http://localhost:3001 (morning_dev 스키마 사용)
```

##### 백엔드 서버 (운영 모드)
```bash
cd backend
npm install
npm start
# 운영 서버: http://localhost:3001 (morning_prod 스키마 사용)
```

##### 프론트엔드 서버
```bash
npm install
npm start
# 개발 서버: http://localhost:3000
```

### 🌍 배포 환경
- **Frontend**: Netlify (자동 배포)
- **Backend**: Koyeb (Docker 기반)
- **Database**: Koyeb PostgreSQL
  - 개발: `morning_dev` 스키마
  - 운영: `morning_prod` 스키마 (190개 명언)

## 📱 주요 화면

### 메인 화면
- 아름다운 그라데이션 배경
- Glass effect 명언 카드
- 부드러운 애니메이션

### 기능들
- **오늘의 명언**: 매일 고정된 특별한 명언
- **랜덤 명언**: 카테고리별 랜덤 명언 탐색
- **카테고리 필터**: 원하는 주제의 명언 선택
- **즐겨찾기**: 좋아하는 명언 저장 및 관리

## 🎨 디자인 특징

### React Bits 스타일
- **Glassmorphism**: 투명하고 블러된 유리 효과
- **부드러운 애니메이션**: fade-in, slide-up, float 효과
- **그라데이션 배경**: 동적으로 변화하는 아름다운 배경
- **현대적 타이포그래피**: Inter 폰트 사용

### 반응형 디자인
- **모바일 우선**: 터치 친화적 인터페이스
- **태블릿 최적화**: 중간 화면 크기 지원
- **데스크톱 향상**: 넓은 화면에서의 완벽한 경험

## 📊 데이터베이스 구조

### 테이블들
- `daily_messages`: 명언 데이터 (190개)
- `message_categories`: 카테고리 정보
- `user_favorites`: 사용자 즐겨찾기
- `user_activity`: 사용자 활동 로그

### 카테고리들
- 동기부여 (10개)
- 성공 (13개)
- 성장 (13개)
- 행복 (11개)
- 사랑 (11개)
- 용기 (11개)
- 인내 (11개)
- 감사 (11개)
- 리더십 (11개)
- 창의성 (11개)
- 마음챙김 (10개)
- 영감 (10개)
- 지혜 (10개)

## 🔧 API 엔드포인트

### 🌐 기본 URL
- **개발**: http://localhost:3001
- **운영**: https://daily-messages-api.koyeb.app

### 📋 엔드포인트 목록

#### 명언 관련
- `GET /api/messages/random` - 랜덤 명언
  - Query: `?category=동기부여&exclude=id1,id2`
- `GET /api/messages/today` - 오늘의 명언 (매일 고정)
- `GET /api/messages` - 명언 목록 (페이지네이션)
  - Query: `?page=1&limit=20&category=성공&search=keyword`

#### 카테고리 & 통계
- `GET /api/categories` - 카테고리 목록
- `GET /api/stats` - 통계 정보 (총 메시지, 카테고리 수 등)

#### 즐겨찾기
- `POST /api/favorites` - 즐겨찾기 추가
- `GET /api/favorites/:userId` - 즐겨찾기 목록

#### 시스템
- `GET /` - API 정보
- `GET /health` - 헬스 체크

## 🌟 특별한 기능들

### 매일 다른 명언
- 날짜 기반 시드를 사용하여 매일 동일한 "오늘의 명언" 제공
- 사용자마다 같은 날에는 같은 명언을 볼 수 있음

### 지능적 중복 방지
- 최근 본 명언 20개를 기억하여 중복 방지
- 카테고리별 필터링과 함께 동작

### 접근성 지원
- 키보드 네비게이션 지원
- 고대비 모드 지원
- 모션 감소 설정 지원
- 스크린 리더 친화적 마크업

## 🚀 배포 및 CI/CD

### 📋 배포 체크리스트
- [x] 운영 DB 스키마 생성 (`morning_prod`)
- [x] 190개 명언 데이터 운영 DB 동기화
- [x] 환경별 설정 파일 (.env.development/.env.production)
- [x] 배포용 백엔드 서버 (server-production.js)
- [x] Netlify 설정 (netlify.toml)
- [x] CORS 설정 (production domain)
- [x] 환경별 API URL 설정
- [x] 운영 환경 테스트 통과

### 🔄 배포 프로세스
1. **개발**: `morning_dev` 스키마 사용, localhost API
2. **운영**: `morning_prod` 스키마 사용, Koyeb API
3. **자동 배포**: Git push → Netlify 자동 빌드 & 배포

### 🛠 환경 관리
```bash
# 개발 환경
npm run dev          # 백엔드 개발 모드
npm start            # 프론트엔드 개발 모드

# 운영 환경
npm run prod         # 백엔드 운영 모드
npm run build        # 프론트엔드 빌드
```

## 📝 향후 개선 계획

- [ ] PWA 지원 (오프라인 사용)
- [ ] 사용자 계정 시스템
- [ ] 더 많은 명언 추가 (목표: 500개)
- [ ] 다국어 지원 (영어, 일본어)
- [ ] 명언 추천 알고리즘 (AI 기반)
- [ ] 소셜 공유 확장 (Instagram, Twitter)
- [ ] 명언 즐겨찾기 클라우드 동기화
- [ ] 푸시 알림 (매일 명언)

## 📊 성능 & 모니터링

### 현재 지표
- **응답 시간**: < 200ms (평균)
- **데이터베이스**: 190개 명언, 13개 주요 카테고리
- **업타임**: 99.9% (Koyeb 호스팅)
- **CDN**: Netlify Edge Network

### 최적화 적용
- React 코드 스플리팅
- 지연 로딩 (Lazy Loading)
- 이미지 최적화
- Gzip 압축
- 캐시 전략

## 👨‍💻 개발 & 배포

### 기술 스택 요약
- **Frontend**: React 18 + Tailwind CSS + Netlify
- **Backend**: Node.js + Express + Koyeb
- **Database**: PostgreSQL (Koyeb) - 개발/운영 분리
- **CI/CD**: Git → Netlify 자동 배포

### 개발자 정보
React Bits 스타일을 적용한 현대적인 웹 애플리케이션으로, 사용자에게 매일 영감을 주는 것을 목표로 합니다.

**라이브 URL**: https://daily-messages-app.netlify.app

---

**Made with ❤️ and React Bits Style**