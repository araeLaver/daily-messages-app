import React from 'react';
import { Sparkles, Coffee, Heart, Clock, Database } from 'lucide-react';

const Footer = ({ stats }) => {
  const getCurrentTime = () => {
    return new Date().toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <footer className="text-center mt-16 animate-fade-in">
      {/* 통계 정보 */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 max-w-2xl mx-auto">
          <div className="bg-white/5 rounded-xl p-4 backdrop-blur-sm">
            <Database className="w-5 h-5 text-blue-300 mx-auto mb-2" />
            <div className="text-white text-lg font-bold">{stats.totalMessages}</div>
            <div className="text-white/60 text-xs">총 명언</div>
          </div>
          
          <div className="bg-white/5 rounded-xl p-4 backdrop-blur-sm">
            <Coffee className="w-5 h-5 text-amber-300 mx-auto mb-2" />
            <div className="text-white text-lg font-bold">{stats.categoriesCount}</div>
            <div className="text-white/60 text-xs">카테고리</div>
          </div>
          
          <div className="bg-white/5 rounded-xl p-4 backdrop-blur-sm">
            <Sparkles className="w-5 h-5 text-yellow-300 mx-auto mb-2" />
            <div className="text-white text-lg font-bold">{stats.recentMessages || 0}</div>
            <div className="text-white/60 text-xs">최근 추가</div>
          </div>
          
          <div className="bg-white/5 rounded-xl p-4 backdrop-blur-sm">
            <Clock className="w-5 h-5 text-green-300 mx-auto mb-2" />
            <div className="text-white text-lg font-bold">{getCurrentTime()}</div>
            <div className="text-white/60 text-xs">현재 시간</div>
          </div>
        </div>
      )}

      {/* 브랜딩 */}
      <div className="flex items-center justify-center gap-2 mb-6">
        <Coffee className="w-5 h-5 text-amber-300" />
        <span className="text-white/90 font-semibold text-lg">
          Daily Messages
        </span>
        <Sparkles className="w-4 h-4 text-yellow-300 animate-pulse" />
      </div>

      {/* 설명 */}
      <div className="max-w-lg mx-auto mb-6">
        <p className="text-white/70 text-sm leading-relaxed mb-2">
          매일 새로운 영감과 동기부여를 전해드립니다 ✨
        </p>
        <p className="text-white/50 text-xs">
          React Bits 스타일의 아름다운 명언 앱
        </p>
      </div>

      {/* 심볼 */}
      <div className="flex items-center justify-center gap-2 text-white/40">
        <Heart className="w-4 h-4 fill-current text-red-400/60" />
        <span className="text-xs">Made with love</span>
        <Heart className="w-4 h-4 fill-current text-red-400/60" />
      </div>

      {/* 하단 여백 */}
      <div className="h-8"></div>
    </footer>
  );
};

export default Footer;