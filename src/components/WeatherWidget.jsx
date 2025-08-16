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
    // 임시 날씨 데이터 (실제로는 날씨 API를 호출해야 함)
    const mockWeather = {
      location: '서울',
      temperature: Math.floor(Math.random() * 20) + 10, // 10-30도
      condition: ['sunny', 'cloudy', 'rainy'][Math.floor(Math.random() * 3)],
      humidity: Math.floor(Math.random() * 40) + 30, // 30-70%
    };

    // 즉시 날씨 데이터 설정
    setWeather(mockWeather);
    setLoading(false);
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