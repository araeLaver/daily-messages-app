import axios from 'axios';
import { mockMessages, mockCategories } from '../data/mockMessages';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3002';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000, // 빠른 타임아웃으로 폴백 활성화
});

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
      console.log('API 서버 연결 실패, 로컬 데이터 사용:', error.message);
      
      // 로컬 랜덤 메시지 반환
      return getRandomMockMessage(filters);
    }
  },

  // 오늘의 메시지 가져오기
  async getTodayMessage() {
    try {
      const response = await api.get('/api/messages/today');
      return response.data;
    } catch (error) {
      console.log('API 서버 연결 실패, 로컬 오늘의 메시지 사용:', error.message);
      return getTodayMockMessage();
    }
  },

  // 메시지 통계
  async getStats() {
    try {
      const response = await api.get('/api/stats');
      return response.data;
    } catch (error) {
      console.log('API 서버 연결 실패, 로컬 통계 사용:', error.message);
      return { 
        totalMessages: mockMessages.length, 
        categoriesCount: mockCategories.length - 1, // '전체' 제외
        recentMessages: mockMessages.length,
        schema: 'mock_data'
      };
    }
  },

  // 카테고리 목록
  async getCategories() {
    try {
      const response = await api.get('/api/categories');
      return response.data;
    } catch (error) {
      console.log('API 서버 연결 실패, 로컬 카테고리 사용:', error.message);
      return mockCategories;
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

      const response = await api.get(`/api/messages?${params}`);
      return response.data;
    } catch (error) {
      console.error('메시지 목록 조회 실패:', error);
      return { messages: [], pagination: { page: 1, total: 0, totalPages: 0 } };
    }
  },

  // 즐겨찾기 추가
  async addFavorite(userId, messageId) {
    try {
      const response = await api.post('/api/favorites', { userId, messageId });
      return response.data;
    } catch (error) {
      console.error('즐겨찾기 추가 실패:', error);
      throw error;
    }
  },

  // 즐겨찾기 목록 조회
  async getFavorites(userId) {
    try {
      const response = await api.get(`/api/favorites/${userId}`);
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