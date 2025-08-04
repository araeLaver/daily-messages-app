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
  const [selectedCategory, setSelectedCategory] = useState('');
  const [showFavorites, setShowFavorites] = useState(false);
  const { count, incrementCounter } = useMessageCounter();

  // 페이지 로드 시 초기 메시지 가져오기
  useEffect(() => {
    const fetchInitial = async () => {
      setLoading(true);
      try {
        const message = await messageService.getRandomMessage();
        setCurrentMessage(message);
        incrementCounter();
      } catch (error) {
        console.error('초기 메시지 로딩 실패:', error);
      }
      setLoading(false);
    };

    const loadCategories = async () => {
      try {
        const categoryList = await messageService.getCategories();
        setCategories(categoryList);
      } catch (error) {
        console.error('카테고리 로딩 실패:', error);
      }
    };

    fetchInitial();
    loadCategories();
  }, [incrementCounter]);

  const fetchNewMessage = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (selectedCategory) filters.category = selectedCategory;
      
      const message = await messageService.getRandomMessage(filters);
      setCurrentMessage(message);
      incrementCounter();
    } catch (error) {
      console.error('새 메시지 로딩 실패:', error);
    }
    setLoading(false);
  };

  const handleShare = () => {
    // 공유 완료 후 추가 로직이 필요한 경우
  };

  const handleSpeak = () => {
    // 음성 재생 완료 후 추가 로직이 필요한 경우
  };

  const handleFavorite = (message) => {
    // 즐겨찾기 기능 구현
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    const isAlreadyFavorite = favorites.some(fav => fav.id === message.id);
    
    if (!isAlreadyFavorite) {
      favorites.push(message);
      localStorage.setItem('favorites', JSON.stringify(favorites));
      alert('즐겨찾기에 추가되었습니다!');
    } else {
      alert('이미 즐겨찾기에 추가된 메시지입니다.');
    }
  };

  return (
    <div className="min-h-screen gradient-bg">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <Header 
          messageCount={count} 
          onShowFavorites={() => setShowFavorites(true)}
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
            onShare={handleShare}
            onSpeak={handleSpeak}
            onFavorite={handleFavorite}
          />
        </main>

        <Footer />
        
        <FavoritesList 
          isOpen={showFavorites}
          onClose={() => setShowFavorites(false)}
        />
      </div>
    </div>
  );
}

export default App;