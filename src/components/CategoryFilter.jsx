import React, { useState } from 'react';
import { ChevronDown, Sparkles } from 'lucide-react';

const CategoryFilter = ({ categories, selectedCategory, onCategoryChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  // 카테고리가 로드되지 않은 경우 기본값 제공
  if (!categories || !Array.isArray(categories) || categories.length === 0) {
    return (
      <div className="mb-8">
        <div className="relative">
          <button
            disabled
            className="w-full flex items-center justify-between px-5 py-4 bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-lg 
                     border border-white/20 rounded-2xl text-white/50 cursor-not-allowed"
          >
            <div className="flex items-center gap-3">
              <div className="text-xl">⏳</div>
              <div>
                <div className="text-left text-sm font-medium text-white/70">
                  카테고리 로딩 중...
                </div>
                <div className="text-xs text-white/50">
                  잠시만 기다려주세요
                </div>
              </div>
            </div>
          </button>
        </div>
      </div>
    );
  }
  
  // 모든 카테고리 표시 (메시지 수 1개 이상 또는 '전체')
  const topCategories = categories
    .filter(cat => cat.message_count >= 1 || cat.name === 'all')
    .slice(0, 15);

  const selectedCategoryInfo = topCategories.find(cat => cat.name === selectedCategory) || 
                               (topCategories.length > 0 ? topCategories[0] : null) || 
                               { name: 'all', name_ko: '전체' };

  const categoryEmojis = {
    'all': '✨',
    '동기부여': '💪',
    '사랑': '❤️',
    '성공': '🏆',
    '지혜': '🧠',
    '행복': '😊',
    '감사': '🙏',
    '리더십': '👑',
    '변화': '🔄',
    '성장': '🌱',
    '시간': '⏰',
    '용기': '🦁',
    '우정': '🤝',
    '인내': '⛰️',
    '창의성': '🎨',
    '평화': '🕊️'
  };

  return (
    <div className="mb-8">
      <div className="relative">
        {/* 커스텀 드롭다운 버튼 */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between px-5 py-4 bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-lg 
                   border border-white/20 rounded-2xl text-white hover:bg-white/15 transition-all duration-300
                   shadow-lg hover:shadow-xl group"
        >
          <div className="flex items-center gap-3">
            <div className="text-xl">{categoryEmojis[selectedCategory] || '✨'}</div>
            <div>
              <div className="text-left text-sm font-medium text-white/90">
                {selectedCategoryInfo?.name_ko || '전체'}
              </div>
              <div className="text-xs text-white/60">
                카테고리 선택
              </div>
            </div>
          </div>
          <ChevronDown 
            className={`w-5 h-5 text-white/60 transition-transform duration-300 group-hover:text-white/80 ${
              isOpen ? 'rotate-180' : ''
            }`} 
          />
        </button>

        {/* 드롭다운 메뉴 */}
        {isOpen && (
          <>
            {/* 배경 오버레이 */}
            <div 
              className="fixed inset-0 z-10" 
              onClick={() => setIsOpen(false)}
            ></div>
            
            {/* 드롭다운 컨텐츠 */}
            <div className="absolute top-full left-0 right-0 mt-2 bg-white/10 backdrop-blur-xl border border-white/20 
                           rounded-2xl shadow-2xl z-20 max-h-80 overflow-y-auto animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-2">
                {topCategories && topCategories.length > 0 ? topCategories.map((category, index) => (
                  <button
                    key={category.name}
                    onClick={() => {
                      onCategoryChange(category.name);
                      setIsOpen(false);
                    }}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all duration-200
                              hover:bg-white/15 hover:scale-[1.02] ${
                                selectedCategory === category.name 
                                  ? 'bg-white/20 ring-1 ring-white/30' 
                                  : ''
                              }`}
                    style={{ animationDelay: `${index * 30}ms` }}
                  >
                    <div className="text-lg">{categoryEmojis[category.name] || '✨'}</div>
                    <div className="flex-1">
                      <div className="text-white font-medium text-sm">
                        {category.name_ko}
                      </div>
                    </div>
                    {selectedCategory === category.name && (
                      <Sparkles className="w-4 h-4 text-yellow-300 animate-pulse" />
                    )}
                  </button>
                )) : (
                  <div className="px-4 py-3 text-white/50 text-center">
                    카테고리가 없습니다
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CategoryFilter;