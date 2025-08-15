from PIL import Image, ImageDraw, ImageFont
import os

# 기능 그래픽 생성 (1024x500)
img = Image.new('RGBA', (1024, 500), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 그라데이션 배경
for i in range(500):
    color_value = int(59 + (37 * i / 500))  # #3B82F6 to #2563EB
    draw.rectangle([0, i, 1024, i+1], fill=(color_value, 130-int(i*0.04), 246))

# 왼쪽에 태양 아이콘
sun_center = (200, 250)
sun_radius = 80

# 태양 광선
import math
for i in range(12):
    angle = i * math.pi / 6
    x1 = sun_center[0] + math.cos(angle) * (sun_radius + 20)
    y1 = sun_center[1] + math.sin(angle) * (sun_radius + 20)
    x2 = sun_center[0] + math.cos(angle) * (sun_radius + 50)
    y2 = sun_center[1] + math.sin(angle) * (sun_radius + 50)
    draw.line([(x1, y1), (x2, y2)], fill='#FDE047', width=8)

# 태양 원
draw.ellipse([sun_center[0] - sun_radius, sun_center[1] - sun_radius,
              sun_center[0] + sun_radius, sun_center[1] + sun_radius],
             fill='#FDE047')

# 텍스트
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 72)
    font_subtitle = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 36)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()

# 메인 타이틀
draw.text((400, 180), "모닝", fill='white', font=font_title)

# 서브 타이틀
draw.text((400, 280), "매일 아침 당신을 위한", fill='#E0E7FF', font=font_subtitle)
draw.text((400, 330), "따뜻한 응원 메시지", fill='#E0E7FF', font=font_subtitle)

# 저장
img.save('public/feature_graphic.png')
print("OK - feature_graphic.png created (1024x500)")