// 영어 카테고리를 한글로 매핑
export const categoryTranslations = {
  motivation: '동기부여',
  wisdom: '지혜',
  happiness: '행복',
  success: '성공',
  love: '사랑',
  friendship: '우정',
  family: '가족',
  health: '건강',
  mindfulness: '마음챙김',
  gratitude: '감사',
  courage: '용기',
  perseverance: '인내',
  leadership: '리더십',
  creativity: '창의성',
  learning: '배움',
  growth: '성장',
  peace: '평화',
  hope: '희망',
  faith: '믿음',
  humor: '유머',
  adventure: '모험',
  dreams: '꿈',
  passion: '열정',
  resilience: '회복력',
  kindness: '친절'
};

export const getKoreanCategory = (category) => {
  return categoryTranslations[category] || category;
};