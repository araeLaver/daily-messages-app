from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    # 이미지 생성
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 배경 - 파란색
    draw.rounded_rectangle([0, 0, size, size], radius=size//10, fill='#3B82F6')
    
    # 태양 아이콘 (아침을 상징)
    sun_center = (size//2, size//2.5)
    sun_radius = size//6
    
    # 태양 광선
    import math
    for i in range(8):
        angle = i * math.pi / 4
        x1 = sun_center[0] + math.cos(angle) * (sun_radius + 10)
        y1 = sun_center[1] + math.sin(angle) * (sun_radius + 10)
        x2 = sun_center[0] + math.cos(angle) * (sun_radius + size//15)
        y2 = sun_center[1] + math.sin(angle) * (sun_radius + size//15)
        draw.line([(x1, y1), (x2, y2)], fill='#FDE047', width=size//50)
    
    # 태양 원
    draw.ellipse([sun_center[0] - sun_radius, sun_center[1] - sun_radius,
                  sun_center[0] + sun_radius, sun_center[1] + sun_radius],
                 fill='#FDE047')
    
    # 텍스트 - 모닝
    try:
        # 한글 폰트 시도
        font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", size//5)
    except:
        # 기본 폰트
        font = ImageFont.load_default()
    
    text = "모닝"
    # 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = int(size * 0.7)
    
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    return img

# 아이콘 생성
print("Creating icons...")

# logo192.png
icon192 = create_icon(192)
icon192.save('public/logo192.png')
print("OK - logo192.png created")

# logo512.png
icon512 = create_icon(512)
icon512.save('public/logo512.png')
print("OK - logo512.png created")

# favicon.ico (여러 크기 포함)
icon16 = create_icon(16)
icon32 = create_icon(32)
icon48 = create_icon(48)

# ICO 파일로 저장 (여러 크기 포함)
icon32.save('public/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
print("OK - favicon.ico created")

print("All icons created successfully!")