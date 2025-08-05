import React, { useState } from 'react';
import { RefreshCw, Heart, Share, Volume2, Copy, Check } from 'lucide-react';
import { getKoreanCategory } from '../utils/categoryTranslations';

const MessageCard = ({ 
  message, 
  onNewMessage, 
  loading = false,
  todayMode = false,
  onShare,
  onSpeak,
  onFavorite 
}) => {
  if (loading) {
    return (
      <div className="glass-effect rounded-3xl p-8 text-center animate-pulse">
        <div className="h-6 bg-white/20 rounded-full mb-4"></div>
        <div className="h-4 bg-white/20 rounded-full mb-2"></div>
        <div className="h-4 bg-white/20 rounded-full w-3/4 mx-auto"></div>
      </div>
    );
  }

  if (!message) {
    return (
      <div className="glass-effect rounded-3xl p-8 text-center">
        <p className="text-white/70">메시지를 불러오는 중...</p>
      </div>
    );
  }

  const handleSpeak = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(message.text);
      utterance.lang = 'ko-KR';
      utterance.rate = 0.8;
      speechSynthesis.speak(utterance);
    }
    onSpeak?.();
  };

  const handleShare = async () => {
    const shareData = {
      title: '모닝 - 새로운 하루',
      text: `"${message.text}" - ${message.author}`,
      url: window.location.href
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (err) {
        console.log('공유 취소됨');
      }
    } else {
      // 폴백: 클립보드에 복사
      navigator.clipboard.writeText(`"${message.text}" - ${message.author}`);
      alert('메시지가 클립보드에 복사되었습니다!');
    }
    onShare?.();
  };

  return (
    <div className="glass-effect rounded-3xl p-8 shadow-2xl animate-slide-up">
      {/* 메시지 텍스트 */}
      <blockquote className="text-white text-xl md:text-2xl font-light leading-relaxed mb-6 text-center text-shadow">
        "{message.text}"
      </blockquote>
      
      {/* 저자 */}
      {message.author && message.author.trim() && message.author !== '익명' && (
        <div className="text-center mb-6">
          <cite className="text-white/80 text-lg font-medium not-italic">
            — {message.author}
          </cite>
        </div>
      )}

      {/* 카테고리 및 기타 정보 */}
      <div className="text-center mb-8 flex justify-center gap-2 flex-wrap">
        <span className="inline-block px-4 py-2 bg-white/20 rounded-full text-white/90 text-sm font-medium">
          #{getKoreanCategory(message.category)}
        </span>
        {todayMode && (
          <span className="inline-block px-3 py-2 bg-yellow-400/20 text-yellow-200 rounded-full text-xs font-medium">
            Today's Pick ⭐
          </span>
        )}
        {message.date && (
          <span className="inline-block px-3 py-2 bg-blue-400/20 text-blue-200 rounded-full text-xs font-medium">
            {new Date(message.date).toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })}
          </span>
        )}
      </div>

      {/* 액션 버튼들 */}
      <div className="flex justify-center gap-3 flex-wrap">
        <button
          onClick={onNewMessage}
          className="flex items-center gap-2 px-6 py-3 bg-white/20 hover:bg-white/30 
                   rounded-full transition-all duration-300 text-white font-medium
                   hover:scale-105 active:scale-95"
          disabled={loading}
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          새로운 메시지
        </button>

        <button
          onClick={handleSpeak}
          className="p-3 bg-white/20 hover:bg-white/30 rounded-full 
                   transition-all duration-300 text-white
                   hover:scale-105 active:scale-95"
          title="음성으로 듣기"
        >
          <Volume2 className="w-4 h-4" />
        </button>

        <button
          onClick={handleShare}
          className="p-3 bg-white/20 hover:bg-white/30 rounded-full 
                   transition-all duration-300 text-white
                   hover:scale-105 active:scale-95"
          title="공유하기"
        >
          <Share className="w-4 h-4" />
        </button>

        <CopyButton message={message} />

        <button
          onClick={() => onFavorite?.(message)}
          className="p-3 bg-white/20 hover:bg-white/30 rounded-full 
                   transition-all duration-300 text-white
                   hover:scale-105 active:scale-95"
          title="즐겨찾기"
        >
          <Heart className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

const CopyButton = ({ message }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('복사 실패:', err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="p-3 bg-white/20 hover:bg-white/30 rounded-full 
               transition-all duration-300 text-white
               hover:scale-105 active:scale-95"
      title="복사하기"
    >
      {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
    </button>
  );
};

export default MessageCard;