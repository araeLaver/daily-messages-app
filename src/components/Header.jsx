import React from 'react';
import { Calendar, Heart, Star, TrendingUp, Coffee } from 'lucide-react';
import WeatherWidget from './WeatherWidget';

const Header = ({ messageCount, stats, todayMode, onShowFavorites, onTodayMessage }) => {
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
        {/* <div className="relative">
          <Sun className="w-8 h-8 text-yellow-300 animate-bounce-soft" />
          {todayMode && (
            <Star className="w-4 h-4 text-yellow-200 absolute -top-1 -right-1 animate-pulse" />
          )}
        </div> */}
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
        {todayMode && (
          <span className="px-2 py-1 bg-yellow-400/20 text-yellow-200 text-xs rounded-full font-medium">
            오늘의 명언
          </span>
        )}
      </div>

      {/* 통계 정보 및 날씨 */}
      <div className="flex items-center justify-center gap-4 mb-6 flex-wrap">
        <WeatherWidget />
        {stats && (
          <>
            <div className="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-full backdrop-blur-sm">
              <TrendingUp className="w-4 h-4 text-blue-300" />
              <span className="text-white/80 text-sm">총 {stats.total_messages}개</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-full backdrop-blur-sm">
              <Coffee className="w-4 h-4 text-amber-300" />
              <span className="text-white/80 text-sm">{Object.keys(stats.by_category || {}).length}개 카테고리</span>
            </div>
          </>
        )}
      </div>

      {/* 메시지 카운터 & 버튼들 */}
      <div className="flex items-center justify-center gap-4 flex-wrap">
        <div className="inline-block px-6 py-3 bg-white/10 rounded-full backdrop-blur-sm">
          <p className="text-white/90 font-medium">
            {messageCount}번째 메시지
          </p>
        </div>
        
        <button
          onClick={onTodayMessage}
          className={`flex items-center gap-2 px-4 py-3 rounded-full backdrop-blur-sm 
                     transition-all duration-300 text-white/90 hover:scale-105 active:scale-95
                     ${todayMode 
                       ? 'bg-yellow-400/20 hover:bg-yellow-400/30 border border-yellow-400/30' 
                       : 'bg-white/10 hover:bg-white/20'}`}
          title="오늘의 명언 보기"
        >
          <Star className="w-4 h-4" />
          <span className="text-sm font-medium">오늘의 명언</span>
        </button>
        
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