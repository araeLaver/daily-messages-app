# Node.js 운영 환경용 Dockerfile
FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치 (운영 환경용)
RUN npm ci --only=production

# 애플리케이션 코드 복사
COPY . .

# 사용자 권한 설정
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

# 포트 노출
EXPOSE 3001

# 환경 변수 설정
ENV NODE_ENV=production
ENV PORT=3001

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1

# 애플리케이션 시작
CMD ["npm", "start"]