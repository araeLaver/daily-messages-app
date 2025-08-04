import React from 'react';
import { Filter } from 'lucide-react';

const CategoryFilter = ({ categories, selectedCategory, onCategoryChange }) => {
  return (
    <div className="flex items-center gap-3 mb-6">
      <Filter className="w-5 h-5 text-white/70" />
      <select 
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        className="bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        <option value="">전체 카테고리</option>
        {categories.map(category => (
          <option key={category} value={category} className="bg-gray-800">
            {category}
          </option>
        ))}
      </select>
    </div>
  );
};

export default CategoryFilter;