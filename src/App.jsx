import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import MessageCard from './components/MessageCard';
import Footer from './components/Footer';
import CategoryFilter from './components/CategoryFilter';
import FavoritesList from './components/FavoritesList';
import { messageService } from './services/api';
import { useMessageCounter } from './hooks/useMessageCounter';
import './App.css';

function App() {
  const [currentMessage, setCurrentMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showFavorites, setShowFavorites] = useState(false);
  const [recentMessageIds, setRecentMessageIds] = useState([]);
  const [stats, setStats] = useState(null);
  const [todayMode, setTodayMode] = useState(false);
  const { count, incrementCounter } = useMessageCounter();

  // 페이지 로드 시 초기 데이터 로딩
  useEffect(() => {
    const initializeApp = async () => {
      setLoading(true);
      try {
        // 병렬로 데이터 로딩
        const [message, categoryList, statsData] = await Promise.all([
          messageService.getTodayMessage(),
          messageService.getCategories(),
          messageService.getStats()
        ]);

        setCurrentMessage(message);
        setCategories(categoryList);
        setStats(statsData);
        setTodayMode(true);
        incrementCounter();
      } catch (error) {
        console.error('초기 데이터 로딩 실패:', error);
        // 폴백으로 랜덤 메시지 시도
        try {
          const fallbackMessage = await messageService.getRandomMessage();
          setCurrentMessage(fallbackMessage);
          incrementCounter();
        } catch (fallbackError) {
          console.error('폴백 메시지 로딩도 실패:', fallbackError);
        }
      }
      setLoading(false);
    };

    initializeApp();
  }, [incrementCounter]);

  const fetchNewMessage = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (selectedCategory && selectedCategory !== 'all') {
        filters.category = selectedCategory;
      }
      
      // 최근 본 메시지 제외 (중복 방지)
      if (recentMessageIds.length > 0) {
        filters.excludeIds = recentMessageIds;
      }
      
      const message = await messageService.getRandomMessage(filters);
      
      if (message && message.id) {
        setCurrentMessage(message);
        setTodayMode(false); // 랜덤 모드로 전환
        incrementCounter();
        
        // 최근 본 메시지 ID 업데이트 (최대 20개 유지)
        setRecentMessageIds(prev => {
          const newIds = [message.id, ...prev.filter(id => id !== message.id)].slice(0, 20);
          return newIds;
        });
      }
    } catch (error) {
      console.error('새 메시지 로딩 실패:', error);
    }
    setLoading(false);
  };

  const fetchTodayMessage = async () => {
    setLoading(true);
    try {
      const message = await messageService.getTodayMessage();
      setCurrentMessage(message);
      setTodayMode(true);
    } catch (error) {
      console.error('오늘의 메시지 로딩 실패:', error);
    }
    setLoading(false);
  };

  const handleShare = () => {
    // 공유 완료 후 추가 로직이 필요한 경우
  };

  const handleSpeak = () => {
    // 음성 재생 완료 후 추가 로직이 필요한 경우
  };

  const handleFavorite = async (message) => {
    try {
      // 간단한 사용자 ID 생성 (실제 앱에서는 인증 시스템 사용)
      const userId = localStorage.getItem('userId') || 'anonymous_' + Date.now();
      if (!localStorage.getItem('userId')) {
        localStorage.setItem('userId', userId);
      }

      // 로컬 스토리지에도 저장 (백업용)
      const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
      const isAlreadyFavorite = favorites.some(fav => fav.id === message.id);
      
      if (!isAlreadyFavorite) {
        favorites.push(message);
        localStorage.setItem('favorites', JSON.stringify(favorites));
        
        // 서버에도 저장 시도
        try {
          await messageService.addFavorite(userId, message.id);
        } catch (serverError) {
          console.warn('서버 즐겨찾기 저장 실패, 로컬에만 저장됨:', serverError);
        }
        
        alert('즐겨찾기에 추가되었습니다! ⭐');
      } else {
        alert('이미 즐겨찾기에 추가된 메시지입니다.');
      }
    } catch (error) {
      console.error('즐겨찾기 추가 실패:', error);
      alert('즐겨찾기 추가에 실패했습니다.');
    }
  };

  return (
    <div className="min-h-screen gradient-bg">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Header 
          messageCount={count} 
          stats={stats}
          todayMode={todayMode}
          onShowFavorites={() => setShowFavorites(true)}
          onTodayMessage={fetchTodayMessage}
        />
        
        <main className="mb-12">
          <CategoryFilter
            categories={categories}
            selectedCategory={selectedCategory}
            onCategoryChange={setSelectedCategory}
          />
          
          <MessageCard
            message={currentMessage}
            onNewMessage={fetchNewMessage}
            loading={loading}
            todayMode={todayMode}
            onShare={handleShare}
            onSpeak={handleSpeak}
            onFavorite={handleFavorite}
          />
        </main>

        <Footer stats={stats} />
        
        <FavoritesList 
          isOpen={showFavorites}
          onClose={() => setShowFavorites(false)}
        />
      </div>
    </div>
  );
}

export default App;