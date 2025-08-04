import axios from 'axios';

const API_BASE_URL = 'http://localhost:8005';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const messageService = {
  // 외부 API에서 명언 가져오기
  async getExternalQuote() {
    try {
      const response = await fetch('https://api.quotable.io/random?tags=inspirational,motivational,wisdom,success');
      const data = await response.json();
      return {
        id: data._id,
        text: data.content,
        author: data.author,
        category: data.tags[0] || '영감',
        source: 'quotable_api'
      };
    } catch (error) {
      console.error('외부 명언 API 실패:', error);
      return null;
    }
  },

  // 랜덤 메시지 가져오기 (로컬 DB + 외부 API)
  async getRandomMessage(filters = {}) {
    // 50% 확률로 외부 API 사용
    if (Math.random() > 0.5) {
      const externalQuote = await this.getExternalQuote();
      if (externalQuote) return externalQuote;
    }

    try {
      const params = new URLSearchParams();
      if (filters.category) params.append('category', filters.category);
      if (filters.time_of_day) params.append('time_of_day', filters.time_of_day);
      if (filters.season) params.append('season', filters.season);
      
      const response = await api.get(`/messages/random?${params}`);
      return response.data;
    } catch (error) {
      console.error('메시지 조회 실패:', error);
      
      // 외부 API 재시도
      const externalQuote = await this.getExternalQuote();
      if (externalQuote) return externalQuote;
      
      // 최종 폴백 메시지
      return {
        id: 'fallback',
        text: '오늘도 새로운 기회가 당신을 기다리고 있습니다. 🌅',
        author: 'Daily Messages',
        category: '새로운 시작',
        source: 'fallback'
      };
    }
  },

  // 메시지 통계
  async getStats() {
    try {
      const response = await api.get('/messages/stats');
      return response.data;
    } catch (error) {
      console.error('통계 조회 실패:', error);
      return { total_messages: 0, by_category: {}, by_source: {} };
    }
  },

  // 카테고리 목록
  async getCategories() {
    try {
      const response = await api.get('/messages/categories');
      return response.data.categories;
    } catch (error) {
      console.error('카테고리 조회 실패:', error);
      return ['새로운 시작', '동기부여', '자신감', '성장'];
    }
  },

  // 헬스 체크
  async checkHealth() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('헬스 체크 실패:', error);
      return { status: 'unhealthy' };
    }
  }
};

export default api;