import React from 'react';

const Footer = ({ stats }) => {

  // 올해 진행률 (더 직관적으로)
  const getYearProgress = () => {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const end = new Date(now.getFullYear() + 1, 0, 1);
    const progress = ((now - start) / (end - start)) * 100;
    const dayOfYear = Math.floor((now - start) / (1000 * 60 * 60 * 24)) + 1;
    
    return {
      percentage: Math.round(progress),
      dayOfYear,
      totalDays: 365,
      remaining: 365 - dayOfYear
    };
  };

  // 실제 날씨 정보 가져오기 (OpenWeatherMap API 사용)
  const [weather, setWeather] = React.useState({
    emoji: '🌤️',
    desc: '로딩중...',
    temp: '--'
  });

  React.useEffect(() => {
    // 실제 날씨 API 호출 (위치 기반)
    const fetchWeather = async () => {
      const API_KEY = '9c91c7531f829a1e0e2fa3ab2fb04b60';
      
      try {
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              const lat = position.coords.latitude;
              const lon = position.coords.longitude;
              
              try {
                console.log('날씨 정보를 가져오는 중...');
                const response = await fetch(
                  `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=kr`
                );
                const data = await response.json();
                
                console.log('날씨 데이터:', data);
                
                // 날씨 상태를 이모지로 변환
                const getWeatherEmoji = (weatherMain, weatherId) => {
                  if (weatherMain === 'Clear') return '☀️';
                  if (weatherMain === 'Clouds') return weatherId === 801 ? '🌤️' : '☁️';
                  if (weatherMain === 'Rain') return '🌧️';
                  if (weatherMain === 'Drizzle') return '🌦️';
                  if (weatherMain === 'Thunderstorm') return '⛈️';
                  if (weatherMain === 'Snow') return '🌨️';
                  if (weatherMain === 'Mist' || weatherMain === 'Fog') return '🌫️';
                  if (weatherMain === 'Haze') return '🌫️';
                  return '🌤️'; // 기본값
                };
                
                const weatherInfo = {
                  emoji: getWeatherEmoji(data.weather[0].main, data.weather[0].id),
                  desc: data.weather[0].description,
                  temp: `${Math.round(data.main.temp)}°C`
                };
                
                setWeather(weatherInfo);
                console.log('날씨 정보 업데이트 완료:', weatherInfo);
              } catch (error) {
                console.error('날씨 API 호출 실패:', error);
                // 위치는 있지만 API 호출 실패시 서울 기본값
                const response = await fetch(
                  `https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=${API_KEY}&units=metric&lang=kr`
                );
                const data = await response.json();
                
                const getWeatherEmoji = (weatherMain) => {
                  if (weatherMain === 'Clear') return '☀️';
                  if (weatherMain === 'Clouds') return '☁️';
                  if (weatherMain === 'Rain') return '🌧️';
                  if (weatherMain === 'Snow') return '🌨️';
                  return '🌤️';
                };
                
                setWeather({
                  emoji: getWeatherEmoji(data.weather[0].main),
                  desc: `${data.weather[0].description} (서울)`,
                  temp: `${Math.round(data.main.temp)}°C`
                });
              }
            },
            async () => {
              // 위치 정보 거부시 서울 날씨
              try {
                console.log('위치 정보 거부됨. 서울 날씨를 가져옵니다.');
                const response = await fetch(
                  `https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=${API_KEY}&units=metric&lang=kr`
                );
                const data = await response.json();
                
                const getWeatherEmoji = (weatherMain) => {
                  if (weatherMain === 'Clear') return '☀️';
                  if (weatherMain === 'Clouds') return '☁️';
                  if (weatherMain === 'Rain') return '🌧️';
                  if (weatherMain === 'Snow') return '🌨️';
                  return '🌤️';
                };
                
                setWeather({
                  emoji: getWeatherEmoji(data.weather[0].main),
                  desc: `${data.weather[0].description} (서울)`,
                  temp: `${Math.round(data.main.temp)}°C`
                });
              } catch (error) {
                console.error('서울 날씨 조회 실패:', error);
                setWeather({ emoji: '🌤️', desc: '날씨 정보 없음', temp: '--°C' });
              }
            }
          );
        } else {
          // 위치 정보를 지원하지 않는 브라우저
          try {
            console.log('위치 정보 미지원. 서울 날씨를 가져옵니다.');
            const response = await fetch(
              `https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=${API_KEY}&units=metric&lang=kr`
            );
            const data = await response.json();
            
            const getWeatherEmoji = (weatherMain) => {
              if (weatherMain === 'Clear') return '☀️';
              if (weatherMain === 'Clouds') return '☁️';
              if (weatherMain === 'Rain') return '🌧️';
              if (weatherMain === 'Snow') return '🌨️';
              return '🌤️';
            };
            
            setWeather({
              emoji: getWeatherEmoji(data.weather[0].main),
              desc: `${data.weather[0].description} (서울)`,
              temp: `${Math.round(data.main.temp)}°C`
            });
          } catch (error) {
            console.error('날씨 조회 실패:', error);
            setWeather({ emoji: '🌤️', desc: '날씨 로딩 실패', temp: '--°C' });
          }
        }
      } catch (error) {
        console.error('날씨 기능 오류:', error);
        setWeather({ emoji: '🌤️', desc: '날씨 서비스 오류', temp: '--°C' });
      }
    };

    fetchWeather();
  }, []);

  // 오늘의 행운 숫자
  const getLuckyNumber = () => {
    const today = new Date();
    const seed = today.getDate() + today.getMonth() + today.getFullYear();
    return (seed % 100) + 1;
  };

  // 랜덤 명언 관련 팁
  const getQuoteTip = () => {
    const tips = [
      "💡 새로고침하면 새로운 명언을 만날 수 있어요",
      "🎯 카테고리를 선택해서 원하는 주제의 명언을 보세요",
      "⭐ 마음에 드는 명언은 캡처해서 간직하세요",
      "🌈 매일 다른 명언으로 하루를 시작해보세요",
      "🔄 버튼을 클릭하면 다음 명언을 볼 수 있어요"
    ];
    return tips[Math.floor(Math.random() * tips.length)];
  };

  return (
    <footer className="text-center mt-16 animate-fade-in">
      {/* 통계 정보 */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8 max-w-2xl mx-auto">
          <div className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-2xl p-5 backdrop-blur-sm border border-white/10 hover:bg-white/5 transition-all duration-300 hover:scale-105">
            <div className="text-3xl mb-3">📊</div>
            <div className="text-white text-xl font-bold mb-1">2025년 {getYearProgress().percentage}%</div>
            <div className="text-white/70 text-sm font-medium">{getYearProgress().dayOfYear}일차 • {getYearProgress().remaining}일 남음</div>
          </div>
          
          <div className="bg-gradient-to-br from-green-500/10 to-teal-500/10 rounded-2xl p-5 backdrop-blur-sm border border-white/10 hover:bg-white/5 transition-all duration-300 hover:scale-105">
            <div className="text-3xl mb-3">{weather.emoji}</div>
            <div className="text-white text-xl font-bold mb-1">{weather.desc}</div>
            <div className="text-white/70 text-sm font-medium">{weather.temp} • 현재 날씨</div>
          </div>
          
          <div className="bg-gradient-to-br from-amber-500/10 to-orange-500/10 rounded-2xl p-5 backdrop-blur-sm border border-white/10 hover:bg-white/5 transition-all duration-300 hover:scale-105">
            <div className="text-3xl mb-3">🍀</div>
            <div className="text-white text-xl font-bold mb-1">{getLuckyNumber()}</div>
            <div className="text-white/70 text-sm font-medium">오늘의 행운숫자</div>
          </div>
        </div>
      )}

      {/* 사용 팁 */}
      <div className="bg-gradient-to-r from-purple-500/10 via-pink-500/10 to-blue-500/10 rounded-2xl p-6 mb-8 max-w-2xl mx-auto backdrop-blur-sm border border-white/10">
        <div className="text-white/90 text-base mb-2">
          {getQuoteTip()}
        </div>
        <div className="text-white/60 text-xs">
          Daily Messages 사용 팁
        </div>
      </div>

      {/* 인기 카테고리 */}
      {stats?.topCategories && (
        <div className="mb-8">
          <div className="text-white/80 text-sm font-medium mb-3">🔥 인기 카테고리 TOP 5</div>
          <div className="flex flex-wrap justify-center gap-2">
            {stats.topCategories.slice(0, 5).map((cat, index) => {
              const categoryEmojis = {
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
                <span 
                  key={index}
                  className="px-3 py-1.5 bg-white/10 rounded-full text-white/80 text-xs backdrop-blur-sm border border-white/10 hover:bg-white/20 transition-all duration-200"
                >
                  {categoryEmojis[cat.category]} {cat.category}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* 설명 */}
      <div className="max-w-lg mx-auto mb-6">
        <p className="text-white/70 text-sm leading-relaxed mb-2">
          세계적인 철학자, 작가, 리더들의 지혜를 매일 새롭게 만나보세요 ✨
        </p>
        <p className="text-white/50 text-xs">
          인생을 바꾸는 하루 한 줄의 힘
        </p>
      </div>

      {/* 하단 여백 */}
      <div className="h-8"></div>
    </footer>
  );
};

export default Footer;