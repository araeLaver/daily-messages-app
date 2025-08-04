import { useState, useEffect, useCallback } from 'react';

export const useMessageCounter = () => {
  const [count, setCount] = useState(0);

  // 카운터 초기화 (페이지 새로고침시마다 0에서 시작)
  useEffect(() => {
    setCount(0);
  }, []);

  // 카운터 증가
  const incrementCounter = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);

  // 카운터 리셋
  const resetCounter = useCallback(() => {
    setCount(0);
  }, []);

  return {
    count,
    incrementCounter,
    resetCounter
  };
};