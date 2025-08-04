# Daily Messages App

매일 새로운 영감과 동기부여 메시지를 제공하는 React 웹 애플리케이션입니다.

## 🌟 주요 기능

- **랜덤 메시지**: 매번 새로운 영감을 주는 메시지
- **카테고리 필터링**: 동기부여, 자신감, 성장, 목표, 행복, 도전 등
- **즐겨찾기 시스템**: 마음에 드는 메시지를 저장하고 관리
- **메시지 복사**: 원클릭으로 클립보드에 복사
- **외부 API 연동**: Quotable.io에서 추가 영어 명언 제공
- **음성 재생**: 브라우저 TTS로 메시지 듣기
- **공유 기능**: 네이티브 공유 API 지원

## 🚀 기술 스택

**Frontend:**
- React 18
- Tailwind CSS
- Lucide React (아이콘)
- Axios (HTTP 클라이언트)

**Backend:**
- FastAPI (Python)
- SQLite 데이터베이스
- 344+ 한국어 메시지

**External APIs:**
- Quotable.io (영어 명언)

## 📦 설치 및 실행

### 프론트엔드
```bash
npm install
npm start
```

### 백엔드
```bash
cd backend
pip install -r requirements.txt
python simple_api.py
```

## 🌐 배포

- **Frontend**: Netlify
- **Backend**: 로컬 또는 클라우드 서버 (포트 8005)

## 📊 데이터베이스

현재 344개의 메시지가 6개 주요 카테고리로 분류되어 있습니다:
- 동기부여: 51개
- 자신감: 51개  
- 성장: 51개
- 목표: 51개
- 행복: 52개
- 도전: 52개

## 🎯 사용법

1. 웹사이트 접속
2. 카테고리 선택 (선택사항)
3. "새로운 메시지" 버튼으로 랜덤 메시지 가져오기
4. 마음에 드는 메시지는 하트 버튼으로 즐겨찾기에 추가
5. 복사 버튼으로 메시지 공유

## 🤖 AI 개발

이 프로젝트는 Claude Code와 함께 개발되었습니다.