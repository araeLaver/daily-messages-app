import React, { useState, useEffect } from 'react';
import { Heart, X, Copy, Check } from 'lucide-react';
import { getKoreanCategory } from '../utils/categoryTranslations';

const FavoritesList = ({ isOpen, onClose }) => {
  const [favorites, setFavorites] = useState([]);
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    if (isOpen) {
      const savedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
      setFavorites(savedFavorites);
    }
  }, [isOpen]);

  const removeFavorite = (id) => {
    const updatedFavorites = favorites.filter(fav => fav.id !== id);
    setFavorites(updatedFavorites);
    localStorage.setItem('favorites', JSON.stringify(updatedFavorites));
  };

  const copyToClipboard = async (text, id) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('복사 실패:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-hidden">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Heart className="w-6 h-6 text-red-400" />
            즐겨찾기 ({favorites.length})
          </h2>
          <button 
            onClick={onClose}
            className="text-white/70 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="overflow-y-auto max-h-[60vh] space-y-4">
          {favorites.length === 0 ? (
            <div className="text-center text-white/60 py-8">
              아직 즐겨찾기한 메시지가 없습니다.
            </div>
          ) : (
            favorites.map((message) => (
              <div key={message.id} className="bg-white/5 rounded-xl p-4 border border-white/10">
                <p className="text-white text-lg leading-relaxed mb-3">
                  "{message.text}"
                </p>
                <div className="flex justify-between items-center">
                  <div className="text-white/60 text-sm">
                    <span className="bg-white/10 px-2 py-1 rounded-full text-xs mr-2">
                      {getKoreanCategory(message.category)}
                    </span>
                    {message.author && `- ${message.author}`}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => copyToClipboard(message.text, message.id)}
                      className="text-white/60 hover:text-white transition-colors"
                    >
                      {copiedId === message.id ? 
                        <Check className="w-4 h-4 text-green-400" /> : 
                        <Copy className="w-4 h-4" />
                      }
                    </button>
                    <button
                      onClick={() => removeFavorite(message.id)}
                      className="text-red-400 hover:text-red-300 transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default FavoritesList;