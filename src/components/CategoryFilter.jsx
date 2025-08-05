import React, { useState } from 'react';
import { Filter, ChevronDown, Tag } from 'lucide-react';

const CategoryFilter = ({ categories, selectedCategory, onCategoryChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  // 상위 카테고리들만 표시 (메시지 수가 많은 순)
  const topCategories = categories
    .filter(cat => cat.message_count > 5 || cat.name === 'all')
    .slice(0, 10);

  const selectedCategoryInfo = categories.find(cat => cat.name === selectedCategory) || categories[0];

  return (
    <div className="mb-8">
      {/* 모바일 친화적 드롭다운 */}
      <div className="relative md:hidden">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between gap-3 px-4 py-3 bg-white/10 backdrop-blur-sm 
                   border border-white/20 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-white/70" />
            <span>{selectedCategoryInfo?.name_ko || '전체'}</span>
            {selectedCategoryInfo?.message_count && (
              <span className="text-xs text-white/60">({selectedCategoryInfo.message_count}개)</span>
            )}
          </div>
          <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white/10 backdrop-blur-md border border-white/20 
                         rounded-xl shadow-2xl z-10 max-h-60 overflow-y-auto">
            {topCategories.map(category => (
              <button
                key={category.name}
                onClick={() => {
                  onCategoryChange(category.name);
                  setIsOpen(false);
                }}
                className={`w-full text-left px-4 py-3 text-white text-sm hover:bg-white/10 transition-colors
                          ${selectedCategory === category.name ? 'bg-white/20' : ''}`}
              >
                <div className="flex items-center justify-between">
                  <span>{category.name_ko}</span>
                  {category.message_count && (
                    <span className="text-xs text-white/60">{category.message_count}개</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* 데스크톱용 태그 스타일 */}
      <div className="hidden md:block">
        <div className="flex items-center gap-2 mb-3">
          <Tag className="w-5 h-5 text-white/70" />
          <span className="text-white/80 text-sm font-medium">카테고리</span>
        </div>
        
        <div className="flex flex-wrap gap-2">
          {topCategories.map(category => (
            <button
              key={category.name}
              onClick={() => onCategoryChange(category.name)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:scale-105
                        ${selectedCategory === category.name
                          ? 'bg-blue-500/80 text-white shadow-lg ring-2 ring-blue-400/50'
                          : 'bg-white/10 text-white/80 hover:bg-white/20 backdrop-blur-sm'}`}
            >
              {category.name_ko}
              {category.message_count && (
                <span className="ml-1 text-xs opacity-70">({category.message_count})</span>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CategoryFilter;