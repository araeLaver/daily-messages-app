// 임시 Mock API - 로컬에서 바로 사용할 수 있도록
const messages = [
    // 동기부여 카테고리
    {
        id: 1,
        text: "새로운 하루가 시작됩니다. 오늘도 좋은 하루 되세요! ✨",
        author: "",
        category: "동기부여",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 2,
        text: "오늘 하루도 당신의 꿈에 한 걸음 더 가까워지는 날이 되길 바랍니다.",
        author: "",
        category: "동기부여",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 3,
        text: "매일 아침이 새로운 기회입니다. 오늘도 최선을 다해보세요!",
        author: "",
        category: "동기부여",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 4,
        text: "당신의 잠재력은 무한합니다. 오늘 그 힘을 발휘해보세요.",
        author: "",
        category: "동기부여",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 5,
        text: "성공은 준비된 자에게 찾아옵니다. 오늘도 준비하세요.",
        author: "",
        category: "동기부여",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 성장 카테고리
    {
        id: 6,
        text: "작은 변화가 큰 결과를 만듭니다. 오늘도 작은 한 걸음을 내딛어보세요.",
        author: "",
        category: "성장",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 7,
        text: "어제보다 조금 더 나은 자신이 되는 것, 그것이 성장입니다.",
        author: "",
        category: "성장",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 8,
        text: "배움에는 끝이 없습니다. 오늘도 새로운 것을 배워보세요.",
        author: "",
        category: "성장",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 9,
        text: "실수는 성장의 밑거름입니다. 두려워하지 마세요.",
        author: "",
        category: "성장",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 자신감 카테고리
    {
        id: 10,
        text: "당신은 지금 이 순간에도 성장하고 있습니다. 자신을 믿으세요.",
        author: "",
        category: "자신감",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 11,
        text: "당신은 생각보다 강하고, 할 수 있는 일이 생각보다 많습니다.",
        author: "",
        category: "자신감",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 12,
        text: "자신을 믿는 마음이 기적을 만듭니다.",
        author: "",
        category: "자신감",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 13,
        text: "당신의 가능성은 당신이 정하는 한계까지입니다.",
        author: "",
        category: "자신감",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 감사 카테고리
    {
        id: 14,
        text: "감사한 마음으로 하루를 시작하면 더 많은 좋은 일이 찾아옵니다.",
        author: "",
        category: "감사",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 15,
        text: "오늘 하루도 감사한 마음으로 시작하세요.",
        author: "",
        category: "감사",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 16,
        text: "작은 것에도 감사할 줄 아는 마음이 행복의 열쇠입니다.",
        author: "",
        category: "감사",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 17,
        text: "지금 이 순간도 감사할 일들로 가득합니다.",
        author: "",
        category: "감사",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 희망 카테고리
    {
        id: 18,
        text: "어둠이 깊을수록 새벽은 가까워집니다.",
        author: "",
        category: "희망",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 19,
        text: "내일은 오늘보다 더 나은 날이 될 것입니다.",
        author: "",
        category: "희망",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 20,
        text: "포기하지 마세요. 가장 어두운 순간이 새벽 바로 전입니다.",
        author: "",
        category: "희망",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 21,
        text: "희망은 마음의 날개입니다. 높이 날아오르세요.",
        author: "",
        category: "희망",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 도전 카테고리
    {
        id: 22,
        text: "새로운 도전이 새로운 가능성을 열어줍니다.",
        author: "",
        category: "도전",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 23,
        text: "두려움을 딛고 한 걸음 나아가는 용기를 가지세요.",
        author: "",
        category: "도전",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 24,
        text: "도전하지 않으면 성장도 없습니다.",
        author: "",
        category: "도전",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 25,
        text: "오늘도 새로운 도전으로 자신을 놀라게 해보세요.",
        author: "",
        category: "도전",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 성취 카테고리
    {
        id: 26,
        text: "작은 성공들이 모여 큰 성취를 만듭니다.",
        author: "",
        category: "성취",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 27,
        text: "목표를 향한 한 걸음 한 걸음이 모두 소중합니다.",
        author: "",
        category: "성취",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 28,
        text: "노력한 만큼 반드시 결과가 따라옵니다.",
        author: "",
        category: "성취",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 29,
        text: "꿈꾸던 일들이 하나씩 현실이 되어가고 있습니다.",
        author: "",
        category: "성취",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 행복 카테고리
    {
        id: 30,
        text: "행복은 멀리 있지 않습니다. 지금 여기에 있습니다.",
        author: "",
        category: "행복",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 31,
        text: "오늘 하루도 행복한 순간들로 채워보세요.",
        author: "",
        category: "행복",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 32,
        text: "웃음은 마음의 비타민입니다. 오늘도 많이 웃으세요.",
        author: "",
        category: "행복",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 33,
        text: "행복의 열쇠는 당신의 마음 속에 있습니다.",
        author: "",
        category: "행복",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 인내 카테고리
    {
        id: 34,
        text: "참고 견디는 힘이 진정한 강함입니다.",
        author: "",
        category: "인내",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 35,
        text: "지금의 어려움도 지나갈 구름일 뿐입니다.",
        author: "",
        category: "인내",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 36,
        text: "인내는 쓰지만 그 열매는 달콤합니다.",
        author: "",
        category: "인내",
        time_of_day: "evening",
        season: "all",
        source: "local",
        view_count: 0
    },

    // 꿈 카테고리
    {
        id: 37,
        text: "당신의 꿈은 당신이 생각하는 것보다 가까이 있습니다.",
        author: "",
        category: "꿈",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 38,
        text: "꿈을 꾸는 자만이 꿈을 이룰 수 있습니다.",
        author: "",
        category: "꿈",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 39,
        text: "큰 꿈을 가지세요. 꿈은 현실이 됩니다.",
        author: "",
        category: "꿈",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    },
    {
        id: 40,
        text: "오늘도 당신만의 특별한 이야기를 써나가세요.",
        author: "",
        category: "꿈",
        time_of_day: "morning",
        season: "all",
        source: "local",
        view_count: 0
    }
];

export const mockApi = {
    getRandomMessage: (filters = {}) => {
        return new Promise((resolve) => {
            setTimeout(() => {
                let availableMessages = messages.filter(msg => true);
                
                // 필터링
                if (filters.category && filters.category !== 'all') {
                    availableMessages = availableMessages.filter(msg => msg.category === filters.category);
                }
                
                if (filters.time_of_day) {
                    availableMessages = availableMessages.filter(msg => 
                        msg.time_of_day === filters.time_of_day || msg.time_of_day === null
                    );
                }
                
                // 랜덤 선택
                const randomIndex = Math.floor(Math.random() * availableMessages.length);
                const selectedMessage = availableMessages[randomIndex] || messages[0];
                
                // 조회수 증가
                selectedMessage.view_count += 1;
                
                resolve(selectedMessage);
            }, 100); // 실제 API 호출처럼 약간의 딜레이
        });
    },
    
    getCategories: () => {
        return new Promise((resolve) => {
            setTimeout(() => {
                const categories = [...new Set(messages.map(msg => msg.category))];
                resolve(categories);
            }, 50);
        });
    },
    
    getStats: () => {
        return new Promise((resolve) => {
            setTimeout(() => {
                const byCategory = {};
                const bySource = {};
                
                messages.forEach(msg => {
                    byCategory[msg.category] = (byCategory[msg.category] || 0) + 1;
                    bySource[msg.source] = (bySource[msg.source] || 0) + 1;
                });
                
                resolve({
                    total_messages: messages.length,
                    by_category: byCategory,
                    by_source: bySource
                });
            }, 50);
        });
    },
    
    checkHealth: () => {
        return new Promise((resolve) => {
            resolve({ 
                status: 'healthy',
                message_count: messages.length,
                timestamp: new Date().toISOString()
            });
        });
    }
};