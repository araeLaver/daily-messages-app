import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// API configuration

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
      console.error('메시지 조회 실패:', error);
      
      // 최종 폴백 메시지
      return {
        id: 'fallback',
        text: '오늘도 새로운 기회가 당신을 기다리고 있습니다. 🌅',
        author: 'Daily Messages',
        category: '영감',
        source: 'fallback'
      };
    }
  },

  // 오늘의 메시지 가져오기
  async getTodayMessage() {
    try {
      const response = await api.get('/api/messages/today');
      return response.data;
    } catch (error) {
      console.error('오늘의 메시지 조회 실패:', error);
      return this.getRandomMessage();
    }
  },

  // 메시지 통계
  async getStats() {
    try {
      const response = await api.get('/api/stats');
      return response.data;
    } catch (error) {
      console.error('통계 조회 실패:', error);
      return { totalMessages: 0, categoriesCount: 0, recentMessages: 0 };
    }
  },

  // 카테고리 목록
  async getCategories() {
    try {
      const response = await api.get('/api/categories');
      return response.data;
    } catch (error) {
      console.error('카테고리 조회 실패:', error);
      return [
        { name: 'all', name_ko: '전체', message_count: null },
        { name: '동기부여', name_ko: '동기부여', message_count: 10 },
        { name: '성공', name_ko: '성공', message_count: 13 },
        { name: '행복', name_ko: '행복', message_count: 11 }
      ];
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