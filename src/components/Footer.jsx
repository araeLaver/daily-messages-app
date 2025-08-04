import React from 'react';
import { Sparkles, Coffee } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="text-center mt-12 animate-fade-in">

      {/* 브랜딩 */}
      <div className="flex items-center justify-center gap-2 mb-4">
        <Coffee className="w-5 h-5 text-amber-300" />
        <span className="text-white/80 font-medium">
          모닝
        </span>
        <Sparkles className="w-4 h-4 text-yellow-300" />
      </div>

      {/* 설명 */}
      <p className="text-white/60 text-sm max-w-md mx-auto leading-relaxed">
        매일 새로운 영감과 동기부여 메시지 ✨
      </p>
    </footer>
  );
};

export default Footer;