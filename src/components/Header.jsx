import React from 'react';
import { Sun, Calendar, Heart } from 'lucide-react';

const Header = ({ messageCount, onShowFavorites }) => {
  const getCurrentDate = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const date = now.getDate();
    const dayNames = ['일', '월', '화', '수', '목', '금', '토'];
    const dayName = dayNames[now.getDay()];
    
    return `${year}년 ${month}월 ${date}일 ${dayName}요일`;
  };

  return (
    <header className="text-center mb-12 animate-fade-in">
      {/* 타이틀 */}
      <div className="flex items-center justify-center gap-3 mb-4">
        <Sun className="w-8 h-8 text-yellow-300 animate-bounce-soft" />
        <h1 className="text-white text-3xl md:text-4xl font-bold text-shadow">
          Daily Messages
        </h1>
      </div>

      {/* 날짜 */}
      <div className="flex items-center justify-center gap-2 mb-6">
        <Calendar className="w-5 h-5 text-white/70" />
        <p className="text-white/80 text-lg font-medium">
          {getCurrentDate()}
        </p>
      </div>

      {/* 메시지 카운터 & 즐겨찾기 버튼 */}
      <div className="flex items-center justify-center gap-4">
        <div className="inline-block px-6 py-3 bg-white/10 rounded-full backdrop-blur-sm">
          <p className="text-white/90 font-medium">
            {messageCount}번째 메시지
          </p>
        </div>
        
        <button
          onClick={onShowFavorites}
          className="flex items-center gap-2 px-4 py-3 bg-white/10 hover:bg-white/20 
                   rounded-full backdrop-blur-sm transition-all duration-300 text-white/90
                   hover:scale-105 active:scale-95"
          title="즐겨찾기 목록"
        >
          <Heart className="w-4 h-4" />
          <span className="text-sm font-medium">즐겨찾기</span>
        </button>
      </div>
    </header>
  );
};

export default Header;