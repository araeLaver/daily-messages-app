require('dotenv').config({ path: `.env.${process.env.NODE_ENV || 'production'}` });
const express = require('express');
const cors = require('cors');
const { Client } = require('pg');

const app = express();
const PORT = process.env.PORT || 3001;

// 미들웨어
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'https://daily-messages-app.netlify.app',
  credentials: true
}));
app.use(express.json());

// 데이터베이스 연결 설정
const dbConfig = {
  host: process.env.DATABASE_HOST,
  user: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  port: process.env.DATABASE_PORT || 5432,
  ssl: {
    rejectUnauthorized: false
  }
};

const DB_SCHEMA = process.env.DATABASE_SCHEMA || 'morning_prod';

// 데이터베이스 연결 풀
const pool = new Client(dbConfig);

// 로그 레벨 설정
const LOG_LEVEL = process.env.LOG_LEVEL || 'info';
const ENABLE_DEBUG = process.env.ENABLE_DEBUG_MODE === 'true';

function log(level, message, data = null) {
  if (level === 'debug' && !ENABLE_DEBUG) return;
  
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${level.toUpperCase()}: ${message}`;
  
  if (data) {
    console.log(logMessage, data);
  } else {
    console.log(logMessage);
  }
}

// 데이터베이스 연결 초기화
async function initializeDB() {
  try {
    await pool.connect();
    log('info', `PostgreSQL 데이터베이스에 연결되었습니다. 스키마: ${DB_SCHEMA}`);
  } catch (error) {
    log('error', '데이터베이스 연결 실패:', error);
    process.exit(1);
  }
}

// API 라우트들

// 1. 홈 - 기본 정보
app.get('/', (req, res) => {
  res.json({
    message: 'Daily Messages API 서버 (Production)',
    version: '2.0.0',
    environment: process.env.NODE_ENV,
    schema: DB_SCHEMA,
    endpoints: {
      '/api/messages/random': '랜덤 명언 가져오기',
      '/api/messages/today': '오늘의 명언 (매일 고정)',
      '/api/categories': '카테고리 목록',
      '/api/messages': '모든 명언 (페이지네이션)',
      '/api/stats': '통계 정보'
    }
  });
});

// 2. 랜덤 명언 가져오기
app.get('/api/messages/random', async (req, res) => {
  try {
    const { category, exclude } = req.query;
    let query = `
      SELECT id, text, author, category, created_at
      FROM ${DB_SCHEMA}.daily_messages 
      WHERE is_active = true
    `;
    const params = [];

    // 카테고리 필터링
    if (category && category !== 'all') {
      query += ` AND category = $${params.length + 1}`;
      params.push(category);
    }

    // 제외할 메시지 ID들 (최근 본 메시지 제외)
    if (exclude) {
      const excludeIds = exclude.split(',').filter(id => id.trim());
      if (excludeIds.length > 0) {
        query += ` AND id NOT IN (${excludeIds.map((_, i) => `$${params.length + i + 1}`).join(',')})`;
        params.push(...excludeIds);
      }
    }

    query += ' ORDER BY RANDOM() LIMIT 1';

    const result = await pool.query(query, params);
    
    if (result.rows.length === 0) {
      // 조건에 맞는 메시지가 없으면 전체에서 랜덤 선택
      const fallbackResult = await pool.query(`
        SELECT id, text, author, category, created_at
        FROM ${DB_SCHEMA}.daily_messages 
        WHERE is_active = true
        ORDER BY RANDOM() 
        LIMIT 1
      `);
      
      log('debug', '랜덤 명언 폴백 사용됨');
      return res.json(fallbackResult.rows[0]);
    }

    log('debug', '랜덤 명언 제공됨', { category, messageId: result.rows[0].id });
    res.json(result.rows[0]);
  } catch (error) {
    log('error', '랜덤 메시지 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 3. 오늘의 명언 (매일 고정)
app.get('/api/messages/today', async (req, res) => {
  try {
    // 오늘 날짜를 기반으로 시드 생성 (매일 동일한 메시지 보장)
    const today = new Date();
    const dateString = today.toISOString().split('T')[0]; // YYYY-MM-DD
    const seed = dateString.split('-').reduce((acc, val) => acc + parseInt(val), 0);

    const result = await pool.query(`
      SELECT id, text, author, category, created_at
      FROM ${DB_SCHEMA}.daily_messages 
      WHERE is_active = true
      ORDER BY (id || '${seed}')::text 
      LIMIT 1
    `);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: '오늘의 메시지를 찾을 수 없습니다.' });
    }

    log('debug', '오늘의 명언 제공됨', { date: dateString, messageId: result.rows[0].id });
    res.json({
      ...result.rows[0],
      isToday: true,
      date: dateString
    });
  } catch (error) {
    log('error', '오늘의 메시지 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 4. 카테고리 목록 가져오기
app.get('/api/categories', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT 
        category as name,
        category as name_ko,
        COUNT(*) as message_count
      FROM ${DB_SCHEMA}.daily_messages 
      WHERE is_active = true AND category IS NOT NULL
      GROUP BY category
      ORDER BY message_count DESC, category
    `);

    const categories = [
      { name: 'all', name_ko: '전체', message_count: null },
      ...result.rows
    ];

    log('debug', '카테고리 목록 제공됨', { count: categories.length });
    res.json(categories);
  } catch (error) {
    log('error', '카테고리 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 5. 모든 명언 가져오기 (페이지네이션)
app.get('/api/messages', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const category = req.query.category;
    const search = req.query.search;
    const offset = (page - 1) * limit;

    let query = `
      SELECT id, text, author, category, created_at
      FROM ${DB_SCHEMA}.daily_messages 
      WHERE is_active = true
    `;
    const params = [];

    // 카테고리 필터
    if (category && category !== 'all') {
      query += ` AND category = $${params.length + 1}`;
      params.push(category);
    }

    // 검색 필터
    if (search) {
      query += ` AND (text ILIKE $${params.length + 1} OR author ILIKE $${params.length + 1})`;
      params.push(`%${search}%`);
    }

    // 정렬 및 페이지네이션
    query += ` ORDER BY created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(limit, offset);

    const result = await pool.query(query, params);

    // 총 개수 조회
    let countQuery = `
      SELECT COUNT(*) 
      FROM ${DB_SCHEMA}.daily_messages 
      WHERE is_active = true
    `;
    const countParams = [];

    if (category && category !== 'all') {
      countQuery += ` AND category = $${countParams.length + 1}`;
      countParams.push(category);
    }

    if (search) {
      countQuery += ` AND (text ILIKE $${countParams.length + 1} OR author ILIKE $${countParams.length + 1})`;
      countParams.push(`%${search}%`);
    }

    const countResult = await pool.query(countQuery, countParams);
    const totalCount = parseInt(countResult.rows[0].count);

    log('debug', '메시지 목록 제공됨', { page, limit, total: totalCount });
    res.json({
      messages: result.rows,
      pagination: {
        page,
        limit,
        total: totalCount,
        totalPages: Math.ceil(totalCount / limit),
        hasNext: page * limit < totalCount,
        hasPrev: page > 1
      }
    });
  } catch (error) {
    log('error', '메시지 목록 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 6. 통계 정보
app.get('/api/stats', async (req, res) => {
  try {
    const [totalResult, categoryResult, recentResult] = await Promise.all([
      // 전체 메시지 수
      pool.query(`SELECT COUNT(*) FROM ${DB_SCHEMA}.daily_messages WHERE is_active = true`),
      
      // 카테고리별 통계
      pool.query(`
        SELECT category, COUNT(*) as count
        FROM ${DB_SCHEMA}.daily_messages 
        WHERE is_active = true AND category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
        LIMIT 10
      `),
      
      // 최근 추가된 메시지 수 (최근 7일)
      pool.query(`
        SELECT COUNT(*) 
        FROM ${DB_SCHEMA}.daily_messages 
        WHERE is_active = true AND created_at >= NOW() - INTERVAL '7 days'
      `)
    ]);

    const stats = {
      totalMessages: parseInt(totalResult.rows[0].count),
      categoriesCount: categoryResult.rows.length,
      topCategories: categoryResult.rows,
      recentMessages: parseInt(recentResult.rows[0].count),
      lastUpdated: new Date().toISOString(),
      environment: process.env.NODE_ENV,
      schema: DB_SCHEMA
    };

    log('debug', '통계 정보 제공됨', stats);
    res.json(stats);
  } catch (error) {
    log('error', '통계 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 7. 즐겨찾기 추가 (향후 확장용)
app.post('/api/favorites', async (req, res) => {
  try {
    const { userId, messageId } = req.body;

    if (!userId || !messageId) {
      return res.status(400).json({ error: '사용자 ID와 메시지 ID가 필요합니다.' });
    }

    await pool.query(`
      INSERT INTO ${DB_SCHEMA}.user_favorites (user_id, message_id, created_at)
      VALUES ($1, $2, CURRENT_TIMESTAMP)
      ON CONFLICT (user_id, message_id) DO NOTHING
    `, [userId, messageId]);

    log('debug', '즐겨찾기 추가됨', { userId, messageId });
    res.json({ success: true, message: '즐겨찾기에 추가되었습니다.' });
  } catch (error) {
    log('error', '즐겨찾기 추가 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// 8. 즐겨찾기 목록 조회
app.get('/api/favorites/:userId', async (req, res) => {
  try {
    const { userId } = req.params;

    const result = await pool.query(`
      SELECT m.id, m.text, m.author, m.category, f.created_at as favorited_at
      FROM ${DB_SCHEMA}.user_favorites f
      JOIN ${DB_SCHEMA}.daily_messages m ON f.message_id = m.id
      WHERE f.user_id = $1 AND m.is_active = true
      ORDER BY f.created_at DESC
    `, [userId]);

    log('debug', '즐겨찾기 목록 제공됨', { userId, count: result.rows.length });
    res.json(result.rows);
  } catch (error) {
    log('error', '즐겨찾기 조회 오류:', error);
    res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
});

// Health Check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV,
    schema: DB_SCHEMA
  });
});

// 에러 핸들링 미들웨어
app.use((err, req, res, next) => {
  log('error', '서버 내부 오류:', err);
  res.status(500).json({ error: '서버 내부 오류가 발생했습니다.' });
});

// 404 핸들러
app.use((req, res) => {
  res.status(404).json({ error: '요청하신 페이지를 찾을 수 없습니다.' });
});

// 서버 시작
async function startServer() {
  try {
    await initializeDB();
    app.listen(PORT, () => {
      log('info', `Daily Messages API 서버가 포트 ${PORT}에서 실행 중입니다.`);
      log('info', `환경: ${process.env.NODE_ENV}`);
      log('info', `스키마: ${DB_SCHEMA}`);
      log('info', `CORS 허용: ${process.env.CORS_ORIGIN}`);
      
      if (ENABLE_DEBUG) {
        log('info', `API 엔드포인트:`);
        log('info', `  GET /api/messages/random - 랜덤 명언`);
        log('info', `  GET /api/messages/today - 오늘의 명언`);
        log('info', `  GET /api/categories - 카테고리 목록`);
        log('info', `  GET /api/stats - 통계 정보`);
        log('info', `  GET /health - 헬스 체크`);
      }
    });
  } catch (error) {
    log('error', '서버 시작 실패:', error);
    process.exit(1);
  }
}

// 종료 처리
process.on('SIGINT', async () => {
  log('info', '서버를 종료하는 중...');
  try {
    await pool.end();
    log('info', '데이터베이스 연결이 종료되었습니다.');
    process.exit(0);
  } catch (error) {
    log('error', '종료 중 오류:', error);
    process.exit(1);
  }
});

process.on('SIGTERM', async () => {
  log('info', '서버를 종료하는 중... (SIGTERM)');
  try {
    await pool.end();
    log('info', '데이터베이스 연결이 종료되었습니다.');
    process.exit(0);
  } catch (error) {
    log('error', '종료 중 오류:', error);
    process.exit(1);
  }
});

startServer();