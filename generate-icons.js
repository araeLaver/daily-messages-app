const fs = require('fs');
const { createCanvas } = require('canvas');

// 아이콘 생성 함수
function createIcon(size) {
    const canvas = createCanvas(size, size);
    const ctx = canvas.getContext('2d');
    
    // 배경 - 파란색 그라데이션
    const gradient = ctx.createLinearGradient(0, 0, size, size);
    gradient.addColorStop(0, '#3B82F6');
    gradient.addColorStop(1, '#2563EB');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, size, size);
    
    // 둥근 모서리 효과
    ctx.globalCompositeOperation = 'destination-in';
    ctx.beginPath();
    ctx.roundRect(0, 0, size, size, size * 0.1);
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';
    
    // 태양 아이콘 (아침을 상징)
    ctx.fillStyle = '#FDE047';
    ctx.shadowColor = '#FCD34D';
    ctx.shadowBlur = size * 0.05;
    ctx.beginPath();
    ctx.arc(size/2, size/2.5, size/6, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    
    // 태양 광선
    ctx.strokeStyle = '#FDE047';
    ctx.lineWidth = size * 0.02;
    for (let i = 0; i < 8; i++) {
        const angle = (i * Math.PI) / 4;
        const x1 = size/2 + Math.cos(angle) * size/4;
        const y1 = size/2.5 + Math.sin(angle) * size/4;
        const x2 = size/2 + Math.cos(angle) * size/3.2;
        const y2 = size/2.5 + Math.sin(angle) * size/3.2;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
    }
    
    // 텍스트 - 모닝
    ctx.fillStyle = '#FFFFFF';
    ctx.font = `bold ${size/5}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('모닝', size/2, size * 0.75);
    
    return canvas.toBuffer();
}

// 아이콘 생성 및 저장
console.log('Generating icons...');

// logo192.png
fs.writeFileSync('./public/logo192.png', createIcon(192));
console.log('✓ logo192.png created');

// logo512.png
fs.writeFileSync('./public/logo512.png', createIcon(512));
console.log('✓ logo512.png created');

console.log('Icons generated successfully!');