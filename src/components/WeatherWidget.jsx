import React, { useState, useEffect } from 'react';
import { Cloud, Sun, CloudRain, CloudSnow, Wind } from 'lucide-react';

const WeatherWidget = () => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  // 날씨 아이콘 매핑
  const getWeatherIcon = (condition) => {
    const iconClass = "w-5 h-5";
    switch (condition?.toLowerCase()) {
      case 'sunny':
      case 'clear':
        return <Sun className={`${iconClass} text-yellow-300`} />;
      case 'cloudy':
      case 'overcast':
        return <Cloud className={`${iconClass} text-gray-300`} />;
      case 'rainy':
      case 'rain':
        return <CloudRain className={`${iconClass} text-blue-300`} />;
      case 'snowy':
      case 'snow':
        return <CloudSnow className={`${iconClass} text-white`} />;
      default:
        return <Wind className={`${iconClass} text-gray-300`} />;
    }
  };

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        // 사용자 위치 가져오기
        if (!navigator.geolocation) {
          throw new Error('위치 서비스가 지원되지 않습니다');
        }

        const position = await new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject, {
            timeout: 5000,
            enableHighAccuracy: false
          });
        });

        const { latitude, longitude } = position.coords;
        
        // OpenWeatherMap API 호출
        const API_KEY = '8a7a1c49b83e4b4e65fd14b9e8b6c7a2';
        const response = await fetch(
          `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${API_KEY}&units=metric&lang=kr`
        );
        
        if (!response.ok) {
          throw new Error('날씨 정보를 가져올 수 없습니다');
        }
        
        const data = await response.json();
        
        setWeather({
          location: data.name || '현재 위치',
          temperature: Math.round(data.main.temp),
          condition: data.weather[0].main.toLowerCase(),
          humidity: data.main.humidity,
          description: data.weather[0].description
        });
      } catch (error) {
        console.error('날씨 정보 로드 실패:', error);
        // 폴백: 서울 날씨
        const fallbackWeather = {
          location: '서울',
          temperature: 22,
          condition: 'clear',
          humidity: 65,
          description: '맑음'
        };
        setWeather(fallbackWeather);
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-full backdrop-blur-sm">
        <div className="animate-spin w-4 h-4 border-2 border-white/20 border-t-white/60 rounded-full"></div>
        <span className="text-white/80 text-sm">날씨 확인중...</span>
      </div>
    );
  }

  if (!weather) {
    return null;
  }

  return (
    <div className="flex items-center gap-2 px-3 py-2 bg-white/10 rounded-full backdrop-blur-sm">
      {getWeatherIcon(weather.condition)}
      <span className="text-white/80 text-sm">
        {weather.location} {weather.temperature}°C
      </span>
    </div>
  );
};

export default WeatherWidget;