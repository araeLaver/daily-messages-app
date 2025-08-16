# Daily Messages API Backend

SQLite 기반 명언 API 서버

## Features
- 랜덤 명언 제공
- 오늘의 명언 (매일 고정)
- 카테고리별 필터링
- 통계 정보
- SQLite 데이터베이스

## API Endpoints
- GET `/api/messages/random` - 랜덤 명언
- GET `/api/messages/today` - 오늘의 명언
- GET `/api/categories` - 카테고리 목록
- GET `/api/stats` - 통계
- GET `/api/messages` - 모든 명언 (페이지네이션)

## Deployment
Railway에 배포 가능

## Start
```bash
npm install
npm start
```