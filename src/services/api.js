import axios from 'axios';
import { mockMessages, mockCategories } from '../data/mockMessages';

// 로컬 개발시에는 localhost:3002, 운영시에는 Railway URL 사용
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3002';

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 타임아웃을 10초로 증가
});

// 요청 인터셉터 추가
api.interceptors.request.use(
  (config) => {
    console.log('API 요청:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API 요청 에러:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터 추가
api.interceptors.response.use(
  (response) => {
    console.log('API 응답 성공:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.error('API 응답 에러:', error.config?.url, error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API configuration

// 랜덤 메시지 선택 함수
const getRandomMockMessage = (filters = {}) => {
  let availableMessages = [...mockMessages];
  
  // 카테고리 필터링
  if (filters.category && filters.category !== 'all') {
    availableMessages = availableMessages.filter(msg => msg.category === filters.category);
  }
  
  // 제외할 ID 필터링
  if (filters.excludeIds && filters.excludeIds.length > 0) {
    availableMessages = availableMessages.filter(msg => !filters.excludeIds.includes(msg.id.toString()));
  }
  
  // 랜덤 선택
  if (availableMessages.length === 0) {
    availableMessages = [...mockMessages]; // 필터링된 메시지가 없으면 전체에서 선택
  }
  
  const randomIndex = Math.floor(Math.random() * availableMessages.length);
  return {
    ...availableMessages[randomIndex],
    source: 'mock',
    timestamp: Date.now()
  };
};

// 날짜 기반 메시지 선택 (오늘의 메시지)
const getTodayMockMessage = () => {
  const today = new Date();
  const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
  const messageIndex = dayOfYear % mockMessages.length;
  
  return {
    ...mockMessages[messageIndex],
    source: 'mock',
    isToday: true,
    date: today.toISOString().split('T')[0],
    timestamp: Date.now()
  };
};

export const messageService = {
  // 랜덤 메시지 가져오기
  async getRandomMessage(filters = {}) {
    // 백엔드 서버가 준비될 때까지 Mock 데이터만 사용
    if (!API_BASE_URL) {
      console.log('백엔드 서버 미설정, Mock 데이터 사용');
      return getRandomMockMessage(filters);
    }
    
    try {
      const params = new URLSearchParams();
      if (filters.category && filters.category !== 'all') {
        params.append('category', filters.category);
      }
      
      if (filters.excludeIds && filters.excludeIds.length > 0) {
        params.append('exclude', filters.excludeIds.join(','));
      }
      
      params.append('_t', Date.now()); // 캐시 방지
      const response = await api.get(`/api/messages/random?${params}`);
      return response.data;
    } catch (error) {
      console.error('API 서버 연결 실패, Mock 데이터 사용:', error);
      console.error('Error details:', {
        message: error.message,
        code: error.code,
        response: error.response?.data,
        status: error.response?.status
      });
      
      // 백엔드가 배포되지 않은 경우 Mock 데이터 사용
      return getRandomMockMessage(filters);
    }
  },

  // 오늘의 메시지 가져오기 (랜덤 메시지로 대체)
  async getTodayMessage() {
    // 백엔드 서버가 준비될 때까지 Mock 데이터만 사용
    if (!API_BASE_URL) {
      console.log('백엔드 서버 미설정, Mock 오늘의 메시지 사용');
      return getTodayMockMessage();
    }
    
    try {
      const response = await api.get('/api/messages/random');
      const data = response.data;
      // 오늘의 메시지 형식으로 변환
      return {
        ...data,
        isToday: true,
        date: new Date().toISOString().split('T')[0]
      };
    } catch (error) {
      console.error('오늘의 메시지 API 연결 실패:', error);
      console.log('로컬 오늘의 메시지로 폴백 중...');
      return getTodayMockMessage();
    }
  },

  // 메시지 통계
  async getStats() {
    // 백엔드 서버가 준비될 때까지 Mock 데이터만 사용
    if (!API_BASE_URL) {
      console.log('백엔드 서버 미설정, Mock 통계 사용');
      return {
        total_messages: mockMessages.length,
        total_categories: mockCategories.length,
        by_category: mockCategories.reduce((acc, cat) => {
          acc[cat.name_ko] = mockMessages.filter(msg => msg.category === cat.name).length;
          return acc;
        }, {})
      };
    }
    
    try {
      const response = await api.get('/api/stats');
      return response.data;
    } catch (error) {
      console.error('통계 API 연결 실패, Mock 데이터 사용:', error);
      // Mock 통계 데이터 반환
      return {
        total_messages: mockMessages.length,
        total_categories: mockCategories.length,
        by_category: mockCategories.reduce((acc, cat) => {
          acc[cat.name_ko] = mockMessages.filter(msg => msg.category === cat.name).length;
          return acc;
        }, {})
      };
    }
  },

  // 카테고리 목록
  async getCategories() {
    // 백엔드 서버가 준비될 때까지 Mock 데이터만 사용
    if (!API_BASE_URL) {
      console.log('백엔드 서버 미설정, Mock 카테고리 사용');
      return { categories: mockCategories.map(cat => cat.name_ko) };
    }
    
    try {
      const response = await api.get('/api/categories');
      return response.data;
    } catch (error) {
      console.error('카테고리 API 연결 실패, Mock 데이터 사용:', error);
      // Mock 카테고리 데이터 반환
      return { categories: mockCategories.map(cat => cat.name_ko) };
    }
  },

  // 메시지 목록 (페이지네이션)
  async getMessages(options = {}) {
    try {
      const params = new URLSearchParams();
      if (options.page) params.append('page', options.page);
      if (options.limit) params.append('limit', options.limit);
      if (options.category && options.category !== 'all') params.append('category', options.category);
      if (options.search) params.append('search', options.search);

      const response = await api.get(`/messages?${params}`);
      return response.data;
    } catch (error) {
      console.error('메시지 목록 조회 실패:', error);
      return { messages: [], pagination: { page: 1, total: 0, totalPages: 0 } };
    }
  },

  // 즐겨찾기 추가
  async addFavorite(userId, messageId) {
    try {
      const response = await api.post('/favorites', { userId, messageId });
      return response.data;
    } catch (error) {
      console.error('즐겨찾기 추가 실패:', error);
      throw error;
    }
  },

  // 즐겨찾기 목록 조회
  async getFavorites(userId) {
    try {
      const response = await api.get(`/favorites/${userId}`);
      return response.data;
    } catch (error) {
      console.error('즐겨찾기 조회 실패:', error);
      return [];
    }
  },

  // 헬스 체크
  async checkHealth() {
    try {
      const response = await api.get('/');
      return { status: 'healthy', message: response.data.message };
    } catch (error) {
      console.error('헬스 체크 실패:', error);
      return { status: 'unhealthy' };
    }
  }
};

export default api;